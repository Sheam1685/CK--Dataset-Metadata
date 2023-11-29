import os

# count the number of subdirectories in given directory. and also print the num of files in each subdirectory's directory
directory = "C:\\Users\\samia\\Documents\\Thesis\\CK+\\surpriseDataset"

count = 0

for filename in os.listdir(directory):
    count += 1
    print(filename, len(os.listdir(os.path.join(directory, filename, "surprise"))))
    
print(count)