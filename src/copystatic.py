import os
import shutil

def copyFromTo(copy_from, copy_to):
    for filename in os.listdir(copy_from):
        file_path = f"{copy_from}/{filename}"
        copy_path = f"{copy_to}/{filename}"
        if os.path.isdir(file_path):
            os.mkdir(copy_path)
            print(f"New dir -> {copy_path}")
            copyFromTo(file_path,copy_path)
        else:
            shutil.copy(file_path, copy_path)
            print(f"Copy {file_path} -> {copy_path}")