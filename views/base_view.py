import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseTabView(ABC):
    """Base class for all tab views"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.create_scrollable_frame()
        self.create_widgets()
    
    def create_scrollable_frame(self):
        """Create scrollable frame for the tab"""
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.frame, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind mouse wheel
        self._bind_mousewheel()
    
    def _bind_mousewheel(self):
        """Bind mouse wheel events for scrolling"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.frame.bind('<Enter>', _bind_to_mousewheel)
        self.frame.bind('<Leave>', _unbind_from_mousewheel)
    
    @abstractmethod
    def create_widgets(self):
        """Create widgets for the tab - must be implemented by subclasses"""
        pass
    
    def get_model(self):
        """Get the SAW model from controller"""
        return self.controller.get_model()
    
    def get_validator(self):
        """Get the validator from controller"""
        return self.controller.get_validator()