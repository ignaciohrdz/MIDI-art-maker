import cv2
print("Using OpenCV ", cv2.__version__)
import numpy as np
import os
from midiutil.MidiFile import MIDIFile


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

    # Load an image
    img = cv2.imread(os.path.join(path_images, "tux.png"))

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

    track = 0   # the only track
    time = 5    # start at the 10th beat
    volume = 100 # 0-127, as per the MIDI standard
    duration = 1 # in beats
    tempo = 60 # BPM

    mf = MIDIFile(1)     # only 1 track
    mf.addTrackName(track, time, "MIDIartMade")
    mf.addTempo(track, time, tempo)

    for i in range(num_cols):
        channel = 0
        col = canny[:,i]
        if col.sum() > 0:
            indexes = list(np.where(col>0)[0])
            print("Writing: ", indexes)
            for pitch in indexes:
                mf.addNote(track, channel, pitch, time, duration, 0)
                channel += 1
        else:
            mf.addNote(track, channel, 0, time, duration, 0)
        time += 1

    with open("MIDIart.mid", 'wb') as outf:
        mf.writeFile(outf)

    print("Done")


