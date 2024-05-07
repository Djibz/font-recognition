import os
import sys
import glob
import ntpath
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN

TRESHOLD = 125
IMAGE_SIZE = 100

def treshold(image):
    image_seuillee = np.copy(image)
    image_seuillee = image>TRESHOLD
    return(image_seuillee)

def make_square(im, min_size=256, fill_color=(255, 255, 255, 255)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

input_directory  = './images'
output_directory = './data'

if len(sys.argv) > 1:
    input_directory = sys.argv[1].rstrip('/\\')

if len(sys.argv) > 2:
    output_directory = sys.argv[2].rstrip('/\\')

for text_image in glob.glob(f'{input_directory}/*.png'):

    name = ' '.join(ntpath.basename(text_image).split('.')[:-1])

    font_dir = f"{output_directory}/{name}"

    if not os.path.exists(font_dir):
        os.makedirs(font_dir)

    im = Image.open(text_image).convert('L')
    im = np.array(im)

    treshold_img = treshold(im)

    X = np.column_stack(np.where(treshold_img==0))

    model = DBSCAN(eps=3, min_samples=10)
    yhat = model.fit_predict(X)
    clusters = np.unique(yhat)

    for i, cluster in enumerate(clusters):
        if cluster == -1: continue #global cluster for random points

        points = X[np.where(yhat == cluster)]

        w = max(points[:, 0]) - min(points[:, 0])
        h = max(points[:, 1]) - min(points[:, 1])

        fragment = np.ones((w+1, h+1), dtype=bool)
        fragment[points[:, 0] - min(points[:, 0]), points[:, 1] - min(points[:, 1])] = False

        fragment_im = Image.fromarray(fragment)
        normalized = make_square(fragment_im, min_size=IMAGE_SIZE)

        normalized.save(f"{font_dir}/{i}.png")

    