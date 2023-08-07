import csv
import json
import pandas as pd

# emotion_label.csv contains the original file inherited from our seniors
# emotion_label_copy.csv contains the proposed bug free file

def map_image_to_emotion():
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
    csv_file_path = "image_emotion_mapping.csv"
    df.to_csv(csv_file_path, index=False)



def check_if_a_session_contains_multiple_emotions():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('image_emotion_mapping.csv')

    df['image file name'] = df['image file name'].str[:-8]

    # Group the data by the 'image file name' column
    grouped = df.groupby('image file name')['emotion'].apply(list)

    # Check if all emotions within each group are the same
    for image_file_name, emotions in grouped.items():
        unique_emotions = set(emotions)
        if len(unique_emotions) != 1:
            print(f"image: {image_file_name}: Different emotions - {', '.join(str(unique_emotions))}")
            break
        


def map_subject_to_its_available_emotions():
    with open('image_metadata.json') as f:
        data = json.load(f)

    # print(f"Number of images: {len(data)}")
        
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



def map_emotions_to_its_subjects():
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

    with open('emotion_metadata.json', 'w') as output_json_file:
        json.dump(output, output_json_file, indent=2)
    
    
def get_subjects_with_all_four_emotions():
    with open('emotion_metadata.json', 'r') as json_file:
        data = json.load(json_file)
        
    disgust_subjects = set(data.get("disgust", []))
    surprise_subjects = set(data.get("surprise", []))
    anger_subjects = set(data.get("anger", []))
    happiness_subjects = set(data.get("happiness", []))

    common_subjects = list(disgust_subjects & surprise_subjects & anger_subjects & happiness_subjects)

    print(f"Number of subjects with disgust, surprise, anger, and happiness: {len(common_subjects)}")
    print(f"Subjects with all four emotions: {common_subjects}")
    

def check_label_integrity():
    emotion_decoder = {
        "neutral": 0,
        "anger": 1,
        "contempt": 2,
        "disgust": 3,
        "fear": 4,
        "happiness": 5,
        "sadness": 6,
        "surprise": 7,
    }
    
    with open('image_metadata.json') as f:
        data = json.load(f)
        
    with open("image_emotion_mapping.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row
        csv_rows = [row for row in reader]
    
    emotion_labels = []
    for row in csv_rows:
        emotion = row[1]
        emotion_labels.append(emotion)
    
    index = 0
    for key, obj in data.items():
        csv_emotion = emotion_labels[index]
        csv_emotion = int(csv_emotion)
        # print(csv_emotion)
        index += 1
        if "ckplus_emotion" in obj:
            json_emotion = obj["ckplus_emotion"]
            json_emotion = emotion_decoder[json_emotion]
            # print(json_emotion)
            if csv_emotion != json_emotion:
                print(f"Image: {key}, CSV emotion: {csv_emotion}, JSON emotion: {json_emotion}")
            
    
        
    
    

map_image_to_emotion()
check_if_a_session_contains_multiple_emotions()
map_subject_to_its_available_emotions()
map_emotions_to_its_subjects()
get_subjects_with_all_four_emotions()
check_label_integrity()