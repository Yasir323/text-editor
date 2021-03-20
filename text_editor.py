import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import filedialog, font, colorchooser, messagebox
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)
file = None


# Functions
def new_file(event=None):
    root.title('Untitled - Text editor')
    text_area.delete(1.0, tk.END)


def open_file(event=None):
    global file

    # Get file name
    file = filedialog.askopenfilename(
                            defaultextension='.txt',
                            filetypes=[
                                ('Text Documents', '*.txt'),
                                ('All Files', '*.*'),
                                ('Python Files', '*.py')
                            ])

    if file == '':
        file = None
    else:
        root.title(os.path.basename(file) + '- Notepad')
        text_area.delete(1.0, tk.END)
        opened_file = open(file, mode='r')
        text_area.insert(1.0, opened_file.read())
        opened_file.close()


def save(event=None):
    global file
    if file is None:
        file = filedialog.asksaveasfilename(
                                    initialfile='Untitled.txt',
                                    defaultextension='.txt',
                                    filetypes=[
                                            ('Text Document', '*.txt'),
                                            ('All Files', '*.*')
                                    ])
        if file == '':
            file = None
        else:
            # Save a new file
            saved_file = open(file, mode='w')
            saved_file.write(text_area.get(1.0, tk.END))
            saved_file.close()
            root.title(os.path.basename(file) + ' - Notepad')

    else:
        # Save an already existing file
        saved_file = open(file, mode='w')
        saved_file.write(text_area.get(1.0, tk.END))
        saved_file.close()


def save_as(event=None):
    global file
    file = filedialog.asksaveasfilename(
                                initialfile='Untitled.txt',
                                defaultextension='.txt',
                                filetypes=[
                                        ('Text Document', '*.txt'),
                                        ('All Files', '*.*')
                                ])
    if file:
        saved_file = open(file, mode='w')
        saved_file.write(text_area.get(1.0, tk.END))
        saved_file.close()
        root.title(os.path.basename(file) + ' - Notepad')


def close(event=None):
    global text_changed, file
    if text_changed:
        mbox = messagebox.askyesnocancel(
                            'warning',
                            'Do you want to save the file before closing?'
        )
        if mbox:
            save()
            root.destroy()
        elif mbox is False:
            root.destroy()
    else:
        root.destroy()


text_changed = False


def is_modified(event=None):
    global text_changed
    if text_area.edit_modified():
        text_changed = True
    text_area.edit_modified(False)


def find_replace(event=None):

    def find():
        word = find_entry.get()
        text_area.tag_remove('match', '1.0', tk.END)
        if word:
            start_pos = '1.0'
            while 2:
                start_pos = text_area.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                # print(start_pos, type(start_pos))
                end_pos = f'{start_pos} + {len(word)}c'
                text_area.tag_add('match', start_pos, end_pos)
                start_pos = end_pos
                text_area.tag_config('match', foreground='white', background='blue')

    def replace():
        find_word = find_entry.get()
        replace_word = replace_entry.get()
        new_word = text_area.get(1.0, tk.END).replace(find_word, replace_word)
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, new_word)

    # Dialog box
    dbox = tk.Toplevel()
    dbox.geometry('300x200')
    dbox.title('Find and Replace')
    dbox.resizable(False, False)

    fr_frame = ttk.LabelFrame(dbox, text='Find | Replace')
    fr_frame.pack(pady=20)
    find_label = ttk.Label(fr_frame, text='Find')
    find_label.grid(row=0, column=0, pady=5)
    find_entry = ttk.Entry(fr_frame, width=20)
    find_entry.grid(row=0, column=1, pady=5)

    replace_label = ttk.Label(fr_frame, text='Replace')
    replace_label.grid(row=1, column=0, pady=5)
    replace_entry = ttk.Entry(fr_frame, width=20)
    replace_entry.grid(row=1, column=1, pady=5)

    find_btn = ttk.Button(fr_frame, text='Find', command=find)
    find_btn.grid(row=2, column=0, pady=5, padx=5)
    replace_btn = ttk.Button(fr_frame, text='Replace', command=replace)
    replace_btn.grid(row=2, column=1, pady=5, padx=5)


current_font = 'Segoe Print'
current_font_size = 12


# Font size
def change_font(event=None):
    global current_font
    current_font = font_var.get()
    text_area.config(font=(current_font, current_font_size))


def change_font_size(event=None):
    global current_font_size
    current_size = size_var.get()
    text_area.config(font=(current_font, current_size))


def hide_toolbar(event=None):
    global show_toolbar
    if show_toolbar:
        toolbar_label.pack_forget()
        show_toolbar = False
    else:
        text_area.pack_forget()
        toolbar_label.pack(side=tk.TOP, fill=tk.X)
        text_area.pack(fill=tk.BOTH, expand=True)
        show_toolbar = True


def hide_statusbar(event=None):
    global show_statusbar
    if show_statusbar:
        statusbar_label.pack_forget()
        show_statusbar = False
    else:
        text_area.pack_forget()
        statusbar_label.pack(side=tk.BOTTOM, fill=tk.X)
        text_area.pack(fill=tk.BOTH, expand=True)
        show_statusbar = True


def bg_color(event=None):
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(bg=color)


def fg_color(event=None):
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(fg=color)


