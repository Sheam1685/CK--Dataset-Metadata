from PIL import Image, ImageDraw
import math

def read_landmarks(file_path, supersample_factor=10):
    landmarks = []
    with open(file_path, 'r') as file:
        for line in file:
            coordinates = line.strip().split()
            if len(coordinates) == 2:
                x, y = float(coordinates[0])*supersample_factor, float(coordinates[1])*supersample_factor
                landmarks.append([x, y])
    return landmarks
  
def angle_between_points(point1, point2):

    degree = math.degrees(math.atan2(point2[1] - point1[1], point2[0] - point1[0]))
    if degree < 0:
        degree = 360 + degree

    return degree

def plot_landmarks(image, emotion, landmarks, width, height):
    size = 30
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    image.save(f'{emotion}_landmarks.png')

def plot_line_features(image, landmarks, features, width, height):
    size = 30
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    for i in range(len(features)):
        feature = features[i]
        if len(feature) == 2:
          point1 = tuple(landmarks[feature[0]-1])
          point2 = tuple(landmarks[feature[1]-1])
        elif len(feature) == 3:
          point1 = tuple(landmarks[feature[0]-1])
          point2 = tuple(landmarks[feature[1]-1])
          # Take the midpoint of the two points
          point1 = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
          point2 = tuple(landmarks[feature[2]-1])
          
        draw.line([point1, point2], fill=(0, 255, 0, 255), width=int(size*0.9))
    
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    image.save(f'A&K_features.png')
    
def plot_features_on_image(image_path, landmarks, supersample_factor, features):
    image = Image.open(image_path)
    # Conver to grayscale and then to RGBA
    image = image.convert("L")
    image = image.convert("RGBA")
    width, height = image.size
    im = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    image_line = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    
    plot_line_features(image_line, landmarks, features, width, height)





supersample_factor = 10

image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images\\S056\\003\\S056_003_00000001.png"
landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S056\\003\\S056_003_00000001_landmarks.txt", supersample_factor)

# Take features as input and plot them on the image

features = []

with open(f'Features/neutral.txt', 'r') as file:
    for line in file:
        feature = line.strip().split()
        feature = [int(value) for value in feature[0][2:-1].split(',')]
        features.append(feature)
    features.append([37,46,9])
    print("Feature extracted")

plot_features_on_image(image_path, landmarks, supersample_factor, features)