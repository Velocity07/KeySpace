import sys, os
import customtkinter as ck
import sqlite3, shutil
from tkinter import filedialog, messagebox

def get_vault_path(filename):
    if getattr(sys, 'frozen', False):
        if sys.platform == 'darwin':
            base_dir = os.path.expanduser('~/Library/Application Support/KeySpace')
        elif sys.platform == 'win32':
            base_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'KeySpace')
        else:
            base_dir = os.path.expanduser('~/.keyspace')
        os.makedirs(base_dir, exist_ok=True)
        if filename.endswith('.ico') or filename.endswith('.icns') or filename.endswith('.png'):
            return os.path.join(sys._MEIPASS, 'Vault', filename)
        db_path = os.path.join(base_dir, filename)
        if not os.path.exists(db_path) and filename == 'Passwords.db':
            bundled_db = os.path.join(sys._MEIPASS, 'Vault', filename)
            if os.path.exists(bundled_db):
                shutil.copy2(bundled_db, db_path)
        return db_path
    return os.path.join('Vault', filename)

ck.set_appearance_mode('System')
ck.set_default_color_theme('blue')

window = ck.CTk()
window.geometry('870x550')
window.iconbitmap(get_vault_path('Logo.ico'))
window.title('KeySpace')

title_label = ck.CTkLabel(window, text='Welcome to KeySpace', text_color='lightblue', font=('Roboto', 24, 'bold'))
title_label.pack(pady=(20, 10))

main_frame = ck.CTkFrame(window, fg_color='transparent')
main_frame.pack(fill='both', expand=True, padx=20, pady=10)

left_frame = ck.CTkFrame(main_frame, fg_color='transparent', width=250)
left_frame.pack(side='left', fill='y', padx=(0, 10))

entry_frame = ck.CTkFrame(left_frame)
entry_frame.pack(fill='x', pady=(0, 10))

entry_label = ck.CTkLabel(entry_frame, text='Add New Password', font=('Roboto', 16, 'bold'))
entry_label.pack(pady=(10, 5))

App_Entry = ck.CTkEntry(entry_frame, placeholder_text='Enter Application Name', width=200)
App_Entry.pack(pady=5, padx=15)

Pass_Entry = ck.CTkEntry(entry_frame, placeholder_text='Enter Your Password', show='*', width=200)
Pass_Entry.pack(pady=5, padx=15)

action_frame = ck.CTkFrame(left_frame)
action_frame.pack(fill='x', pady=(0, 10))

delete_frame = ck.CTkFrame(left_frame)
delete_frame.pack(fill='x', pady=(0, 10))

delete_label = ck.CTkLabel(delete_frame, text='Delete Entry', font=('Roboto', 16, 'bold'))
delete_label.pack(pady=(10, 5))

Delete_Entry = ck.CTkEntry(delete_frame, placeholder_text='Enter ID to Delete', width=200)
Delete_Entry.pack(pady=5, padx=15)

right_frame = ck.CTkFrame(main_frame)
right_frame.pack(side='right', fill='both', expand=True)

view_label = ck.CTkLabel(right_frame, text='Vault Records', font=('Roboto', 16, 'bold'))
view_label.pack(pady=(10, 0))

records_scrollable = ck.CTkScrollableFrame(right_frame)
records_scrollable.pack(fill='both', expand=True, padx=10, pady=10)

Line_2 = ck.CTkLabel(records_scrollable, text='', font=('Roboto', 14), justify='left')
Line_2.pack(anchor='nw', padx=10, pady=10)

footer_frame = ck.CTkFrame(window, fg_color='transparent')
footer_frame.pack(fill='x', side='bottom', padx=20, pady=(0, 20))


