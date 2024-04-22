
from tkinter import *
# from tkinter import messagebox, filedialog, Radiobutton


class MainWindow(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.createWidgets()
        # self.pack()

    def createWidgets(self):
        modes = [
            ("Encrypt", "encrypt"),
            ("Decrypt", "decrypt")
        ]

        self.headerLabel = Label(
            self, text="Select your mode:", font="Times 16 bold").pack()
        
        self.mode = StringVar()


def main():
    menu = MainWindow()
    menu.title("AES XTSs Encryption/Decryption GUI")
    menu.mainloop()


if __name__ == "__main__":
    main()
