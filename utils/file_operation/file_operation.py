import os
from datetime import datetime


def check_last_modified_date(filepath):
    if os.path.exists(filepath):
        modified_time = os.path.getmtime(filepath)
        last_modified_date = datetime.fromtimestamp(modified_time)
        return last_modified_date
    else:
        return None


def list_files(folder_path, endswith=None, except_folder: str | list[str] = "qz"):
    silk_files = []

    for root, dirs, files in os.walk(folder_path):
        if root.split("/")[-1] in except_folder:
            continue
        for file in files:
            if endswith and os.path.splitext(file)[1] == endswith:
                relative_path = os.path.join(root, file).replace(folder_path, "")
                silk_files.append(relative_path)
            else:
                relative_path = os.path.join(root, file).replace(folder_path, "")
                silk_files.append(relative_path)

    return silk_files


if __name__ == "__main__":

    pass
