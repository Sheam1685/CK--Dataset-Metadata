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



def generate_collage(emotion):
    emotion_dir = os.path.join('C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet', emotion)
    
    # this line will take random 5 subjects
    # sub_dirs = os.listdir(emotion_dir)
    # sub_dirs = random.sample(sub_dirs, min(5, len(sub_dirs)))  # Randomly select 5 subdirectories or less
    # this line is specifically for surprise emotion. Detected by us to detect feature of surprise
    sub_dirs = ['S010', 'S042', 'S026', 'S136', 'S037']
    print(sub_dirs)

    landmark_dir = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\Landmarks'
    max_width = 0
    total_height = 0
    subject_images = []

    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(emotion_dir, sub_dir)
        images = os.listdir(sub_dir_path)
        images.sort()  # Ensure images are in order
        images = images[-5:]  # Take the last 5 images

        subject_images_per_dir = []
        current_height = 0;
        
        for image in images:
            image_path = os.path.join(sub_dir_path, image)
            img = Image.open(image_path)
            
            # landmark files are at different locations. so session needed to access the right file  
            session = image.split('_')[1]
            landmark_path = os.path.join(landmark_dir, sub_dir, session, image.replace('.png', '_landmarks.txt'))
            landmarks = read_landmarks(landmark_path)
            plot_landmarks_on_image(img, landmarks)
            
            subject_images_per_dir.append(img)

            max_width = max(max_width, img.width)
            current_height += img.height
        
        total_height = max(total_height, current_height)
        subject_images.append(subject_images_per_dir)

    collage = Image.new('RGB', (max_width * len(sub_dirs), total_height), color=(255, 255, 255))

    y_offset = 0
    x_offset = 0
    for sub_images in subject_images:        
        for img in sub_images:
            collage.paste(img, (x_offset, y_offset))
            y_offset += img.height
        y_offset = 0  # Reset y_offset for next column
        x_offset += max_width  # Move to next column

    collage.show()  # Display the generated collage
    # save the image as emotionCollage.png
    collage.save(emotion+'Collage.png')

# Replace 'disgust' with the desired emotion
generate_collage('anger')
