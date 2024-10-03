# main.py
from tkinter import Tk
from gui import AppGUI
from database import DatabaseController  # Asumo que tienes un controlador de base de datos definido aquí

def main():
    root = Tk()
    db_controller = DatabaseController()  # Instanciar el controlador de base de datos
    app = AppGUI(root, db_controller)  # Pasar el controlador de base de datos como segundo argumento
    root.mainloop()

if __name__ == "__main__":
    main()
