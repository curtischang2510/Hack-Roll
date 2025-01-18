from tkinter import messagebox

def ErrorDialog(message):
    messagebox.showerror("Error", message)

def InfoDialog(message):
    messagebox.showinfo("Information", message)
