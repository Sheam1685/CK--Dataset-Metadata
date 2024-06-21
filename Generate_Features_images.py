from PIL import Image, ImageDraw
import math


# Choose emotion and mode from here. 
# emotion = "happiness"
# emotion = "surprise"
# emotion = "anger"
# emotion = "sadness"
# emotion = "fear"
emotion = "disgust"
# mode = "neutral"
mode = "emotional"
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

def plot_line_features(image, emotion, landmarks, line_features, width, height):
    size = 30
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    for i in range(len(line_features)):
        feature = line_features[i]
        point1 = tuple(landmarks[feature[0]-1])
        point2 = tuple(landmarks[feature[1]-1])
        # Draw double headed arrow
        draw.line([point1, point2], fill=(0, 255, 0, 255), width=int(size*0.9))
    
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    if mode == "emotional":
        image.save(f'{emotion}_line_features.png')
    elif mode == "neutral":
        image.save(f'{emotion}_line_features_neutral.png')
    
def plot_angle_features(image, emotion, landmarks, angle_features, width, height):
    size = 30
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    for i in range(len(angle_features)):

        feature = angle_features[i]
        point1 = tuple(landmarks[feature[0]-1])
        point2 = tuple(landmarks[feature[1]-1])
        point3 = tuple(landmarks[feature[2]-1])

        draw.line([point1, point2], fill=(0, 0, 255, 255), width=int(size*0.9))
        draw.line([point2, point3], fill=(0, 0, 255, 255), width=int(size*0.9))
        
        # Draw the arc
        center = (point2[0], point2[1])  # The center is the point2
        radius = 125
        start_angle = angle_between_points(point2, point1)
        end_angle = angle_between_points(point2, point3)
        
        if end_angle > start_angle and end_angle - start_angle > 180:
            start_angle, end_angle = end_angle, start_angle
        elif start_angle > end_angle and start_angle - end_angle < 180:
            start_angle, end_angle = end_angle, start_angle
            
 
        draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
                  start_angle, end_angle, fill=(0, 255, 0, 255), width=int(size*0.8))
        
    
    # Resize back to original size with Lanczos resampling  
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    if mode == "emotional":
        image.save(f'{emotion}_angle_features.png')
    elif mode == "neutral":
        image.save(f'{emotion}_angle_features_neutral.png')

def plot_features_on_image(image_path, landmarks, emotion,supersample_factor, line_features, angle_features):
    image = Image.open(image_path)
    # Conver to grayscale and then to RGBA
    image = image.convert("L")
    image = image.convert("RGBA")
    width, height = image.size
    im = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    image_line = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    image_angle = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    
    # plot_landmarks(im, emotion, landmarks, width, height)
    plot_line_features(image_line, emotion, landmarks, line_features, width, height)
    # plot_angle_features(image_angle, emotion, landmarks, angle_features, width, height)





supersample_factor = 10

image_paths = {}
landmarks = {}


if mode == "emotional":
    happiness_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\happiness\\S113\\S113_004_00000023.png"
    happiness_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\004\\S113_004_00000023_landmarks.txt", supersample_factor)
elif mode == "neutral":
    happiness_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\happiness\\S113\\S113_004_00000001.png"
    happiness_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\004\\S113_004_00000001_landmarks.txt", supersample_factor)

image_paths["happiness"] = happiness_image_path
landmarks["happiness"] = happiness_landmarks

if mode == "emotional":
    surprise_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\surprise\\S113\\S113_001_00000012.png"
    surprise_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\001\\S113_001_00000012_landmarks.txt", supersample_factor)
elif mode == "neutral":
    surprise_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\surprise\\S113\\S113_001_00000001.png"
    surprise_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\001\\S113_001_00000001_landmarks.txt", supersample_factor)

image_paths["surprise"] = surprise_image_path
landmarks["surprise"] = surprise_landmarks

if mode == "emotional":
    anger_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\anger\\S113\\S113_008_00000023.png"
    anger_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\008\\S113_008_00000023_landmarks.txt", supersample_factor)
elif mode == "neutral":
    anger_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\anger\\S113\\S113_008_00000001.png"
    anger_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S113\\008\\S113_008_00000001_landmarks.txt", supersample_factor)

image_paths["anger"] = anger_image_path
landmarks["anger"] = anger_landmarks

if mode == "neutral":
    sad_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\sadness\\S081\\S081_002_00000001.png"
    sad_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S081\\002\\S081_002_00000001_landmarks.txt", supersample_factor)
elif mode == "emotional":
    sad_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\sadness\\S081\\S081_002_00000024.png"
    sad_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S081\\002\\S081_002_00000024_landmarks.txt", supersample_factor)

image_paths["sadness"] = sad_image_path
landmarks["sadness"] = sad_landmarks

if mode == "emotional":
    fear_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\fear\\S050\\S050_001_00000017.png"
    fear_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S050\\001\\S050_001_00000017_landmarks.txt", supersample_factor)
elif mode == "neutral":
    fear_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\fear\\S050\\S050_001_00000001.png"
    fear_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S050\\001\\S050_001_00000001_landmarks.txt", supersample_factor)

image_paths["fear"] = fear_image_path
landmarks["fear"] = fear_landmarks

if mode == "emotional":
    disgust_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\disgust\\S037\\S037_004_00000066.png"
    disgust_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S037\\004\\S037_004_00000066_landmarks.txt", supersample_factor)
elif mode == "neutral":
    disgust_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\disgust\\S037\\S037_004_00000001.png"
    disgust_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S037\\004\\S037_004_00000001_landmarks.txt", supersample_factor)
    
# if mode == "emotional":
#     disgust_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\disgust\\S010\\S010_005_00000016.png"
#     disgust_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S010\\005\\S010_005_00000016_landmarks.txt", supersample_factor)
# elif mode == "neutral":
#     disgust_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\disgust\\S010\\S010_005_00000001.png"
#     disgust_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S010\\005\\S010_005_00000001_landmarks.txt", supersample_factor)

image_paths["disgust"] = disgust_image_path
landmarks["disgust"] = disgust_landmarks

# Take features as input and plot them on the image

line_features = []
angle_features = []

with open(f'Features/{emotion}.txt', 'r') as file:
    for line in file:
        feature = line.strip().split()
        feature = [int(value) for value in feature[0][2:-1].split(',')]
        if len(feature) == 2:
            line_features.append(feature)
        else:
            angle_features.append(feature)
    print("Feature extracted")

image_path = image_paths[emotion]
landmark = landmarks[emotion]

plot_features_on_image(image_path, landmark, emotion, supersample_factor, line_features, angle_features)