import json
import pandas as pd
import numpy as np

# Load JSON data
with open('modified_image_metadata.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize lists to store data
rows = []
columns = ["subject_id", "session_id", "image_id", "emotion"] + [f"landmark_{i}" for i in range(1, 69)]

# Iterate through JSON data
for key, value in data.items():
    row = [value["subject_id"], value["session_id"], value["image_id"], value.get("labelled_emotion", value.get("ckplus_emotion", ""))]
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

# Save DataFrame to CSV
df.to_csv('ck_plus.csv', index=False)