def text_color(event=None):
    color = colorchooser.askcolor()[1]
    if color:
        color_font = font.Font(text_area, text_area.cget('font'))
        # Configure a tag
        text_area.tag_configure('colored', font=color_font, foreground=color)
        # Define current tag
        current_tag = text_area.tag_names('sel.first')
        if 'colored' in current_tag:
            text_area.tag_remove('colored', 'sel.first', 'sel.last')
        else:
            text_area.tag_add('colored', 'sel.first', 'sel.last')


# Creating the root window
root = tk.Tk()

root.title('Untitled - Text Editor')
root.geometry('800x600')
root.iconbitmap('icon.ico')

# Text Area
text_area = tk.Text(root,
                    font=('Segoe Print', 12),
                    foreground='blue'
                    )
text_area.config(wrap='word', relief=tk.FLAT)

####################################################
#################### Menubar #######################
####################################################
menubar = tk.Menu(root)

#################### File menu #####################
new_file_icon = tk.PhotoImage(file='new_file.png')
open_file_icon = tk.PhotoImage(file='open_file.png')
save_file_icon = tk.PhotoImage(file='save_file.png')
saveas_file_icon = tk.PhotoImage(file='save_file.png')
exit_file_icon = tk.PhotoImage(file='exit_file.png')

file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(
            label='New',
            image=new_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + N',
            command=new_file
)
file_menu.add_command(
            label='Open',
            image=open_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + O',
            command=open_file
)
# file_menu.add_separator()
file_menu.add_command(
            label='Save',
            image=save_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + S',
            command=save
)
file_menu.add_command(
            label='Save as',
            image=save_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + Shift + S',
            command=save_as
)
# file_menu.add_separator()
file_menu.add_command(
            label='Exit',
            image=exit_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + Q',
            command=close
)

menubar.add_cascade(label='File', menu=file_menu)

################## Edit menu #######################
cut_file_icon = tk.PhotoImage(file='cut_file.png')
copy_file_icon = tk.PhotoImage(file='copy_file.png')
paste_file_icon = tk.PhotoImage(file='paste_file.png')
clear_all_file_icon = tk.PhotoImage(file='clear_file.png')
find_file_icon = tk.PhotoImage(file='find.png')
##Select all option
##Undo
##Redo

edit_menu = tk.Menu(menubar, tearoff=False)
edit_menu.add_command(
            label='Cut',
            image=cut_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + X',
            command=lambda: text_area.event_generate('<Control x>')
)
edit_menu.add_command(
            label='Copy',
            image=copy_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + C',
            command=lambda: text_area.event_generate('<Control c>')
)
# file_menu.add_separator()
edit_menu.add_command(
            label='Paste',
            image=paste_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + V',
            command=lambda: text_area.event_generate('<Control v>')
)
edit_menu.add_command(
            label='Clear all',
            image=clear_all_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + Shift + X',
            command=lambda: text_area.delete(1.0, tk.END)
)
# file_menu.add_separator()
edit_menu.add_command(
            label='Find',
            image=find_file_icon,
            compound=tk.LEFT,
            accelerator='CTRL + F',
            command=find_replace
)

menubar.add_cascade(label='Edit', menu=edit_menu)

# View Menu
toolbar_icon = tk.PhotoImage(file='tool_bar.png')
statusbar_icon = tk.PhotoImage(file='status_bar.png')

# Toolbar Label
toolbar_label = ttk.Label(root)
toolbar_label.pack(side=tk.TOP, fill=tk.X)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

# Statusbar Label
statusbar_label = ttk.Label(root, text='Status Bar')
statusbar_label.pack(side=tk.BOTTOM, fill=tk.X)
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)

view_menu = tk.Menu(menubar, tearoff=False)

view_menu.add_checkbutton(
            label='Tool bar',
            onvalue=True,
            offvalue=0,
            variable=show_toolbar,
            image=toolbar_icon,
            compound=tk.LEFT,
            command=hide_toolbar
)
view_menu.add_checkbutton(
            label='Status bar',
            onvalue=True,
            offvalue=0,
            variable=show_statusbar,
            image=statusbar_icon,
            compound=tk.LEFT,
            command=hide_statusbar
)

menubar.add_cascade(label='View', menu=view_menu)

# Creating toolbar option
fonts = font.families()
font_var = tk.StringVar()
font_box = ttk.Combobox(
                toolbar_label,
                width=30,
                textvariable=font_var,
                state='readonly'
)
font_box['values'] = fonts
font_box.current(fonts.index('Segoe Print'))
font_box.grid(row=0, column=0, padx=5, pady=5)

# Font size box
size_var = tk.IntVar()
size_box = ttk.Combobox(toolbar_label, width=20, textvariable=size_var, state='readonly')
size_box['values'] = tuple(range(8, 100, 2))
size_box.current(2)
size_box.grid(row=0, column=1, padx=5)


# Creating a scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.focus_set()
text_area.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text_area.yview)
text_area.config(yscrollcommand=scrollbar.set)

# Creating color select menu
color_menu = tk.Menu(menubar, tearoff=False)
color_menu.add_command(label='Selected text', command=text_color)
color_menu.add_command(label='All text', command=fg_color)
color_menu.add_command(label='Background', command=bg_color)
menubar.add_cascade(label='Color', menu=color_menu)

root.config(menu=menubar)

text_area.bind('<<Modified>>', is_modified)
font_box.bind('<<ComboboxSelected>>', change_font)
size_box.bind('<<ComboboxSelected>>', change_font_size)
root.bind('<Control-n>', new_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save)
# root.bind('<Control-Shift-s>', save_as)
root.bind('<Control-q>', close)
root.bind('<Control-f>', find_replace)

root.mainloop()
