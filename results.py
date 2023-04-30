import numpy as np
import pickle

from PIL import Image
from tqdm import tqdm

from f1 import LAPS,pitstops

results = pickle.load(open( "results.p", "rb" ))

size = (LAPS-1) * (LAPS-2) // 2

# go through all rows and check for all-blue
for a,b in pitstops():
    all_blue = True
    for c,d in pitstops():
        if results[a, b, c, d] == 1:
            all_blue = False
            break
    if all_blue:
        print(f'All blue row: {a} {b}')
        
# go through all columns and check for all-red
for a,b in pitstops():
    all_red = True
    for c,d in pitstops():
        if results[a, b, c, d] == -1:
            all_red = False
            break
    if all_red:
        print(f'All red row: {a} {b}')
        
# go through all columns and check for all-blue
for c,d in pitstops():
    all_blue = True
    for a,b in pitstops():
        if results[a, b, c, d] == 1:
            all_blue = False
            break
    if all_blue:
        print(f'All blue column: {c} {d}')

# go through all columns and check for all-red
for c,d in pitstops():
    all_red = True
    for a,b in pitstops():
        if results[a, b, c, d] == -1:
            all_red = False
            break
    if all_red:
        print(f'All red column: {c} {d}')
        
# define color mappings
color_map = {
    -1: (0, 0, 255),  # blue
    0: (0, 0, 0),     # black
    1: (255, 0, 0)    # red
}

image_matrix = np.zeros((size, size, 3), dtype=np.uint8)
for i,(a,b) in enumerate(tqdm(pitstops(), total=size)):
    for j,(c,d) in enumerate(pitstops()):
        image_matrix[i, j] = color_map[results[a, b, c, d]]
        
image = Image.fromarray(image_matrix)

# Save the image as a PNG file
image.save('results.png')