def About():
 window_about = ck.CTkToplevel(window)
 window_about.geometry('350x180')
 window_about.iconbitmap(get_vault_path('Logo.ico'))
 window_about.title('About KeySpace')
 window_about.grab_set()

 title = ck.CTkLabel(window_about, text='KeySpace', font=('Roboto', 24, 'bold'), text_color='lightblue')
 title.pack(pady=(20, 5))
 version = ck.CTkLabel(window_about, text='Version V3.0', font=('Roboto', 16))
 version.pack()
 author = ck.CTkLabel(window_about, text='Github - Velocity-7', font=('Roboto', 14))
 author.pack(pady=(0, 15))

 action_frame_about = ck.CTkFrame(window_about, fg_color='transparent')
 action_frame_about.pack()

 Button_Import = ck.CTkButton(action_frame_about, text='Import', command=Import)
 Button_Import.pack(side='left', padx=5)
 Button_Export = ck.CTkButton(action_frame_about, text='Export', hover_color='red', command=Export)
 Button_Export.pack(side='left', padx=5)

def Clear():
 Line_2.configure(text='')    

def Delete():
 database_connector = sqlite3.connect(get_vault_path('Passwords.db'))
 database_cursor = database_connector.cursor()

 database_cursor.execute('DELETE from passwords WHERE oid= ' + Delete_Entry.get())

 database_connector.commit()
 database_connector.close() 
 Delete_Entry.delete(0, 'end')
 Show()

def Export():
 file_path = filedialog.asksaveasfilename(defaultextension='.db', initialfile='Passwords.db', filetypes=[('Database files', '*.db'), ('All files', '*.*')], title='Export Database')
 if file_path:
  try:
   shutil.copy2(get_vault_path('Passwords.db'), file_path)
   messagebox.showinfo('Export Successful', 'Database exported successfully!')
  except Exception as e:
   messagebox.showerror('Export Failed', f'An error occurred: {e}')

def Import():
 file_path = filedialog.askopenfilename(filetypes=[('Database files', '*.db'), ('All files', '*.*')], title='Import Database')
 if file_path:
  try:
   shutil.copy2(file_path, get_vault_path('Passwords.db'))
   messagebox.showinfo('Import Successful', 'Database imported successfully!')
   Show()
  except Exception as e:
   messagebox.showerror('Import Failed', f'An error occurred: {e}')

def Save():
 database_connector = sqlite3.connect(get_vault_path('Passwords.db'))
 database_cursor = database_connector.cursor()
 database_cursor.execute('INSERT INTO passwords VALUES (:App_Entry, :Pass_Entry)',
 {
    'App_Entry': App_Entry.get(),
    'Pass_Entry': Pass_Entry.get()
 }
 )
 database_connector.commit()
 database_connector.close()
 App_Entry.delete(0, 'end')
 Pass_Entry.delete(0, 'end')
 Show()

def Show():
 database_connector = sqlite3.connect(get_vault_path('Passwords.db'))
 database_cursor = database_connector.cursor()
 database_cursor.execute('SELECT *, oid FROM passwords')
 records = database_cursor.fetchall()
 
 print_records = ''

 for record in records:
    print_records += f'App Name: {record[0]} | Password: {record[1]} | ID: {record[2]}\n'

 Line_2.configure(text=print_records)

 database_connector.commit()
 database_connector.close()  

Button_Save = ck.CTkButton(entry_frame, text='Save Password', hover_color='green', command=Save)
Button_Save.pack(pady=(5, 15), padx=15)

Button_Delete = ck.CTkButton(delete_frame, text='Delete Entry', fg_color='grey', hover_color='red', command=Delete)
Button_Delete.pack(pady=(5, 15), padx=15)

Button_Show = ck.CTkButton(action_frame, text='Show Passwords', command=Show)
Button_Show.pack(pady=(15, 5), padx=15)
Button_Clear = ck.CTkButton(action_frame, text='Clear View', fg_color='grey', command=Clear)
Button_Clear.pack(pady=(5, 15), padx=15) 

Button_Quit = ck.CTkButton(footer_frame, text='Quit', fg_color='red', hover_color='darkred', command=window.quit)
Button_Quit.pack(side='right', padx=5) 
Button_About = ck.CTkButton(footer_frame, text='About', hover_color='grey', command=About)
Button_About.pack(side='left', padx=5)

database_connector = sqlite3.connect(get_vault_path('Passwords.db'))
database_cursor = database_connector.cursor()

database_connector.commit()
database_connector.close()

Show()

window.mainloop()
