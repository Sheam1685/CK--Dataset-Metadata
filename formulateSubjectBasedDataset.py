import os
import json
import shutil
from collections import defaultdict

# Load your JSON data
with open('modified_image_metadata.json') as json_file:
    data = json.load(json_file)

# Function to organize images by emotion for each subject
def organize_emotion_images(data, emotion):
    
    image_counts = defaultdict(int)
    
    for image_key, image_info in data.items():
        subject_id = image_info.get("subject_id", "")
        labelled_emotion = image_info.get("labelled_emotion", "")
        ckplus_emotion = image_info.get("ckplus_emotion", "")
        image_path = image_info.get("image_path", "")
        # append ck source directory with image path
        image_path = os.path.join('C:\\Users\\samia\\Documents\\Thesis\\CK+', image_path)

        # Check if the image has required emotion
        if labelled_emotion == emotion or ckplus_emotion == emotion:
            subject_dir = os.path.join("C:\\Users\\samia\\Documents\\Thesis\\CK+",emotion, subject_id)
            emotion_dir = os.path.join(subject_dir, emotion)

            # Create subject directory if it doesn't exist
            if not os.path.exists(subject_dir):
                os.makedirs(subject_dir)

            # Create emotion directory if it doesn't exist
            if not os.path.exists(emotion_dir):
                os.makedirs(emotion_dir)
                
            # Take the last 5 images
            dir = os.path.dirname(image_path)           
            images = os.listdir(dir)           
            if image_key+".png" in images[-5:]:
                shutil.copy(image_path, emotion_dir)
                image_counts[subject_id] += 1
    
    for subject_id, count in image_counts.items():
      # if count is not equal to 5 alert me
      if count != 5:
        print(f"Copied {count} images for subject {subject_id}")

# Call the function to organize emotion images
organize_emotion_images(data, "happiness")