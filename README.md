# Smart File Organizer

## Description
This application was built to help users automatically organize their files into proper subfolders. It was built using python, with the help of the tkinter library for the visual representation, as well as os and shutil for file operations.

## Functionalities Implemented
- 2 types of file organizing methods that the user can choose from: Generalized & Specialized.
- 2 ways for the user to enter their desired folder: by writing its path or by visually selecting it using the GUI.
- History log that keeps track of all the moved files.
- Undo button that reallocates the moved files back to the original directory.
- Start/Stop buttons for the user to start or pause the operation, as well as a Reset button to revert the state of the application back to its default settings.
- A status label that updates the user on the status of the operation (Not Started Yet, Paused, Processing, Done, Complete)
- Popup notifications that guide the user when using the application (e.g. "Please Select a Folder First", "Operation was not Started" "Folders have been created. No Files were there to move" "Operation Successful", ...)
- Error handling: the application includes try-except blocks to handle potential errors during file operations and displays user-friendly error messages when something goes wrong.

## Instructions
- Upon running the application, the user interface is shown in ApplicationScreenshots/GUI.png
- First, select the folder you want to organize, either by clicking on the "Select Folder" button, or by typing out its path on your local machine.
- Then, select one of the two types of organizers, Generalized or Specialized.
- Lastly, press the "Start" button to start organizing the folder you have selected. If you'd like to stop the operation, simply click on the "Stop" button.
- To see the moved files history, click on the "History Log" button at the top right corner. There you can see the source path, destination path and the time the change was made. It is shown in ApplicationScreenshots/HistoryLog.png
- If you would like to reverse the change, click on the "Undo" button present inside the "History Log" window.
- See ApplicationScreenshots/test_folder-before.png, ApplicationScreenshots/test_folder-afterGeneralized.png & ApplicationScreenshots/test_folder-afterSpecialized.png