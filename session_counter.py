import csv

# Read the original CSV file
with open('emotion_label.csv', 'r') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Skip the header row
    rows = [row for row in reader]

# Create a new list to store the collapsed rows
collapsed_rows = []
prev_emotion = None

# Loop through the rows and collapse consecutive rows with the same emotion value
for row in rows:
    emotion = row[0]  # Assuming the emotion value is in the first column
    if emotion != prev_emotion:
        collapsed_rows.append(row)
        prev_emotion = emotion

# Write the collapsed rows to a new CSV file
with open('session_metadata.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)  # Write the header
    writer.writerows(collapsed_rows)
