import json

json_file_path = 'newdataset_metadata.json'
with open(json_file_path, 'r') as f:
    json_data = json.load(f)

# Dictionary to store subject IDs and their counts
subject_id_counts = {}

# Iterate through the keys and count subject IDs
for key in json_data.keys():
    subject_id = key.split('_')[0]  # Extract subject ID from the key
    if subject_id in subject_id_counts:
        subject_id_counts[subject_id] += 1
    else:
        subject_id_counts[subject_id] = 1

# Find subject IDs that appear at least twice
subject_ids_appearing_twice = [subject_id for subject_id, count in subject_id_counts.items() if count >= 2]

print("Subject IDs appearing at least twice:", subject_ids_appearing_twice)
