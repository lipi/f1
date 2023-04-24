import numpy as np
import pickle

from PIL import Image

results = pickle.load(open( "results.p", "rb" ))

matrix = results.reshape((70*70, 70*70))

# Convert the matrix to a grayscale image
image = Image.fromarray((matrix * 255).astype(np.uint8), mode='L')

# Save the image as a PNG file
image.save('results.png')
