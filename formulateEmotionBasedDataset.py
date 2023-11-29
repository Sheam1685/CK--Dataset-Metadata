import os
import shutil
import json

# Load your JSON data
with open('modified_image_metadata.json') as json_file:
    data = json.load(json_file)

# Create folders for each emotion
emotions = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
output_dir = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\EmotionBasedDataSet'

# Create emotion folders if they don't exist
for emotion in emotions:
    os.makedirs(os.path.join(output_dir, emotion), exist_ok=True)

# Organize images into respective emotion folders
for key, value in data.items():
    emotion = value.get('labelled_emotion') or value.get('ckplus_emotion')
    if emotion in emotions:
        subject_id = value['subject_id']
        image_path = value['image_path']
        # append ck source directory with image path
        image_path = os.path.join('C:\\Users\\samia\\Documents\\Thesis\\CK+', image_path)
        output_path = os.path.join(output_dir, emotion, subject_id)       
        os.makedirs(output_path, exist_ok=True)
        shutil.copy(image_path, os.path.join(output_path, os.path.basename(image_path)))
