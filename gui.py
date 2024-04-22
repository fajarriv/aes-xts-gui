import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom

class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("AES XTS Encryption/Decryption GUI")
        self.createWidgets()
        self.updateExecuteButton()
        
    def createWidgets(self):
        # Header label
        self.headerLabel = tk.Label(self, text="Select your mode:", font="Times 16 bold")
        self.headerLabel.pack(pady=10)
        
        # Radio buttons
        self.mode = tk.StringVar()
        self.mode.set("encrypt")  # Set default encrypt
        modes = [("Encrypt", "encrypt"), ("Decrypt", "decrypt")]
        for text, mode in modes:
            tk.Radiobutton(self, text=text, variable=self.mode, value=mode, command=self.updateExecuteButton).pack(anchor=tk.W)
        
        # Label to display selected data file
        self.dataFileLabel = tk.Label(self, text="Data file:")
        self.dataFileLabel.pack(pady=(20, 0))
        self.selectedDataFile = tk.Label(self, text="", wraplength=400)
        self.selectedDataFile.pack(padx=20, pady=5)
        self.browseDataButton = tk.Button(self, text="Browse...", command=lambda: self.browseFile(self.selectedDataFile))
        self.browseDataButton.pack(pady=5)

        # Label to display selected key file
        self.keyFileLabel = tk.Label(self, text="Key file:")
        self.keyFileLabel.pack(pady=(10, 0))
        self.selectedKeyFile = tk.Label(self, text="", wraplength=400)
        self.selectedKeyFile.pack(padx=20, pady=5)
        self.browseKeyButton = tk.Button(self, text="Browse...", command=lambda: self.browseFile(self.selectedKeyFile))
        self.browseKeyButton.pack(pady=5)
        
        # Button execute encryption/decryption
        self.executeButton = tk.Button(self, text="Execute Encryption", command=self.executeOperation)
        self.executeButton.pack(pady=20)
        
        # Button to select download directory
        self.downloadButton = tk.Button(self, text="Select Download Directory", command=self.selectDownloadDirectory)
        self.downloadButton.pack(pady=10)

        # Label to display selected download directory
        self.selectedDownloadDirLabel = tk.Label(self, text="Download directory:")
        self.selectedDownloadDirLabel.pack(pady=(10, 0))
        self.selectedDownloadDir = tk.Label(self, text="", wraplength=400)
        self.selectedDownloadDir.pack(padx=20, pady=5)

    def browseFile(self, label):
        # Open file dialog
        file_path = filedialog.askopenfilename()
        if file_path:
            label.config(text=file_path)

    def updateExecuteButton(self):
        mode = self.mode.get()
        if mode == "encrypt":
            self.executeButton.config(text="Execute Encryption")
        else:
            self.executeButton.config(text="Execute Decryption")
    
    def executeOperation(self):
        mode = self.mode.get()
        data_path = self.selectedDataFile.cget("text")
        key_path = self.selectedKeyFile.cget("text")
        if not data_path or not key_path:
            messagebox.showerror("Error", "Please select both data and key files.")
            return
        if mode == "encrypt":
            self.encrypt(data_path, key_path)
        else:
            self.decrypt(data_path, key_path)
    
    def encrypt(self, data_path, key_path):
        with open(data_path, 'rb') as file:
            plaintext = file.read()
        with open(key_path, 'rb') as f:
            key = f.read()

        if len(key) != 32:
            messagebox.showerror("Error", "Invalid key size. AES-128-XTS requires a 32-byte key.")
            return

        key1 = key[:16]
        key2 = key[16:33]

        cipher = Cipher(algorithms.AES(key1), modes.XTS(key2), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        print(ciphertext)

        messagebox.showinfo("Info", "Encryption successful!")

        # After encryption, select download directory
        self.selectDownloadDirectory()
    
    def decrypt(self, data_path, key_path):
        # (to be implemented)
        messagebox.showinfo("Info", "Decryption successful!")

        # After decryption, select download directory
        self.selectDownloadDirectory()

    def selectDownloadDirectory(self):
        # Open directory selection dialog
        download_path = filedialog.askdirectory()
        if download_path:
            self.selectedDownloadDir.config(text=download_path)

    def read_file(self, file_path, mode):
        with open(file_path, mode) as file:
            return file.read()

def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
