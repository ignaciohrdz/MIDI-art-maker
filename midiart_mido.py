import cv2
print("Using OpenCV ", cv2.__version__)
import numpy as np

import os
import random

from mido import Message, MidiFile, MidiTrack

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

    path_images = "demo_images"
    use_scale = scales.f_maj

    # Load an image
    demo_imgs = ["tux.png", "apple_logo.jpg", "win98_logo.jpg"]
    img = cv2.imread(os.path.join(path_images, demo_imgs[0]))
    img = cv2.flip(img, 0)

    # cv2.imshow("Image", img)
    # cv2.waitKey()

    num_rows = 128
    num_cols = int(img.shape[0]*128/img.shape[1])
    original_shape = (img.shape[1], img.shape[0], img.shape[2])
    new_shape = (num_cols, num_rows, 3)

    print("Resizing (w,h,c): {} -> {}".format(original_shape, new_shape))
    img = cv2.resize(img, tuple(new_shape[:2]))

    cv2.imshow("Image", img)
    cv2.waitKey()

    print("Computing image edges")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = auto_canny(img_gray)

    cv2.imshow("Image", canny)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print("Generating MIDI file")
    mid = MidiFile()
    mid.ticks_per_beat = 4
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message("program_change", program=12))

    # TODO: new fueature: randomly choose note duration?
    delta = [1,2,3,4]
    for i in range(num_cols):
        col = canny[:,i]
        if col.sum() > 0:
            indexes = list(np.where(col>0)[0])
            written = []
            for note in indexes:
                if note in use_scale:
                    track.append(Message("note_on", note=note, velocity=64, time=random.choices(delta, k=1)[0]))
                    written.append(note)
                # track.append(Message("note_off", note=note, velocity=64, time=delta)) # I don't know how this works
            print("Written: ", indexes)
        else:
            pass

    mid.save("midiart.mid")

    print("Done")


