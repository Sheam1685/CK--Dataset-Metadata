import os
import random
from PIL import Image, ImageDraw

def read_landmarks(file_path):
    landmarks = []
    with open(file_path, 'r') as file:
        for line in file:
            coordinates = line.strip().split()
            if len(coordinates) == 2:
                x, y = float(coordinates[0]), float(coordinates[1])
                landmarks.append([x, y])
    return landmarks

def plot_landmarks_on_image(image, landmarks, color='red'):
    size = 2
    draw = ImageDraw.Draw(image)
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=color)
    # Show the image
    image.show()
    image.save("anger.png")

image = Image.open("C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images\\S010\\004\\S010_004_00000019.png")
landmark = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S010\\004\\S010_004_00000019_landmarks.txt")
plot_landmarks_on_image(image, landmark)