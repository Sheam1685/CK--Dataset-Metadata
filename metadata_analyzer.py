import csv
import json
import pandas as pd

with open('image_metadata.json') as f:
    json_data = json.load(f)

with open('emotion_label_copy.csv', 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Skip the header row
    csv_rows = [row for row in reader]

keys = []
for key, obj in json_data.items():
    keys.append(key)

emotions = []
for row in csv_rows:
    emotion = row[0]
    emotions.append(emotion)

new_csv_rows = []

for i in range(len(emotions)):
    string = keys[i] + "," + emotions[i]
    new_csv_rows.append(string)

# Split each string in the array into name, address, and phone parts
data = {
    "image file name": [],
    "emotion": [],
}

for item in new_csv_rows:
    image_file_name, emotion = item.split(",")
    data["image file name"].append(image_file_name)
    data["emotion"].append(emotion)

# Create a DataFrame from the data dictionary
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_path = "debug_data.csv"
df.to_csv(csv_file_path, index=False)

# Read the CSV file into a DataFrame
df = pd.read_csv('debug_data.csv')

df['image file name'] = df['image file name'].str[:-8]

# Group the data by the 'key' column
grouped = df.groupby('image file name')['emotion'].apply(list)

# Check if all emotions within each group are the same
for image_file_name, emotions in grouped.items():
    unique_emotions = set(emotions)
    if len(unique_emotions) != 1:
        print(f"image: {image_file_name}: Different emotions - {', '.join(str(unique_emotions))}")
        break



with open('image_metadata.json') as f:
    data = json.load(f)

print(f"Number of images: {len(data)}")
    
output = {}

for key, obj in data.items():
    if "ckplus_emotion" in obj:
        subject_id = obj["subject_id"] 
        emotion = obj["ckplus_emotion"]
        if subject_id in output:
            output[subject_id]["emotion"] += ", " + emotion
        else:
            output[subject_id] = {"subject_id": subject_id, "emotion": emotion}
            
with open('subject_metadata.json', 'w') as output_json_file:
    json.dump(list(output.values()), output_json_file, indent=2)

with open('subject_metadata.json') as f:
    data = json.load(f)

output = {}

for obj in data:
    subject_id = obj["subject_id"]
    emotions = obj["emotion"].split(", ")
    for emotion in emotions:
        if emotion not in output:
            output[emotion] = []
        output[emotion].append(subject_id)

# Step 3: Write the emotion_subjects dictionary to a new JSON file
with open('emotion_metadata.json', 'w') as output_json_file:
    json.dump(output, output_json_file, indent=2)
    
with open('emotion_metadata.json', 'r') as json_file:
    data = json.load(json_file)
    
disgust_subjects = set(data.get("disgust", []))
surprise_subjects = set(data.get("surprise", []))
anger_subjects = set(data.get("anger", []))
happiness_subjects = set(data.get("happiness", []))

common_subjects = list(disgust_subjects & surprise_subjects & anger_subjects & happiness_subjects)

print(f"Number of subjects with disgust, surprise, anger, and happiness: {len(common_subjects)}")
print(f"Subjects with all four emotions: {common_subjects}")