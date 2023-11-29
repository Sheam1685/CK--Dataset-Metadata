import json
import shutil
import os


# Read the original JSON file
with open('modified_image_metadata.json', 'r') as f:
    data = json.load(f)

# Initialize a dictionary to store selected data
selected_data = {}

# Initialize dictionaries to keep track of images per subject-session combination
image_counter_high = {}
image_counter_low = {}

# Iterate through each object in the original data
for key, value in data.items():
    # Check if the object has 'ckplus_emotion' or 'labelled_emotion' as "happiness"
    if value.get('ckplus_emotion') == 'happiness' or value.get('labelled_emotion') == 'happiness':
        subject_id = value['subject_id']
        session_id = value['session_id']
        image_id = int(value['image_id'])

        # Create a unique key for the subject-session combination
        combo_key = f"{subject_id}_{session_id}"

        # Update the image_counter dictionaries to keep track of the image_ids
        if combo_key not in image_counter_high:
            image_counter_high[combo_key] = []
        if combo_key not in image_counter_low:
            image_counter_low[combo_key] = []
        image_counter_high[combo_key].append(image_id)
        image_counter_low[combo_key].append(image_id)

# Iterate through the image_counter dictionaries to select the top 5 and bottom 3 image_ids
for combo_key in image_counter_high.keys():
    top_image_ids = sorted(image_counter_high[combo_key], reverse=True)[:5]
    low_image_ids = sorted(image_counter_low[combo_key])[:3]

    # Collect the selected data
    selected_data[combo_key] = {
        "happy_images": [
            data[f"{combo_key}_{str(image_id).zfill(8)}"] for image_id in top_image_ids
        ],
        "neutral_images": [
            data[f"{combo_key}_{str(image_id).zfill(8)}"] for image_id in low_image_ids
        ]
    }

# Write the selected data to a new JSON file
with open('newdataset_metadata.json', 'w') as f:
    json.dump(selected_data, f, indent=2)
    
    
# formulate the new dataset

# Path to the input JSON file
json_file_path = 'newdataset_metadata.json'

# Base directory for the new dataset
base_output_dir = 'C:\\Users\\samia\\Documents\\Thesis\\CK+\\new-Data'

# Read the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Iterate through each subject-session combination
for combo_key, images_data in data.items():
    subject_id = combo_key.split('_')[0]

    # Create subject's directory in the base output directory
    subject_output_dir = os.path.join(base_output_dir, subject_id)
    os.makedirs(subject_output_dir, exist_ok=True)

    # Iterate through each type of image (happy and neutral)
    for image_type, image_list in images_data.items():
        for image_data in image_list:
            image_path = image_data['image_path']
            image_filename = os.path.basename(image_path)
            image_emotion = image_data.get('ckplus_emotion', image_data.get('labelled_emotion'))

            source_image_path = os.path.join("C:\\Users\\samia\\Documents\\Thesis\\CK+", image_path)

            if image_type == 'happy_images':
                image_output_dir = os.path.join(subject_output_dir, 'happy')
            else:
                image_output_dir = os.path.join(subject_output_dir, 'neutral')

            os.makedirs(image_output_dir, exist_ok=True)
            destination_image_path = os.path.join(image_output_dir, image_filename)

            # Copy the image to the appropriate subdirectory
            shutil.copy(source_image_path, destination_image_path)

print("Image copying completed.")


