
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import datetime
import shutil
from zipfile import ZipFile

def delete_all():
    count = 0
    for name in ui_files:
        try:
            if ui_files[name].get('windows') and Path(ui_files[name]['windows']).exists():
                Path(ui_files[name]['windows']).unlink()
            if ui_files[name].get('social_abs') and Path(ui_files[name]['social_abs']).exists():
                Path(ui_files[name]['social_abs']).unlink()
            count += 1
        except PermissionError:
            tk.messagebox.showinfo("Deletion Failed", f"Insufficent permissions to delete ui for {name}. If needed run in administrator mode.")
            return
      
    tk.messagebox.showinfo("Deletion Successful", f"Deleted {count} Characters UI data.")
    
    
def delete_selected():
    selection = treeview.selection()
    name = treeview.item(selection[0])['values'][0]
    try:
        if ui_files[name].get('windows') and Path(ui_files[name]['windows']).exists():
            Path(ui_files[name]['windows']).unlink()
        if ui_files[name].get('social_abs') and Path(ui_files[name]['social_abs']).exists():
            Path(ui_files[name]['social_abs']).unlink()
        tk.messagebox.showinfo("Deletion Successful", f"Deleted Character UI for {name}")
    except PermissionError:
        tk.messagebox.showinfo("Deletion Failed", f"Insufficent permissions to delete ui for {name}. If needed run in administrator mode.")
    
    
def backup_data():
    if not eq_folder_entry.get():
        tk.messagebox.showwarning("Folder not selected", "Please select appropriate Everquest Folder")
        return
    
    if not output_entry.get():
        tk.messagebox.showwarning("Folder not selected", "Please select appropriate Output Folder")
        return
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    out_path = Path(output_entry.get()+'\\equibackup\\')
    out_path.mkdir(exist_ok=True)
    zip_loc = f"{str(out_path)}\{now}.zip"
    
    with ZipFile(zip_loc, 'w') as z:
        for item in ui_files:
            if ui_files[item].get('windows'):
                p = ui_files[item]['windows']
                z.write(p, arcname=p[p.rfind('\\')+1:])
            if ui_files[item].get('social_abs'):
                p = ui_files[item]['social_abs']
                z.write(p, arcname=p[p.rfind('\\')+1:])
                
    tk.messagebox.showinfo("Backup Created", f"Backup made at: \n{zip_loc}")
    

def refresh_data():
    if not eq_folder_entry.get():
        return
    path = Path(eq_folder_entry.get())
    window_location_files = [file for file in path.iterdir() if file.is_file() and file.name.startswith('UI_') and file.name.endswith('_project1999.ini')]
    socials_abilities_files = [file for file in path.iterdir() if file.is_file() and not file.name.startswith('UI_') and file.name.endswith('_project1999.ini')]
    
    for item in window_location_files:
        file_path = str(item)
        name = item.name[item.name.find('_')+1:item.name.rfind('_')]
        if not ui_files.get(name):
            ui_files[name] = {'windows': file_path}
        else:
            ui_files[name]['windows'] = file_path
        
    for item in socials_abilities_files:
        file_path = str(item)
        name = item.name[:item.name.rfind('_')]
        if not ui_files.get(name):
            ui_files[name] = {'social_abs': file_path}
        else:
            ui_files[name]['social_abs'] = file_path
    refresh_records()
    
    
def select_bot_text():
    folder_path = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
    if folder_path:
        path = Path(folder_path)
        bot_list_entry.delete(0, tk.END)  
        bot_list_entry.insert(0, path)  


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path = Path(folder_path)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)  


def select_eq_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path = Path(folder_path)
        if sorted(path.glob('*eqgame.exe')):
            eq_folder_entry.delete(0, tk.END) 
            eq_folder_entry.insert(0, path)  
            output_entry.delete(0, tk.END)
            output_entry.insert(0, path)  
            checkmark_label.config(text="✓", fg="green")  
            
        else:
            checkmark_label.config(text="✗", fg="red")  # Clear the checkmark if no folder is selected
            tk.messagebox.showinfo("Non-Everquest Folder", f"Please select your Everquest folder, eqgame.exe not found")
    refresh_data()
    

def copy_to_bots():
    folder_path = eq_folder_entry.get()
    bot_file = bot_list_entry.get()
    output_path = output_entry.get()
    selection = treeview.selection()
    
    if not folder_path:
        tk.messagebox.showwarning("Folder not selected", "Please select appropriate Everquest Folder")
        return
    if not bot_file:
        tk.messagebox.showwarning("Bot File not selected", "Please select list of bots file")
        return
    if not selection:
        tk.messagebox.showwarning("No Source Selected", "Please select the character you want to copy ui data from")
        return
    if not output_path:
        tk.messagebox.showwarning("No Output Selected", "Please select an output location for ui files")
        return
        
    name = treeview.item(selection[0])['values'][0]
    processed = []
    with open(bot_file) as bots:
        window_src = ui_files[name].get('windows')
        social_src = ui_files[name].get('social_abs')
        dstname = bots.readline().capitalize()
        while dstname:
            win_dst = f"{output_path}/UI_{dstname}_project1999.ini"
            soc_dst = f"{output_path}/{dstname}_project1999.ini"
            if (win_dst and Path(win_dst).exists()) or (soc_dst and Path(soc_dst).exists()):
                response = tk.messagebox.askquestion("UI Exists", f"UI Data for {dstname} exists, overwrite?")
                if response == 'no':
                    dstname = bots.readline().capitalize()
                    continue
                    
            if window_src:
                shutil.copy(window_src, win_dst)
            if social_src:
                shutil.copy(social_src, soc_dst)
            processed.append(dstname)
            dstname = bots.readline().capitalize()
    refresh_data()    
    tk.messagebox.showinfo("Copy Complete", f"Copied UI data from {name} to: {','.join(processed)}")


