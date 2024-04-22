from tkinter import *
from tkinter import filedialog, messagebox

class MainWindow(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("AES XTS Encryption/Decryption GUI")
        self.createWidgets()
        
    def createWidgets(self):
        # Header label
        self.headerLabel = Label(self, text="Select your mode:", font="Times 16 bold")
        self.headerLabel.pack(pady=10)
        
        # Radio buttons
        self.mode = StringVar()
        self.mode.set("encrypt")  # Set default encrypt
        modes = [("Encrypt", "encrypt"), ("Decrypt", "decrypt")]
        for text, mode in modes:
            Radiobutton(self, text=text, variable=self.mode, value=mode, command=self.updateExecuteButton).pack(anchor=W)
        
        # Entry input file
        self.dataFileLabel = Label(self, text="Select data file:")
        self.dataFileLabel.pack(pady=(20, 0))
        self.dataFileEntry = Entry(self, width=50)
        self.dataFileEntry.pack(padx=20, pady=5)
        self.browseDataButton = Button(self, text="Browse...", command=lambda: self.browseFile(self.dataFileEntry))
        self.browseDataButton.pack(pady=5)

        # Entry input untuk key file
        self.keyFileLabel = Label(self, text="Select key file:")
        self.keyFileLabel.pack(pady=(10, 0))
        self.keyFileEntry = Entry(self, width=50)
        self.keyFileEntry.pack(padx=20, pady=5)
        self.browseKeyButton = Button(self, text="Browse...", command=lambda: self.browseFile(self.keyFileEntry))
        self.browseKeyButton.pack(pady=5)
        
        # Button execute encryption/decryption
        self.executeButton = Button(self, text="Execute Encryption", command=self.executeOperation)
        self.executeButton.pack(pady=20)
        
    def browseFile(self, entry):
        # Open dialog pilih file
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, END)
            entry.insert(0, file_path)

    def updateExecuteButton(self):
        mode = self.mode.get()
        if mode == "encrypt":
            self.executeButton.config(text="Execute Encryption")
        else:
            self.executeButton.config(text="Execute Decryption")
    
    def executeOperation(self):
        # Fungsi execute
        mode = self.mode.get()
        data_path = self.dataFileEntry.get()
        key_path = self.keyFileEntry.get()
        if not data_path or not key_path:
            messagebox.showerror("Error", "Please select both data and key files.")
            return
        if mode == "encrypt":
            self.encrypt(data_path, key_path)
        else:
            self.decrypt(data_path, key_path)
        
    def encrypt(self, data_path, key_path):
        # (to be implemented)
        messagebox.showinfo("Info", "Encryption successful!")
    
    def decrypt(self, data_path, key_path):
        # (to be implemented)
        messagebox.showinfo("Info", "Decryption successful!")

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
