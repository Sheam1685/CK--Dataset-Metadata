import json
import os

root_dir = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\cohn-kanade-images"

session_count = 0

for path, dirnames, _ in os.walk(root_dir):
    # print(path, dirnames)
    if path != root_dir: # Skip the root directory folder count.
        session_count += len(dirnames)
        
        for sub_path, sub_dir, _ in os.walk(path):
            if sub_path != path:
                file_count = 0
                for item in os.listdir(sub_path):
                    item_path = os.path.join(sub_path, item)
                    if os.path.isfile(item_path):
                        file_count += 1
                if file_count == 0:
                    print(f"Empty folder: {sub_path}")
        
print(f"Number of sessions: {session_count}")

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