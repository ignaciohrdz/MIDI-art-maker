import cv2
import numpy as np

import os
import argparse
import random

from music21 import *
import scales


# From pyimagesearch
# URL: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
def auto_canny(image, sigma=0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, help="Path to the image", required=True)
    parser.add_argument('--out_img_path', type=str, help="Path for the output images", required=False)
    parser.add_argument('--out_midi_path', type=str, help="Path for the output MIDIs", required=False)
    parser.add_argument('--scale',
                        type=str,
                        choices=list(scales.major_scales_dict.keys()),
                        default='f_maj', required=False,
                        help='Scale (major or minor)')
    parser.add_argument("--show", action='store_true', help='Display the output images')
    args = parser.parse_args()

    use_scale = args.scale

    # Demo images
    # path_images = "demo_images"
    # demo_imgs = ["tux.png", "apple_logo.jpg", "win98_logo.jpg"]
    # img_name = demo_imgs[0]
    # img = cv2.imread(os.path.join(path_images, img_name))

    # Load an image
    img_path = args.img_path
    img_name = os.path.basename(img_path)
    img = cv2.imread(os.path.join(img_path))
    img = cv2.flip(img, 0)

    # cv2.imshow("Image", img)
    # cv2.waitKey()

    num_rows = 128
    num_cols = int(img.shape[0]*128/img.shape[1])
    original_shape = (img.shape[1], img.shape[0], img.shape[2])
    new_shape = (num_cols, num_rows, 3)

    print("Resizing (w,h,c): {} -> {}".format(original_shape, new_shape))
    img = cv2.resize(img, tuple(new_shape[:2]))

    if args.show:
        cv2.imshow("Image", img)
        cv2.waitKey()

    print("Computing image edges")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = auto_canny(img_gray)

    if args.show:
        cv2.imshow("Image", canny)
        cv2.waitKey()
        cv2.destroyAllWindows()

    # Export the Canny edges as an image
    if not args.out_img_path:
        path_out_imgs = os.path.dirname(img_path)
    else:
        path_out_imgs = args.out_img_path
    cv2.imwrite(os.path.join(path_out_imgs, img_name.split(".")[0] + "_bw.jpg"), cv2.flip(canny, 0))

    print("Generating MIDI file")
    s = stream.Stream()

    # TODO: randomly choose note duration?
    q_length = [1, 2, 3, 4]
    for i in range(num_cols):
        col = canny[:,i]
        if col.sum() > 0:
            indexes = list(np.where(col>0)[0])
            indexes = [i for i in indexes if i in use_scale]  # Filtering the notes
            total_notes = len(indexes)

            # If there are enough notes, I write a chord
            if len(indexes) > 6:
                rand_chord = random.sample(indexes, 4)
                rand_length = random.choice(q_length)/4
                c = chord.Chord()
                for c_note in rand_chord:
                    n = note.Note()
                    n.pitch.midi = c_note
                    n.duration.quarterLength = rand_length
                    c.add(n)
                    indexes.remove(c_note)
                s.append(c)
            
            # Adding the single notes
            for px_note in indexes:
                n = note.Note()
                n.pitch.midi = px_note
                n.duration.quarterLength = random.choice(q_length)/4
                s.append(n)

            print("Total notes: {} | Written: {}".format(total_notes, indexes))
        else:
            pass

    # Export the result
    if not args.out_midi_path:
        path_out_midi = "export"
        if not os.path.isdir(path_out_midi):
            os.mkdir(path_out_midi)
    else:
        path_out_midi = args.out_midi_path
    s.write('midi', os.path.join(path_out_midi, os.path.splitext(img_name)[0] + '_midiart_music21.mid'))
    print("Done")


