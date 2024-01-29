import os
import json
import shutil
import random

# Path to the main folder containing subject IDs
main_folder_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images"
dest_folder_path = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\SubjectBasedDataCopy"

json_file = "modified_image_metadata.json"
with open(json_file) as json_file:
      data = json.load(json_file)

# list to contain bad folders
bad_folders = []

# Emotions to be considered
emotions = ["anger", "happiness", "sadness", "surprise", "neutral"]

# Walk through all folders and subfolders
for root, dirs, files in os.walk(main_folder_path):
    session = os.path.basename(os.path.normpath(root))
    subject_id = os.path.basename(os.path.normpath(os.path.dirname(root)))
    # keep only the files with .jpg or .png extension or .jpeg
    files = [f for f in files if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]
    if len(files) <= 0:
      continue
    
    # take the last 50% images and store into files. Save the rest into neutral
    temp = files
    files = files[-int(len(files)/2):]
    neutral = temp[:-int(len(temp)/2)]
     
    # Check if all the files have the same emotion
    emotion = ""
    object = data[files[0][:-4]]
    if 'labelled_emotion' in object:
      emotion = object['labelled_emotion']
    elif 'ckplus_emotion' in object:
      emotion = object['ckplus_emotion']
    
    for file in files:
      object = data[file[:-4]]
      if 'labelled_emotion' in object:
        if emotion != object['labelled_emotion']:
          print("Error: Emotion mismatch for subject", subject_id, "session", session, "file", file, "emotion", emotion, "labelled_emotion", object['labelled_emotion'])
      elif 'ckplus_emotion' in object:
        if emotion != object['ckplus_emotion']:
          print("Error: Emotion mismatch for subject", subject_id, "session", session, "file", file, "emotion", emotion, "ckplus_emotion", object['ckplus_emotion'])
    
    if emotion not in emotions:
      # print("Error: Emotion not in emotions list for subject", subject_id, "session", session, "emotion", emotion)
      continue
            
    # copy the last 50% images to proper folder
    
    # Create subject directory if it doesn't exist
    if not os.path.exists(os.path.join(dest_folder_path, subject_id)):
        os.makedirs(os.path.join(dest_folder_path, subject_id))
        for e in emotions:
          os.makedirs(os.path.join(dest_folder_path, subject_id, e))
    # check if the emotion folder is not empty. if not empty then there is a conflict. Manual intervention is required
    elif len(os.listdir(os.path.join(dest_folder_path, subject_id, emotion))) > 0:
      print(subject_id+emotion)
        
    for file in files:
        image_path = os.path.join(root, file)
        # Copy the image to the destination folder
        shutil.copy(image_path, os.path.join(dest_folder_path, subject_id, emotion))
    
    # copy the rest of the images to neutral folder
    for file in neutral:
        image_path = os.path.join(root, file)
        # Copy the image to the destination folder
        shutil.copy(image_path, os.path.join(dest_folder_path, subject_id, "neutral"))
        

# neutral folders will have a lot of images. So lets take at most 10 randomly.
# for root, dirs, files in os.walk(dest_folder_path):
#     emotion = os.path.basename(os.path.normpath(root))
#     if emotion != "neutral":
#       continue
#     subject_id = os.path.basename(os.path.normpath(os.path.dirname(root)))
#     # check if there are 0 images in neutral folder.
#     if len(files) <= 0:
#       print("Error: No images in neutral folder for subject", subject_id)
#       continue
    
#     if len(files) > 10:
#       # take 10 random images and delete rest
#       files = random.sample(files, 10)
#       for file in os.listdir(root):
#         if file not in files:
#           os.remove(os.path.join(root, file))
      