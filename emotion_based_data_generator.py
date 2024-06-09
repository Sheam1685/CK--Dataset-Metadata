import os
import shutil
import pandas as pd

# Load CSV file
csv_file_path = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\metadata\\ck_plus.csv'
df = pd.read_csv(csv_file_path, dtype={'subject_id': str, 'session_id': str})

# Step 1: Remove rows where ckplus_labelled is 0
df = df[df['ckplus_labelled'] != 0]

# Step 2: Validate emotion values for each subject_id, session_id pair
for (subject_id, session_id), group in df.groupby(['subject_id', 'session_id']):
    emotions = group['emotion'].unique()
    if len(emotions) > 1:
        raise ValueError(f"Error: Different emotions found for Subject {subject_id}, Session {session_id}")
    
# Step 3: Group by subject_id, session_id, and emotion, keeping only necessary columns
df = df.groupby(['subject_id', 'session_id', 'emotion']).first().reset_index()[['subject_id', 'session_id', 'emotion']]

# print unique emotions
print(df['emotion'].unique())

# remove rows with contempt emotion
df = df[df['emotion'] != 'contempt']


# Step 4: Process images based on count and emotion
for index, row in df.iterrows():
    subject_id = row['subject_id']
    session_id = row['session_id']
    emotion = row['emotion']

    images_directory = f'C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images\\{subject_id}\\{session_id}'
    project_directory = f'C:\\Users\\samia\\Documents\\Thesis\\CK+\\Project_data\\{emotion}'

    # list files with .png extension
    images = [file for file in os.listdir(images_directory) if file.endswith('.png')]
    image_count = len(images)
    half_count = image_count // 2

    count = min(5, half_count)
    
    # Select last count images
    selected_images = images[-count:]

    # Move selected images to project directory
    for image in selected_images:
        image_path = os.path.join(images_directory, image)
        shutil.copy(image_path, project_directory)

    # Move top 2 images to neutral directory
    top2_images = images[:2]
    neutral_directory = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\Project_data\\neutral'
    for image in top2_images:
        image_path = os.path.join(images_directory, image)
        shutil.copy(image_path, neutral_directory)
