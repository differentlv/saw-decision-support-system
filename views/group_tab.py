import tkinter as tk
from views.base_view import BaseTabView


class GroupTabView(BaseTabView):
    """Group information tab"""
    
    def create_widgets(self):
        """Create group information widgets"""
        group_text = "RAIHAN ALVIAN NURYANSYAH"
        
        label = tk.Label(
            self.scrollable_frame,
            text=group_text,
            font=("Arial", 14, "bold"),
            justify="center",
            bg='#f0f0f0'
        )
        label.pack(expand=True, fill="both")