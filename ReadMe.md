# Build info:

Use pyinstaller to create executible for your environment:

pyinstaller --onefile --windowed --icon=eq.ico --add-data "eq.ico;." --name EQUITool ui.py