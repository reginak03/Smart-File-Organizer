import os
import shutil
from tkinter import *
from threading import *
from PIL import ImageTk, Image #for the app logo
from tkinter import messagebox, filedialog
from datetime import datetime #for logging moved files

#dictionary that categorizes files, each key is the folder name, and the values are file extensions that belong in that folder
fileFormat = {
    "Documents": (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".xml", ".odt", ".rtf", ".tex"),
    "Web": (".html", ".html5", ".xhtml", ".htm", ".css", ".js", ".php", ".asp", ".aspx", ".jsp", ".json", ".yaml"),
    "Images": (".jpeg", ".jpg", ".gif", ".png", ".webp", ".svg", ".heic", ".heif", ".bmp", ".tiff", ".ico", ".jfif", ".JPG", ".JPEG"),
    "Videos": (".mkv", ".wmv", ".mov", ".mp4", ".3gp", ".mpeg", ".flv", ".avi", ".webm", ".mts", ".m4v"),
    "Audio": (".m4a", ".mp3", ".wav", ".webm", ".ogg", ".flac", ".aac", ".wma", ".aiff", ".opus"),
    "Compressed": (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".dmg", ".iso", ".lz", ".z"),
    "Programs": (".py", ".java", ".cpp", ".c", ".cs", ".sh", ".js", ".ts", ".swift", ".rb", ".go", ".php", ".bat", ".pl", ".rs"),
    "Apps": (".exe", ".msi", ".app", ".apk", ".deb", ".rpm", ".bin", ".command"),
    "Spreadsheets": (".xls", ".xlsx", ".ods"),
    "Presentations": (".ppt", ".pptx", ".odp", ".key"),
    "Databases": (".sql", ".db", ".dbf", ".mdb", ".accdb", ".sqlite", ".sqlite3"),
    "CAD": (".dwg", ".dxf", ".step", ".stp", ".igs", ".iges", ".3dm"),
    "Archives": (".cab", ".arj", ".lzh", ".ace"),
    "Executables": (".exe", ".dll", ".sys", ".ocx", ".vxd")
}

