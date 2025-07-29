import tkinter as tk
from tkinter import ttk
from config.settings import AppConfig


class AppStyles:
    """Application styling and theme manager"""
    
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        
    def configure_styles(self):
        """Configure all application styles"""
        self.root.title(AppConfig.WINDOW_TITLE)
        self.root.configure(bg=AppConfig.BACKGROUND_COLOR)
        
        # Try to use modern theme
        try:
            self.style.theme_use(AppConfig.THEME)
        except:
            pass
        
        # Configure custom styles
        self._configure_label_styles()
        self._configure_button_styles()
        self._configure_frame_styles()
    
    def _configure_label_styles(self):
        """Configure label styles"""
        self.style.configure('Title.TLabel', 
                           font=AppConfig.TITLE_FONT, 
                           background=AppConfig.BACKGROUND_COLOR)
        
        self.style.configure('Heading.TLabel', 
                           font=AppConfig.HEADING_FONT, 
                           background=AppConfig.BACKGROUND_COLOR)
    
    def _configure_button_styles(self):
        """Configure button styles"""
        # Accent button
        self.style.configure('Accent.TButton', 
                           foreground='white',
                           background=AppConfig.PRIMARY_COLOR,
                           font=AppConfig.HEADING_FONT)
        
        self.style.map('Accent.TButton',
                      background=[('active', AppConfig.PRIMARY_ACTIVE)])
        
        # Success button
        self.style.configure('green.TButton', 
                           background=AppConfig.SUCCESS_COLOR, 
                           foreground='white')
        
        # Danger button
        self.style.configure('red.TButton', 
                           background=AppConfig.DANGER_COLOR, 
                           foreground='white')
    
    def _configure_frame_styles(self):
        """Configure frame styles"""
        pass
    
    @staticmethod
    def get_color_palette(n_colors):
        """Get color palette for charts"""
        import matplotlib.pyplot as plt
        import numpy as np
        return plt.cm.viridis(np.linspace(0, 1, n_colors))
    
    @staticmethod
    def get_group_text():
        """Get formatted group member text"""
        members = "\n".join([
            "RAIHAN ALVIAN NURYANSYAH"
        ])
        return f"PEMBUAT:\n{members}"