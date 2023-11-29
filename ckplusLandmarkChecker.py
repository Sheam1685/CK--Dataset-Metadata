import matplotlib.pyplot as plt
from PIL import Image

# Read landmarks from a file
def read_landmarks(file_path):
    landmarks = []
    with open(file_path, 'r') as file:
        for line in file:
            coordinates = line.strip().split()
            if len(coordinates) == 2:
                x, y = float(coordinates[0]), float(coordinates[1])
                landmarks.append([x, y])
    return landmarks

# Function to plot landmarks on top of the image
def plot_landmarks(landmarks, color):
    x = [landmark[0] for landmark in landmarks]
    y = [landmark[1] for landmark in landmarks]
    plt.scatter(x, y, color=color, s=5)  # Adjust 's' for point size

# File path containing landmarks
file_path_red = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S011\\001\\S011_001_00000001_landmarks.txt"
file_path_green = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S011\\001\\S011_001_00000016_landmarks.txt"

# Read red landmarks from file
landmarks_red = read_landmarks(file_path_red)

# Read green landmarks from file (if available)
landmarks_green = read_landmarks(file_path_green)

# Load the image
image_path_red = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images\\S011\\001\\S011_001_00000001.png'
image_path_green = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images\\S011\\001\\S011_001_00000016.png'
image_red = Image.open(image_path_red)
image_green = Image.open(image_path_green)

# Plot the image
plt.figure(figsize=(8, 8))
plt.imshow(image_red)
plt.axis('off')  # Turn off axis labels

# Plot red landmarks on the red image
plot_landmarks(landmarks_red, 'red')

plt.show()

# Plot the image
plt.figure(figsize=(8, 8))
plt.imshow(image_green)
plt.axis('off')  # Turn off axis labels

# Plot green landmarks on the green image
plot_landmarks(landmarks_green, 'green')

plt.show()