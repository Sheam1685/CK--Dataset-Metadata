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
    return 360 - math.degrees(math.atan2(point2[1] - point1[1], point2[0] - point1[0]))

def plot_line_features(image, emotion, landmarks, line_features, width, height):
    size = 20
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    for i in range(len(line_features)):
        feature = line_features[i]
        point1 = tuple(landmarks[feature[0]-1])
        point2 = tuple(landmarks[feature[1]-1])
        draw.line([point1, point2], fill=(0, 255, 0, 255), width=int(size*0.8))
    
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    image.save(f'{emotion}_line_features.png')
    
def plot_angle_features(image, emotion, landmarks, angle_features, width, height):
    size = 20
    draw = ImageDraw.Draw(image)
    
    for landmark in landmarks:
        draw.ellipse([landmark[0] - size, landmark[1] - size, landmark[0] + size, landmark[1] + size], fill=(255, 0, 0, 255))
    
    for i in range(len(angle_features)):
        feature = angle_features[i]
        point1 = tuple(landmarks[feature[0]-1])
        point2 = tuple(landmarks[feature[1]-1])
        point3 = tuple(landmarks[feature[2]-1])
        draw.line([point1, point2], fill=(0, 0, 255, 255), width=int(size*0.8))
        draw.line([point2, point3], fill=(0, 0, 255, 255), width=int(size*0.8))
        
        # Draw the arc
        # center = (point2[0], point2[1])  # The center is the point2
        # radius = 100
        # start_angle = angle_between_points(point2, point1)
        # end_angle = angle_between_points(point2, point3)
        
        # if start_angle > end_angle:
        #     start_angle, end_angle = end_angle, start_angle
            
        # draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        #           start_angle, end_angle, fill=(0, 0, 255, 255), width=10)
        
        # Resize back to original size with Lanczos resampling
        
    image = image.resize((width, height), resample=Image.LANCZOS)
    image.show()
    image.save(f'{emotion}_angle_features.png')

def plot_features_on_image(image_path, landmarks, emotion,supersample_factor, line_features, angle_features):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    width, height = image.size
    image_line = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    image_angle = image.resize((width * supersample_factor, height * supersample_factor), resample=Image.LANCZOS)
    
    plot_line_features(image_line, emotion, landmarks, line_features, width, height)
    plot_angle_features(image_angle, emotion, landmarks, angle_features, width, height)

supersample_factor = 10
surprise_image_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet\\surprise\\S050\\S050_002_00000018.png"
surprise_landmarks = read_landmarks("C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks\\S050\\002\\S050_002_00000018_landmarks.txt", supersample_factor)


# Take features as input and plot them on the image

line_features = []
angle_features = []

with open("surprise.txt", 'r') as file:
    for line in file:
        feature = line.strip().split()
        feature = [int(value) for value in feature[0][2:-1].split(',')]
        if len(feature) == 2:
            line_features.append(feature)
        else:
            angle_features.append(feature)

plot_features_on_image(surprise_image_path, surprise_landmarks, "surprise",supersample_factor, line_features, angle_features)