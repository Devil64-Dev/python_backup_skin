import os
import shutil
# Program crate by Devil64-Dev
# E-mail: devil64dev@gmail.com
full_path = paths = ""  # global variable for save full path for any file


# this function help to get a valid path for skin_folder
def get_skin_folder():
    while True:
        # get skin_path by user
        # skin_path is a dir or path to folder that contain mod skin files
        skin_path = input("  Skin folder: ")
        if os.path.exists(skin_path):  # exist this path
            # is dir or file
            if os.path.isdir(skin_path):
                # is valid path because contain Art and UI folder or anyone of them.
                if "Art" in os.listdir(skin_path) or "UI" in os.listdir(skin_path):
                    print("  Folder is valid...")  # toast
                    break
                # invalid path because not contain anyone of required folder
                else:
                    print("  ERROR: Folder exists but not is valid")
                    print("  Try again...")
            # not is valid because is a file not a dir
            else:
                print("  ERROR: Skin folder must be a directory not a file")
                print("  Try again")
        # folder not exist
        else:
            print("  ERROR: Folder no exist")
            print("  Try again...")
    return skin_path  # return verified path to skin_folder


# this function get and verify output folder for backup
def set_output_skin_folder():
    skin_path = ""  # contain skin output folder name
    while True:
        # get skin path by user input
        user_skin_path = input("  Output skin folder:")
        # already exists path
        if os.path.exists(user_skin_path):
            # folder is empty
            if len(os.listdir(user_skin_path)) <= 0:
                print(" Folder valid...")
                break
            else:
                # show operations to use by user
                print("\n  The folder already exist what you what to do: ")
                while True:
                    print("    1. Overwrite files")
                    print("    2. Remove files")
                    print("    3. Use other folder")
                    user_input = input("  Your option: ")  # option
                    # all done just sets var skin_path
                    if user_input == "1":
                        skin_path = user_skin_path
                        break
                    # path need be clear
                    elif user_input == "2":
                        old_path = os.getcwd()  # save old work directory
                        os.chdir(user_skin_path)  # change to new work directory
                        print("  Cleaning folder...")
                        # delete all files in this dir
                        for i in os.listdir():
                            if os.path.isdir(i):
                                shutil.rmtree(i)  # recursive remove
                            else:
                                os.remove(i)  # file remove
                        print("  Folder now clear.")  # toast
                        os.chdir(old_path)  # return to old work directory
                        skin_path = user_skin_path  # set skin_path
                        break
                    # user need again input new skin_folder
                    elif user_input == "3":
                        print("")
                        break
                    # option match not found try again
                    else:
                        print("  ERROR: Unknown option\n")
                break
        # folder not exists thus make it
        else:
            os.mkdir(user_skin_path)  # make folder
            skin_path = user_skin_path  # set skin_path
            break
    return skin_path  # len value can be 0


# this function get all full paths for backup files
def get_backup_paths(mod_skin_path):
    current_work_path = os.getcwd()
    os.chdir(mod_skin_path)  # change work directory to skin folder
    old_work_path = os.getcwd()  # save current work directory
    # list with full backup paths
    # note: all paths start in Art, UI or other but not contain skin folder
    back_path = []
    # get file paths for all directories as Art, UI etc.
    for p in os.listdir():
        get_recursive_path(p)  # call function that return a full path without files in Art/* etc...
        global full_path  # global variable that contain current work in path
        back_path.append(full_path)  # add complete path to list
        full_path = ""  # restore full path to none o 0 len
        os.chdir(old_work_path)  # change work directory to skin_folder
    os.chdir(current_work_path)  # when ends change work directory to script call dir
    return back_path  # return list of path to search


# this function call return full path of any backup file, each item start in Art or similar path
def get_backup_file_path(skin_folder):
    global paths
    paths = get_backup_paths(skin_folder)  # get backup paths
    current_work_directory = os.getcwd()  # save script call directory
    # when get_backup_paths is called the directory is change again to script call directory
    os.chdir(skin_folder)  # change work directory to skin_folder
    backup_files = []  # list that contain full paths to files staring with Art, or others

    # get paths in backup path variable > paths
    for file in paths:
        # get items for backup list
        for item2 in os.listdir(file):
            backup_files.append(file+item2)  # add items to backup_files
    os.chdir(current_work_directory)  # change directory to call script directory
    return backup_files  # return list with all backup files


# this function get only dirs in skin_folder recursively
def get_recursive_path(path):
    os.chdir(path)  # change work directory to path
    global full_path  # get global variable for paths
    full_path += path + "/"  # add folder to path
    if len(os.listdir()) >= 1:
        if os.path.isdir(os.listdir()[0]):
            get_recursive_path(os.listdir()[0])


# get backup files and save it
def get_ml_assets():
    while True:
        ml_assets_folder = input("    Input assets folder for Mobile Legends: ")
        if os.path.exists(ml_assets_folder):
            print("  Checking folder...")
            old_directory = os.getcwd()
            os.chdir(ml_assets_folder)
            bool_valid = False
            for item in paths:
                if os.path.exists(item):
                    print("  Found: {}".format(item))
                    bool_valid = True
                else:
                    print("  Not fount: {}".format(item))
                    bool_valid = False
            os.chdir(old_directory)
            if bool_valid:
                print("  Folder correct.")
                break
            else:
                print("  Folder exist but no contain necessary files.")
                print("  Try again...")
        else:
            print("  Folder not exists.\n  Try again...")

    return ml_assets_folder


def backup():
    skin_folder = get_skin_folder()  # get skin folder
    backup_files = get_backup_file_path(skin_folder)
    ml_assets = get_ml_assets()
    backup_folder = set_output_skin_folder()
    # make need folders
    old_dir = os.getcwd()
    os.chdir(backup_folder)
    print("  Creating folders...")
    for item in paths:
        print("  Created: {}".format(item))
        os.makedirs(item)
    print("  ok.")
    backup_folder = os.getcwd()  # absolute path to backup folder
    # now copy files
    os.chdir(old_dir)
    os.chdir(ml_assets)
    count = 0
    for item in backup_files:
        if not os.path.exists(item):
            print("  Skipping: {}".format(item))
        else:
            shutil.copy(item, backup_folder+"/"+item)


backup()