class FileOrganizer: 
    #create the main application window, specify the window size, title, background color, etc.
    def __init__(self, root):
        #setting the tkinter main window
        self.window = root
        self.window.geometry("720x400")
        self.window.title("File Organizer")
        self.window.resizable(width = False, height = False)
        self.window.configure(bg="gray90")
        #initialize variables to track:
        self.selected_dir = "" #to store the path of the folder selected by the user
        self.browsed = False #to check if the user selected a valid folder (that exists)
        self.is_running = False #to track if the operation is ongoing
        self.history_log = [] #to store moved files history

        #GUI components:
        #frame 1: logo, logging & exit button
        self.frame_1 = Frame(self.window,bg="gray90", width=100, height=100)
        self.frame_1.place(x=20, y=20)
        self.display_logo()
        #exit button to close the application
        Exit_Btn = Button(self.window, text="Exit", font=("Arial", 10, "bold"), fg="red", width=5, command=self.exit_window)
        Exit_Btn.place(x=640, y=20)
        #logging history button
        History_Btn = Button(self.window, text="History Log", font=("Arial", 11, "bold"), fg="black", width=5, command=self.showHistory)
        History_Btn.place(x=638, y=50)

        #frame 2: main page widgets
        self.frame_2 = Frame(self.window, bg="white", width=720, height=480)
        self.frame_2.place(x=0, y=110)
        self.main_window()
        self.history_window = None #to track the open history window
        #organizer options:
        self.organizer_mode = StringVar(value="generalized") #default value
        Label(self.window, text="Select Organizer:", font=("Arial", 12, "bold"), bg="white", fg="black").place(x=160, y=250)
        Radiobutton(self.window, text="Generalized (e.g. Documents, Images, ...)", font=("Arial", 11), bg="white", fg="black", variable=self.organizer_mode, value="generalized").place(x=270, y=249)
        Radiobutton(self.window, text="Specialized (e.g. pdf, jpeg, docx, ...)", font=("Arial", 11), bg="white", fg="black", variable=self.organizer_mode, value="specialized").place(x=270, y=270)

    #application logo and title
    def display_logo(self):
        image = Image.open("Images/file_organizer_logo.png")
        resized_image = image.resize((80, 80))
        self.logo = ImageTk.PhotoImage(resized_image)
        label = Label(self.frame_1, bg="gray90",image=self.logo)
        label.pack(side=LEFT, padx=5)
        title_label = Label(self.frame_1, text="Smart File Organizer", font=("Arial", 20, "bold"), bg="gray90", fg="black")
        title_label.pack(side=LEFT, padx=10)

    #this method presents all the components related to file organization within a folder
    #it includes features like the “Select Folder” button for selecting a directory via the tkinter dialog box, an entry widget for manually entering the target folder’s location, a status label, and the “Start”, "Stop" & "Reset" buttons
    def main_window(self):
        Heading_Label = Label(self.frame_2, text="Please Select the Folder to Organize, or Enter its Path on your Local Machine", font=("Arial", 16, "bold"), bg="white", fg="black")
        Heading_Label.place(x=60, y=20)
        Folder_Button = Button(self.frame_2, text="Select Folder", font=("Arial", 10, "bold"), bg="white", fg="black", command=self.select_directory)
        Folder_Button.place(x=165, y=80)
        self.Folder_Entry = Entry(self.frame_2, font=("Arial", 12), width=32, bg="white", fg="black", insertbackground="black") 
        self.Folder_Entry.place(x=271, y=80)

        Status = Label(self.frame_2, text="Status: ", font=("Arial", 12, "bold"), bg="white", fg="black")
        Status.place(x=195, y=110)
        self.Status_Label = Label(self.frame_2, text="Not Started Yet", font=("Arial", 12), bg="white", fg="red")
        self.Status_Label.place(x=272, y=110)
        
        Start_Button = Button(self.frame_2, text="Start", font=("Arial", 13, "bold"), bg="white", fg="black", width=8, command=self._threading) #when the "Start" button is clicked, the _threading method starts the organizer in a separate thread to keep the GUI responsive
        Start_Button.place(x=170, y=200)

        Stop_Button = Button(self.frame_2, text="Stop", font=("Arial", 13, "bold"), bg="white", fg="black", width=8, command=self.stop)
        Stop_Button.place(x=285, y=200)
        
        Reset_Button = Button(self.frame_2, text="Reset", font=("Arial", 13, "bold"), bg="white", fg="black", width=8, command=self.reset)
        Reset_Button.place(x=400, y=200)

    #select the target folder via file dialog
    def select_directory(self):
        self.selected_dir = filedialog.askdirectory(title = "Select a location") #open a file dialog to let the user choose a folder
        self.Folder_Entry.insert(0, self.selected_dir) #update the entry field with the selected path
        self.selected_dir = str(self.selected_dir)
        #check if the folder path exists or not
        if os.path.exists(self.selected_dir):
            self.browsed = True

    #handle organizer events
    #before the organizer method, I started a separate thread using python’s "threading" module to call the "organizer" method, to keep the GUI responsive during file operations (parallel execution)
    def _threading(self):
        self.x = Thread(target=self.organizer, daemon=True)
        self.x.start()

    #organizes files based on selected mode, updates the status and shows completion messages
    def organizer(self):
        if not self.browsed and not self.Folder_Entry.get(): #if no directory is chosen by either method (manually or via file dialog)
            messagebox.showwarning("No folders are chosen", "Please Select a Folder First")
            return

        if not self.browsed and self.Folder_Entry.get(): #if the user typed the directory path manually, update self.selected_dir
            self.selected_dir = self.Folder_Entry.get()
            if not os.path.exists(self.selected_dir):  #validate path
                messagebox.showerror("Invalid Path", "The entered path does not exist!")
                return

        try:
            self.Status_Label.config(text="Processing...")
            self.Current_Path = self.selected_dir
            self.is_running = True #process started running
            self.stop_requested = False #flag to handle pausing
            self.Folder_List1 = [] #stores all the folders that are already presented in the selected directory
            self.Folder_List2 = [] #stores newly created folders
            self.flag = False

            os.chdir(self.Current_Path)

            selected_mode = self.organizer_mode.get()

            if selected_mode == "generalized":
                for folder, extensions in fileFormat.items(): #create folders based on the fileFormat dictionary. Go through each key (folder) and find the files with matching extension values to that key
                    if self.stop_requested: #check if the user clicked on the "Stop" button
                        self.Status_Label.config(text="Paused")
                        return

                    #call the "file_finder" function to find a specific type of file (/extension) and change their old path to the new path
                    matching_files = self.file_finder(self.Current_Path, extensions)
                    if not matching_files:
                        continue #no files to move, skip this folder

                    folder_path = os.path.join(self.Current_Path, folder)
                    if not os.path.exists(folder_path): #the folder is not present in that directory, create a new one and append the file to it
                        os.mkdir(folder_path)
                        self.Folder_List2.append(folder)
                    else: #the folder is already present in that directory 
                        self.Folder_List1.append(folder)

                    for item in matching_files:
                        if self.stop_requested:
                            self.Status_Label.config(text="Paused")
                            return

                        old_path = os.path.join(self.Current_Path, item)
                        new_path = os.path.join(folder_path, item)
                        shutil.move(old_path, new_path) #move the file to the new directory (from old_path to new_path)

                        #for logging:
                        move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.history_log.append({
                            "src": old_path,
                            "dest": new_path,
                            "time": move_time
                        })

                        self.flag = True

            elif selected_mode == "specialized":
                files = [f for f in os.listdir(self.Current_Path) if os.path.isfile(os.path.join(self.Current_Path, f))]

                for file in files: #go through each file in the directory
                    if self.stop_requested: #check if the user clicked on the "Stop" button
                        self.Status_Label.config(text="Paused")
                        return
                    
                    filename, extension = os.path.splitext(file)  #split filename and file extension
                    extension = extension[1:].lower() #get the extension name (without the dot), lowercase

                    if not extension:
                        continue #skip files without extensions

                    ext_folder = os.path.join(self.Current_Path, extension)

                    if not os.path.exists(ext_folder): #if the extension directory does not exist, create directory first, then move the file into it
                        os.makedirs(ext_folder)
                        self.Folder_List2.append(extension)
                    else:
                        self.Folder_List1.append(extension)

                    old_path = os.path.join(self.Current_Path, file)
                    new_path = os.path.join(ext_folder, file)
                    shutil.move(old_path, new_path)

                    move_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.history_log.append({
                        "src": old_path,
                        "dest": new_path,
                        "time": move_time
                    })

                    self.flag = True #at least one file has been moved

            else:
                messagebox.showerror("Invalid Option", "Unknown organizer mode selected.")

            if self.flag: #the program discovered matching files and they have been organized
                self.song_Label.config(text="Done!")
                messagebox.showinfo("Done!", "Operation Successful!")
            
            else: #the program didn't find any matching files (no files were moved)
                self.Status_Label.config(text="Complete!")
                messagebox.showinfo("Done!", "Folders have been created\nNo Files were there to move")

            self.reset() #automatically

        except Exception as es:  #if any error occurs
            messagebox.showerror("Error!", f"Error due to {str(es)}")
        finally:
            self.is_running = False #mark process as stopped

    #this method scans the given folder (folder_path) for files matching the given extension and appends it to a python list. The function later returns this list
    def file_finder(self, folder_path, file_extensions):
        self.files = []
        for file in os.listdir(folder_path): #for each file in the given directory (folder_path)
            for extension in file_extensions:
                if file.endswith(extension):
                    self.files.append(file)
        return self.files
    
    def stop(self):
        if not self.is_running:
            messagebox.showinfo("Info", "Operation was not started.")
        else:
            self.stop_requested = True #this variable is present inside the organizer function, which checks its value in every loop. If it is true, the organizer function returns
            messagebox.showinfo("Info", "Operation paused.")


    #clear both the entry and label widgets and reset the "selected_dir" variable following each successful operation, or when user clicks on the "Reset" button
    def reset(self):
        self.Status_Label.config(text="Not Started Yet")
        self.Folder_Entry.delete(0, END)
        self.selected_dir = ""
        self.browsed = False
        self.is_running = False
        self.stop_requested = False
        self.organizer_mode.set("generalized")

    #displays a new window with all the recorded file movements
    def showHistory(self):
        #if a history window is already open, destroy it before displaying the new one
        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_window.destroy()

        self.history_window = Toplevel(self.window)
        self.history_window.title("History Log")
        self.history_window.geometry("800x500")
        Label(self.history_window, text="File Move History", font=("Arial", 14, "bold")).pack(pady=10)

        text_box = Text(self.history_window, wrap="word", font=("Courier", 12))
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        if self.history_log:
            for entry in self.history_log:
                text_box.insert(END, "Source: " + entry["src"] + "\n" + "Destination: " + entry["dest"] + "\n" + "Time: " + entry["time"] + "\n\n")
        else:
            text_box.insert(END, "No file movements logged yet.")

        #undo all button
        Button(self.history_window, text="Undo", font=("Arial", 11, "bold"), fg="red", command=self.undo_all_moves).pack(pady=10)
        text_box.config(state="disabled")  #read-only

    def undo_all_moves(self):
        failed = []
        for i in reversed(range(len(self.history_log))):  #reversed to avoid index issues
            entry = self.history_log[i]
            try:
                shutil.move(entry["dest"], entry["src"]) #move file back

                #check if destination folder is now empty and remove it if so
                dest_folder = os.path.dirname(entry["dest"])
                if os.path.isdir(dest_folder) and not os.listdir(dest_folder):
                    os.rmdir(dest_folder)

            except Exception as e: 
                failed.append(entry)
            else:
                del self.history_log[i]
        #update existing widgets in the same window (no new window)
        self.showHistory()

        if failed:
            messagebox.showerror("Undo All", f"{len(failed)} undos failed.")

    #function for the "Exit" button in the application header
    def exit_window(self):
        self.window.destroy()

