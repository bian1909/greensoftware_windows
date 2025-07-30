import sys
import os
from src.interfaz import MonitorApp
import tkinter as tk

def resource_path(relative_path):
    """ Convierte rutas relativas a absolutas para .exe y desarrollo """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

if __name__ == "__main__":
    # Configura el directorio de trabajo
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
