import os
import tkinter as tk
from tkinter import filedialog, messagebox

from aes_xts import AESXTS


class MainWindow(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("AES XTS Encryption/Decryption GUI")
        self.create_widgets()

    def create_widgets(self):
        # Header label
        self.header_label = tk.Label(
            self, text="Select your mode:", font="Times 16 bold")
        self.header_label.pack(pady=10)

        # Radio buttons
        self.mode = tk.StringVar()
        self.mode.set("encrypt")  # Set default encrypt
        modes = [("Encrypt", "encrypt"), ("Decrypt", "decrypt")]
        for text, mode in modes:
            tk.Radiobutton(self, text=text, variable=self.mode, value=mode,
                           command=self.update_execute_button).pack(anchor=tk.W)

        # Input file widgets
        self.input_file_label = tk.Label(
            self, text="Input file:", font="Times 14 bold")
        self.input_file_label.pack(pady=(20, 0))

        self.selected_input_file_label = tk.Label(
            self, text="", wraplength=400)
        self.selected_input_file_label.pack(padx=20, pady=5)

        self.browse_input_file_button = tk.Button(
            self, text="Browse input file", command=self.select_input_file)
        self.browse_input_file_button.pack(pady=5)

        # key file widgets
        self.key_file_label = tk.Label(
            self, text="Key file:", font="Times 14 bold")
        self.key_file_label.pack(pady=(10, 0))

        self.selected_key_file = tk.Label(self, text="", wraplength=400)
        self.selected_key_file.pack(padx=20, pady=5)

        self.browse_key_file_button = tk.Button(
            self, text="Browse key file", command=self.select_key_file)
        self.browse_key_file_button.pack(pady=5)

        # Button execute encryption/decryption
        self.execute_button = tk.Button(
            self, text="Execute Encryption", command=self.execute_operation)
        self.execute_button.pack(pady=20)

        # Button to select download directory
        self.downloadButton = tk.Button(
            self, text="Select Download Directory", command=self.download_result)
        self.downloadButton.pack(pady=10)

        # Label to display selected download directory
        self.selectedDownloadDirLabel = tk.Label(
            self, text="Download directory:")
        self.selectedDownloadDirLabel.pack(pady=(10, 0))
        self.selectedDownloadDir = tk.Label(self, text="", wraplength=400)
        self.selectedDownloadDir.pack(padx=20, pady=5)

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename()
        if self.input_file_path:
            self.file_base_name = os.path.basename(self.input_file_path).split(".")[0]
            self.origin_file_type = self.input_file_path.split(".")[1]
            self.selected_input_file_label.config(
                text=f'{self.file_base_name}.{self.origin_file_type}', wraplength=400)

    def select_key_file(self):
        self.key_file_path = filedialog.askopenfilename()
        if self.key_file_path:
            self.selected_key_file.config(
                text=os.path.basename(self.key_file_path))

    def update_execute_button(self):
        mode = self.mode.get()
        if mode == "encrypt":
            self.execute_button.config(text="Execute Encryption")
        else:
            self.execute_button.config(text="Execute Decryption")

    def execute_operation(self):
        mode = self.mode.get()

        if not self.input_file_path or not self.key_file_path:
            messagebox.showerror(
                "Error", "Please select both data and key files.")
            return

        aes = AESXTS(self.read_key_file())
        input_data = self.read_input_file()
        print("Input data", input_data)
        if mode == "encrypt":
            self.result = aes.encrypt(input_data)
            self.output_file_type = f"{self.origin_file_type}.txt"
        else:
            self.result = aes.decrypt(input_data)
            self.output_file_type = self.origin_file_type
        print(self.result)

    def read_key_file(self):
        with open(self.key_file_path, "r") as key_file:
            key = bytes.fromhex(key_file.read().strip())
            return key

    def read_input_file(self):
        with open(self.input_file_path, "rb") as input_file:
            print("Reading input file", input_file.read())
            return input_file.read()

    def download_result(self):
        if not hasattr(self, "result"):
            messagebox.showerror("Error", "No result to bed downloaded.")
            return

        download_dir = filedialog.askdirectory()
        if download_dir:

            complete_path = os.path.join(
                download_dir, f"{self.file_base_name}-result." + self.output_file_type)
            
            with open(complete_path, "wb") as output_file:
                output_file.write(self.result)
                messagebox.showinfo("Success", "Output has been successfully downloaded!")



def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
