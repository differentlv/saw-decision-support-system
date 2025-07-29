import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from views.base_view import BaseTabView
from utils.exporters import ResultExporter
from utils.chart_utils import ChartGenerator


class ResultsTabView(BaseTabView):
    """Results tab for visualization and export"""
    
    def create_widgets(self):
        """Create results widgets"""
        # Controls
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Tampilkan Grafik", 
                  command=self.show_chart, style='green.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="Export Hasil", 
                  command=self.export_results, style='green.TButton').pack(side='left', padx=5)
        
        # Chart container
        self.chart_frame = ttk.Frame(self.scrollable_frame)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    def show_chart(self):
        """Display visualization charts"""
        model = self.get_model()
        
        if not model.results:
            messagebox.showwarning("Peringatan", "Lakukan perhitungan terlebih dahulu!")
            return
        
        try:
            # Clear previous chart
            self._clear_charts()
            
            # Generate charts
            chart_generator = ChartGenerator()
            fig = chart_generator.create_saw_charts(model.results)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan grafik: {str(e)}")
    
    def export_results(self):
        """Export results to file"""
        model = self.get_model()
        
        if not model.results:
            messagebox.showwarning("Peringatan", "Tidak ada hasil untuk diekspor!")
            return
        
        try:
            exporter = ResultExporter()
            filename = exporter.export_to_csv(model.results)
            messagebox.showinfo("Sukses", f"Hasil berhasil diekspor ke {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor: {str(e)}")
    
    def _clear_charts(self):
        """Clear previous charts"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def clear_results(self):
        """Clear results (called from controller)"""
        self._clear_charts()