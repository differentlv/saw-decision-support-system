import tkinter as tk
from tkinter import ttk
from controllers.app_controller import SPKSAWController
from assets.styles import AppStyles


def main():
    """Main function to run the application"""#
    root = tk.Tk()
    app_styles = AppStyles(root)
    app_styles.configure_styles()
    root.update_idletasks()
    width = 1200
    height = 800
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.minsize(1000, 600)
    
    controller = SPKSAWController(root)
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    
    root.mainloop()


if __name__ == "__main__":
    main()