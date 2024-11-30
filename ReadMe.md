# Info:

This tool is used to create (or overwrite) UI data from a source, an existing character ui data, to character names supplied in a text file. This eliminates manual work of copy/pasting and naming ui files correctly.

# Usage:

1) Select your Everquest folder

2) Select your Bot List txt file
This file should be a txt file that has one character name per line, capitalization does not matter, this app does not support invalid everquest names (multiple capital letters in name)
You can use different text files for different profiles of characters (ex clerics, mages, etc.)

3) (OPTIONAL) If desired, or if permissions dont permit you to create files in the everquest folder you can select an alternate output location of files, then copy those files into your everquest directory

4) Highly suggest using the backup ui data button before proceeding, which will create a zip file of existing ui data to the output folder location + \equibackup\ folder.

5) Select a character to source UI Data from. Ideally this profile should have window data and socials data. If a profile has only one, data will only be created for that type.

6) Press Copy UI Data and Characters listed in the bot list will have their ui data updated from the selected source
If UI Data already exists for a given character you will be prompted to overwrite their data.

# Build info:

Use pyinstaller to create executible for your environment:

pyinstaller --onefile --windowed --icon=eq.ico --add-data "eq.ico;." --name EQUITool ui.py