#create an instance of the fileOrganizer class to build the GUI, then start the main loop
if __name__ == "__main__": #check if the script is being run as the main program (to ensure that the code inside this block only runs when the script is executed, not when imported as a module...)
    root = Tk()
    obj = FileOrganizer(root)
    root.mainloop()

######################################################################################
#File Movement Process (thought process):
#For each file in the selected directory:
# 1. Gets its extension
# 2. Checks if a matching folder exists
# 3. Creates the folder if needed
# 4. Moves the file into the folder
# 5. Records the move in the history log
######################################################################################
# The Organization Process Flow
# 1. User selects a folder (or enters path manually)
# 2. User chooses organization mode (Generalized or Specialized)
# 3. User clicks "Start":
#    - Application scans the folder
#    - Creates necessary subfolders
#    - Moves files to appropriate folders
#    - Records each move in history
# 4. When complete:
#    - Shows success message
#    - Updates status
# 5. User can:
#    - View history of moves
#    - Undo all moves
#    - Start a new operation
######################################################################################
#initial implementation:
# import os
# import shutil
    
# path = input("Enter Path: ") #path of directory that you want to organize
# files = os.listdir(path) #lists all the files within this path

# for file in files: #go through each file in the directory
#     filename,extension = os.path.splitext(file) #split filename and file extension
#     extension = extension[1:] #get the extension name (without the dot)

#     if os.path.exists(path+'/'+extension): #if the extension directory already exists, move the file to that directory
#         shutil.move(path+'/'+file, path+'/'+extension+'/'+file)
#     else:
#         os.makedirs(path+'/'+extension) #create directory first, then move the file into it
#         print("New folder created: "+extension)
#         shutil.move(path+'/'+file, path+'/'+extension+'/'+file)
#     print('File "'+file+'" was moved into '+extension)