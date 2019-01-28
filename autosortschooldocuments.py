from pathlib import Path
import shutil
import os
import sys


class Subject:
    token = ""
    name = ""
    dropbox_path = ""
    local_path = ""

    def __init__(self, token, name, dropbox_path, local_path):
        self.token = token
        self.name = name
        self.dropbox_path = dropbox_path
        self.local_path = local_path


subjects = []
dropped_files = []


# Initialize subjects
subjects.append(Subject("m", "Mathematik",
                        "F:/Dropbox/Dropbox/8B/Mathe", "E:/Albertgasse/8B/Mathe"))
subjects.append(Subject("e", "Englisch",
                        "F:/Dropbox/Dropbox/8B/Englisch", "E:/Albertgasse/8B/Englisch"))
subjects.append(Subject("d", "Deutsch",
                        "F:/Dropbox/Dropbox/8B/Deutsch", "E:/Albertgasse/8B/Deutsch"))
subjects.append(Subject("acg", "ACG",
                        "F:/Dropbox/Dropbox/8B/ACG", "E:/Albertgasse/8B/ACG"))
subjects.append(Subject("be", "BE",
                        "F:/Dropbox/Dropbox/8B/BE", "E:/Albertgasse/8B/BE"))
subjects.append(Subject("bio", "Bio",
                        "F:/Dropbox/Dropbox/8B/Bio", "E:/Albertgasse/8B/Bio"))
subjects.append(Subject("c", "Chemie",
                        "F:/Dropbox/Dropbox/8B/Chemie", "E:/Albertgasse/8B/Chemie"))
subjects.append(Subject("g", "Geschichte",
                        "F:/Dropbox/Dropbox/8B/Geschichte", "E:/Albertgasse/8B/Geschichte"))
subjects.append(Subject("s", "Spanisch",
                        "F:/Dropbox/Dropbox/8B/Spanisch", "E:/Albertgasse/8B/Spanisch"))
subjects.append(Subject("infz", "INFZ",
                        "F:/Dropbox/Dropbox/8B/INFZ", "E:/Albertgasse/8B/INFZ"))
subjects.append(Subject("geo", "Geo",
                        "F:/Dropbox/Dropbox/8B/Geo", "E:/Albertgasse/8B/Geo"))

# helper functions


def yes_no(question):
    while True:
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def move_file(file, path):
    filename, file_extension = os.path.splitext(
        os.path.basename(str(file)))

    new_filename = filename

    dest_path = os.path.join(str(path), str(filename)) + str(file_extension)

    if Path(dest_path).is_file() == True:
        if yes_no("File already exists in " + path + ". Overwrite?"):
            shutil.move(str(file), dest_path)
        else:
            i = 1
            dest_path_new_filename = os.path.join(
                str(path), new_filename) + str(file_extension)
            while Path(dest_path_new_filename).is_file() == True:
                new_filename = str(filename) + "(" + str(i) + ")"
                dest_path_new_filename = os.path.join(str(path),
                                                      new_filename) + str(file_extension)
                i += 1
            shutil.move(str(file), dest_path_new_filename)
    else:
        shutil.move(str(file), dest_path)

    print("Moved file")

# START


def start():
    for arg in sys.argv[1:]:
        if Path(arg).is_file() == True:
            dropped_files.append(Path(arg))

    if len(dropped_files) > 0:
        for s in subjects:
            print(s.name + ": " + s.token + " ")
        print("")
        for f in dropped_files:
            sort_document(f)
    else:
        print("No files found.")
    input("Press any key to exit.")


def sort_document(dropped_file):
    print("File path: " + str(dropped_file))

    subject_input = input("Subject: ")

    path = ""

    for s in subjects:
        if s.token == subject_input.lower():
            if yes_no("Save to Dropbox?") == True:
                path = s.dropbox_path
            else:
                path = s.local_path

            if os.path.exists(path):
                move_file(dropped_file, path)
            else:
                if yes_no("Path does not exist. Create?") == True:
                    os.makedirs(path)
                    move_file(dropped_file, path)
                else:
                    exit

    input("Press any key to continue.")


if __name__ == "__main__":
    start()
