import json
import pandas as pd
import numpy as np

# Load JSON data
with open('modified_image_metadata.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize lists to store data
rows = []
columns = ["subject_id", "session_id", "image_id", "emotion","ckplus_labelled"] + [f"landmark_{i}" for i in range(1, 69)]

# Iterate through JSON data
for key, value in data.items():
    row = [value["subject_id"], value["session_id"], value["image_id"], value.get("labelled_emotion", value.get("ckplus_emotion", "")), 1 if "ckplus_emotion" in value else 0]
    landmark_file_path = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\' + value["image_path"].replace("cohn-kanade-images", "Landmarks").replace(".png", "_landmarks.txt")

    try:
      
        landmarks = []
        with open(landmark_file_path, 'r') as file:
            for line in file:
                coordinates = line.strip().split()
                if len(coordinates) == 2:
                    x, y = float(coordinates[0]), float(coordinates[1])
                    row.append(str(x) + ' ' + str(y))

    except FileNotFoundError:
      
        print(f"Landmark file not found: {landmark_file_path}")
        
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows, columns=columns)

# Convert 'ckplus_labelled' column to integer
df['ckplus_labelled'] = df['ckplus_labelled'].astype(int)

# Set 'ckplus_labelled' to 1 for rows with the same 'subject_id' and 'session_id' if any row has 'ckplus_labelled' as 1
df['ckplus_labelled'] = df.groupby(['subject_id', 'session_id'])['ckplus_labelled'].transform('max')

# Save DataFrame to CSV
df.to_csv('ck_plus.csv', index=False)

# For each subject_id, session_id pair, if any one of the rows has ckplus_labelled as 1, then set all the rows with the same subject_id, session_id pair to 1
# This is because if any one of the images in a session is labelled, then all the images in that session are labelled