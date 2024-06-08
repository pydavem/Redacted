""" Main program """
import tkinter as tk
import tkinter.filedialog
import tkinter.simpledialog
from pathlib import Path
import redactor


def on_readact_ips_toggle():
    """ toggle the variable for IP redaction """
    if redactIPs.get() == 1:
        print("Checkbutton is selected")
    else:
        print("Checkbutton is deselected")


def on_readact_logins_toggle():
    """ toggle the variable for Logins redaction """
    if redactLogins.get() == 1:
        print("Checkbutton is selected")
    else:
        print("Checkbutton is deselected")


def on_readact_machines_toggle():
    """ toggle the variable for Machine Names redaction """
    if redactLogins.get() == 1:
        print("Checkbutton is selected")
    else:
        print("Checkbutton is deselected")


def select_file():
    """ select a single file for redaction """
    file = tkinter.filedialog.askopenfilename(title='Open a File')

    if file:
        redactor.redact_file(file, redactIPs.get(),
                             redactLogins.get(), redactMachines.get())


def select_folder():
    """ select a folder for redaction """

    new_files = []
    path = tkinter.filedialog.askdirectory(title='Select a folder')
    if len(path):
        p = Path(path).rglob('*.txt')
        for file in p:
            if not new_files.count(file):
                print(f'Processing {file}')
                new_file = redactor.redact_file(file, redactIPs.get(),
                                                redactLogins.get(), redactMachines.get())
                new_files.append(new_file)
            else:
                print(f'not processing new file {file}')


root = tk.Tk()

top_frame = tk.Frame(root, bg='cyan', width=450, height=50, pady=3)
center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = tk.Frame(root, bg='white', width=450, height=45, pady=3)
btm_frame2 = tk.Frame(root, bg='lavender', width=450, height=60, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")

redactIPs = tk.IntVar(master=top_frame)
checkbutton_ips = tk.Checkbutton(top_frame, text="Redact IP's", variable=redactIPs,
                                 onvalue=1, offvalue=0, command=on_readact_ips_toggle)
checkbutton_ips.config(bg="lightgrey", fg="blue", font=("Arial", 12),
                       selectcolor="green", relief="raised", padx=10, pady=5)

# Placing the Checkbutton in the window
checkbutton_ips.pack(padx=40, pady=4)

redactLogins = tk.IntVar(master=top_frame)
checkbutton_logins = tk.Checkbutton(top_frame, text="Redact Logins", variable=redactLogins,
                                    onvalue=1, offvalue=0, command=on_readact_logins_toggle)
checkbutton_logins.config(bg="lightgrey", fg="blue", font=("Arial", 12),
                          selectcolor="green", relief="raised", padx=10, pady=5,state="disabled")

# Placing the Checkbutton in the window
checkbutton_logins.pack(padx=40, pady=4)

redactMachines = tk.IntVar(master=top_frame)
checkbutton_machines = tk.Checkbutton(top_frame, text="Redact Machine Names",
                                      variable=redactMachines,
                                      onvalue=1, offvalue=0, command=on_readact_machines_toggle)
checkbutton_machines.config(bg="lightgrey", fg="blue", font=("Arial", 12),
                            selectcolor="green", relief="raised", padx=10, pady=5,state="disabled")

# Placing the Checkbutton in the window
checkbutton_machines.pack(padx=40, pady=4)

button_file = tk.Button(center, text='Select a File', command=select_file)
button_folder = tk.Button(
    center, text='Select a Folder (Recursive, so be carefull)', command=select_folder)

button_file.pack(padx=10, pady=10)
button_folder.pack(pady=10)

root.wm_title('Daves Amazing Redactor')
root.mainloop()
