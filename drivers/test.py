import os

for root, sub_folders, files in os.walk('.'):
    print(root, sub_folders, files)
)
