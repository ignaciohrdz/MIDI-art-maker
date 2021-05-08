# Scales
import random

def create_scale(scale):
    global NOTES
    scale_notes = []
    for note in scale:
        scale_notes += NOTES[note]
    return scale_notes


def get_random_scale():
    global major_scales
    scales = major_scales
    random.shuffle(scales)
    return scales[0]



NOTES = ["c", "csharp", "d", "dsharp", "e", "f", "fsharp", "g", "gsharp", "a", "asharp", "b"]
NOTES = {name: [i+12*j for j in range(11) if i+12*j <= 127] for i,name in enumerate(NOTES)}
 
c_maj = ["c", "d", "e", "f", "g", "a", "b"]
c_maj = create_scale(c_maj)
d_maj = ["d", "e","fsharp", "g", "a", "b", "csharp"]
d_maj = create_scale(d_maj)
e_maj = ["e", "fsharp", "gsharp", "a", "b", "csharp", "dsharp"]
e_maj = create_scale(e_maj)
f_maj = ["f", "g", "a", "asharp", "c", "d", "e"]
f_maj = create_scale(f_maj)
g_maj = ["g", "a", "b", "c", "d", "e", "f"]
g_maj = create_scale(g_maj)
a_maj = ["a", "b", "csharp", "d", "e", "fsharp", "gsharp"]
a_maj = create_scale(a_maj)
b_maj = ["b", "csharp", "dsharp", "e", "fsharp", "gsharp", "asharp"]
b_maj = create_scale(b_maj)

major_scales = [c_maj, d_maj, e_maj, f_maj, g_maj, a_maj, b_maj]