def refresh_records():
    treeview.delete(*treeview.get_children())
    names = sorted(ui_files.keys())
    win_count = 0
    soc_count = 0
    for idx, name in enumerate(names):
        if ui_files[name].get('windows'):
            has_windows = '✓'
            win_count += 1
            last_window = datetime.datetime.fromtimestamp(Path(ui_files[name]['windows']).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        else:
            has_windows = 'Default'
            last_window = ''
        if ui_files[name].get('social_abs'):
            has_social_abs = '✓'
            soc_count += 1
            last_social = datetime.datetime.fromtimestamp(Path(ui_files[name]['social_abs']).stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        else:
            has_social_abs = '✗'
            last_social = ''  
        count_label.config(text=f"{idx+1} Characters ({win_count}/{soc_count})")
        treeview.insert("", "end", values=(name, has_windows,last_window, has_social_abs, last_social))

    
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path)
    
root = tk.Tk()
root.title("Everquest UI Tool")
icon_path = resource_path("eq.ico")
root.iconbitmap(icon_path)
root.geometry("700x460")
root.resizable(False, False)

ui_files = {}

file_label = tk.Label(root, text="Everquest Path:", anchor='w')
file_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

eq_folder_entry = tk.Entry(root)
eq_folder_entry.grid(row=0, column=1, columnspan=2, sticky='ew', padx=10, pady=10)

checkmark_label = tk.Label(root, text="✗", font=("Arial", 16), fg="red")
checkmark_label.grid(row=0, column=3, padx=10, pady=10)

select_button = tk.Button(root, text="Select EQ Folder", command=select_eq_folder)
select_button.grid(row=0, column=4, padx=10, pady=10)


file_label = tk.Label(root, text="Bot List:", anchor='e')
file_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)

bot_list_entry = tk.Entry(root)
bot_list_entry.grid(row=1, column=1, columnspan=2, sticky='ew', padx=10, pady=10)

select_button = tk.Button(root, text="Select Bot List", command=select_bot_text)
select_button.grid(row=1, column=4, padx=10, pady=10)


file_label = tk.Label(root, text="Output Path:", anchor='w')
file_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)

output_entry = tk.Entry(root)
output_entry.grid(row=2, column=1, columnspan=2, sticky='ew', padx=10, pady=10)

select_button = tk.Button(root, text="Select Ouput Folder", command=select_output_folder)
select_button.grid(row=2, column=4, padx=10, pady=10)


file_label = tk.Label(root, text="UI To Copy:", anchor='e')
file_label.grid(row=3, column=0, sticky='sw', padx=10, pady=0)

count_label = tk.Label(root, text="", anchor='w')
count_label.grid(row=3, column=4, sticky='sw', padx=10, pady=0)


treeview = ttk.Treeview(root, columns=("Name", "Window", "LastUpdatedWind", "Social", "LastUpdatedSoc"), show='headings', selectmode='browse', height=10)
treeview.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

treeview.column('Name', width=70, anchor='w')
treeview.heading("Name", text="Name")
treeview.column('Window', width=35, anchor='center')
treeview.heading("Window", text="Windows Info")
treeview.column('LastUpdatedWind', width=85, anchor='w')
treeview.heading("LastUpdatedWind", text="Last Updated")
treeview.column('Social', width=35, anchor='center')
treeview.heading("Social", text="Socials Info")
treeview.column('LastUpdatedSoc', width=85, anchor='w')
treeview.heading("LastUpdatedSoc", text="Last Updated")


execute_button = tk.Button(root, text="Copy UI Data", command=copy_to_bots)
execute_button.grid(row=5, column=4, padx=10, pady=10)

backup_button = tk.Button(root, text="Backup UI Data", command=backup_data)
backup_button.grid(row=5, column=0, padx=10, pady=10)

backup_button = tk.Button(root, text="Delete All UI Data", bg='red', fg='white', command=delete_all)
backup_button.grid(row=5, column=1, sticky='w', padx=10, pady=10)

backup_button = tk.Button(root, text="Delete Selected UI Data", bg='red', fg='white', command=delete_selected)
backup_button.grid(row=5, column=1, padx=10, pady=10)


root.grid_columnconfigure(1, weight=1)

root.mainloop()