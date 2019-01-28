import sys
import os
import shutil
import pickle
import atexit
from pathlib import Path
from terminaltables import AsciiTable


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

savefilename = "autosortschooldocuments_subjects.pkl"

predefined_subjects = []
# Initialize subjects
predefined_subjects.append(Subject("m", "Mathematik",
                                   "F:/Dropbox/Dropbox/8B/Mathe", "E:/Albertgasse/8B/Mathe"))
predefined_subjects.append(Subject("e", "Englisch",
                                   "F:/Dropbox/Dropbox/8B/Englisch", "E:/Albertgasse/8B/Englisch"))
predefined_subjects.append(Subject("d", "Deutsch",
                                   "F:/Dropbox/Dropbox/8B/Deutsch", "E:/Albertgasse/8B/Deutsch"))
predefined_subjects.append(Subject("acg", "ACG",
                                   "F:/Dropbox/Dropbox/8B/ACG", "E:/Albertgasse/8B/ACG"))
predefined_subjects.append(Subject("be", "BE",
                                   "F:/Dropbox/Dropbox/8B/BE", "E:/Albertgasse/8B/BE"))
predefined_subjects.append(Subject("bio", "Bio",
                                   "F:/Dropbox/Dropbox/8B/Bio", "E:/Albertgasse/8B/Bio"))
predefined_subjects.append(Subject("c", "Chemie",
                                   "F:/Dropbox/Dropbox/8B/Chemie", "E:/Albertgasse/8B/Chemie"))
predefined_subjects.append(Subject("g", "Geschichte",
                                   "F:/Dropbox/Dropbox/8B/Geschichte", "E:/Albertgasse/8B/Geschichte"))
predefined_subjects.append(Subject("s", "Spanisch",
                                   "F:/Dropbox/Dropbox/8B/Spanisch", "E:/Albertgasse/8B/Spanisch"))
predefined_subjects.append(Subject("infz", "INFZ",
                                   "F:/Dropbox/Dropbox/8B/INFZ", "E:/Albertgasse/8B/INFZ"))
predefined_subjects.append(Subject("geo", "Geo",
                                   "F:/Dropbox/Dropbox/8B/Geo", "E:/Albertgasse/8B/Geo"))


# helper functions


def save_object():
    global subjects
    with open(savefilename, "wb") as output:
        pickle.dump(subjects, output, pickle.HIGHEST_PROTOCOL)


def open_object():
    global subjects
    if Path(savefilename).is_file() == True:
        with open(savefilename, "rb") as input:
            obj = pickle.load(input)
            return obj
    else:
        print("Could not find " + savefilename + ". Using build in subjects.")
        subjects = predefined_subjects
        save_object()
        return subjects


def yes_no(question):
    while True:
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def selectable_options(options):
    for i, element in enumerate(options):
        print("{}) {}".format(i + 1, element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
    except:
        pass
    return None


def show_subjects():
    global subjects
    table_data = [
        ["Token", "Name", "Dropbox Path", "Local Path"]
    ]
    for s in subjects:
        table_data.append([str(s.token), str(s.name), str(
            s.dropbox_path), str(s.local_path)])

    table = AsciiTable(table_data)
    print(table.table)


def move_file(file, path):
    global subjects
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
    global subjects
    subjects = open_object()
    atexit.register(on_exit)

    for arg in sys.argv[1:]:
        if Path(arg).is_file() == True:
            dropped_files.append(Path(arg))

    if len(dropped_files) > 0:
        show_subjects()
        print("")
        for f in dropped_files:
            sort_document(f)
    else:
        print("No files found.")
        if selectable_options(["Settings", "Exit"]) == 1:
            settings()
        else:
            exit


def sort_document(dropped_file):
    global subjects
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


def settings():
    global subjects
    os.system("cls")
    print("Settings:")
    show_subjects()
    menupoints = ["Delete", "Update", "Add", "Exit"]
    selection = selectable_options(menupoints)
    if selection == 1:
        settings_window(menupoints[selection - 1], delete_insert)
    elif selection == 2:
        settings_window(menupoints[selection - 1], update_insert)
    elif selection == 3:
        add(menupoints[selection - 1])
    else:
        sys.exit(0)
    settings()


def delete_insert(s):
    global subjects
    subjects.remove(s)
    print("")
    print("Deleted")
    print("New List")
    show_subjects()


def update_insert(s):
    global subjects
    dropbox = input("Dropbox Path: ")
    if dropbox == "*":
        dropbox = s.dropbox_path
    local = input("Local Path: ")
    if local == "*":
        local = s.local_path
    s.dropbox_path = dropbox
    s.local_path = local
    print("")
    print("Updated")
    print("New List")
    show_subjects()


def add(name):
    global subjects
    os.system("cls")
    print(str(name))
    show_subjects()
    print("")
    token = input("Token: ").strip()
    if len(token) <= 0:
        print("Token is null")
        if yes_no("Return to settings?") == True:
            settings()
        else:
            add(name)
    for s in subjects:
        if s.token == token:
            print("Token already exists.")
            if yes_no("Want to delete the already existing subject?") == True:
                delete_insert(s)
            else:
                add(name)
            break
    else:
        subject_name = input("Name: ").strip()
        dropbox_path = input("Dropbox Path: ").strip()
        local_path = input("Local Path: ").strip()
        subjects.append(Subject(token, subject_name, dropbox_path, local_path))
    print("")
    print("Added")
    print("New List")
    show_subjects()


def settings_window(name, func):
    global subjects
    os.system("cls")
    print(str(name))
    show_subjects()
    token = input("Subject Token: ")
    for s in subjects:
        if s.token == token:
            func(s)
            input()
            break
    else:
        print("Token could not be found.")
        if yes_no("Return to settings?") == True:
            settings()
        else:
            settings_window(name, func)


def on_exit():
    global subjects
    save_object()


if __name__ == "__main__":
    start()
