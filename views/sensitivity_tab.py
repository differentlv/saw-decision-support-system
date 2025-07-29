import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from views.base_view import BaseTabView
from utils.chart_utils import SensitivityChartGenerator
from config.settings import AppConfig


class SensitivityTabView(BaseTabView):
    """Sensitivity analysis tab"""
    
    def create_widgets(self):
        """Create sensitivity analysis widgets"""
        # Control frame
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(control_frame, text="Pilih Kriteria:").pack(side='left', padx=5)
        
        self.sens_criteria_var = tk.StringVar()
        self.sens_criteria_combo = ttk.Combobox(control_frame, textvariable=self.sens_criteria_var, 
                                               state="readonly")
        self.sens_criteria_combo.pack(side='left', padx=5)
        
        ttk.Label(control_frame, text="Range Perubahan (0.1 - 1.0):").pack(side='left', padx=5)
        
        self.sens_range_var = tk.DoubleVar(value=AppConfig.DEFAULT_SENSITIVITY_RANGE)
        ttk.Entry(control_frame, textvariable=self.sens_range_var, width=5).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="Analisis Sensitivitas", 
                  command=self.sensitivity_analysis, style='green.TButton').pack(side='left', padx=10)
        
        # Results area
        results_frame = ttk.Frame(self.scrollable_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Text results
        self.sens_text = scrolledtext.ScrolledText(results_frame, font=('Courier', 10), height=12)
        self.sens_text.pack(fill='both', expand=True)
        
        # Chart area
        self.sens_chart_frame = ttk.Frame(results_frame, height=300)
        self.sens_chart_frame.pack(fill='both', expand=True, pady=(10, 0))
    
    def sensitivity_analysis(self):
        """Perform sensitivity analysis"""
        model = self.get_model()
        validator = self.get_validator()
        
        if not model.results or not self.sens_criteria_var.get():
            messagebox.showwarning("Peringatan", 
                                 "Lakukan perhitungan dan pilih kriteria terlebih dahulu!")
            return
        
        # Validate range
        range_str = str(self.sens_range_var.get())
        is_valid, weight_range, error_msg = validator.validate_sensitivity_range(range_str)
        if not is_valid:
            messagebox.showwarning("Peringatan", error_msg)
            return
        
        try:
            selected_criteria = self.sens_criteria_var.get()
            criteria_index = model.criteria.index(selected_criteria)
            
            # Perform sensitivity analysis
            sensitivity_results = model.sensitivity_analysis(criteria_index, weight_range)
            stability_info = model.calculate_stability(sensitivity_results)
            
            # Display results
            self._display_sensitivity_results(selected_criteria, model.weights[criteria_index], 
                                            weight_range, sensitivity_results, stability_info)
            
            # Create chart
            self._create_sensitivity_chart(sensitivity_results, selected_criteria)
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan dalam analisis: {str(e)}")
    
    def _display_sensitivity_results(self, criteria_name, original_weight, weight_range, 
                                   sensitivity_results, stability_info):
        """Display sensitivity analysis results"""
        self.sens_text.delete(1.0, tk.END)
        self.sens_text.insert(tk.END, f"=== ANALISIS SENSITIVITAS ===\n")
        self.sens_text.insert(tk.END, f"Kriteria: {criteria_name}\n")
        self.sens_text.insert(tk.END, f"Bobot Original: {original_weight:.3f}\n")
        self.sens_text.insert(tk.END, f"Range Perubahan: ±{weight_range:.3f}\n\n")
        
        # Results table
        self.sens_text.insert(tk.END, f"{'Perubahan':<12}{'Bobot Baru':<12}{'Alternatif Terbaik':<20}{'Skor':<10}\n")
        self.sens_text.insert(tk.END, "-" * 60 + "\n")
        
        for result in sensitivity_results:
            self.sens_text.insert(tk.END, 
                f"{result['change']:+.3f}       {result['new_weight']:.3f}       "
                f"{result['winner']:<20}{result['score']:.4f}\n")
        
        # Stability analysis
        self.sens_text.insert(tk.END, f"\nSTABILITAS KEPUTUSAN:\n")
        self.sens_text.insert(tk.END, f"Alternatif terbaik asli: {stability_info['original_winner']}\n")
        self.sens_text.insert(tk.END, f"Tingkat stabilitas: {stability_info['stability']:.1f}%\n")
        self.sens_text.insert(tk.END, f"Keputusan {stability_info['level']}\n")
    
    def _create_sensitivity_chart(self, sensitivity_results, criteria_name):
        """Create sensitivity analysis chart"""
        # Clear previous chart
        for widget in self.sens_chart_frame.winfo_children():
            widget.destroy()
        
        if not sensitivity_results:
            return
        
        try:
            chart_generator = SensitivityChartGenerator()
            fig = chart_generator.create_sensitivity_chart(sensitivity_results, criteria_name)
            
            canvas = FigureCanvasTkAgg(fig, self.sens_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat grafik: {str(e)}")
    
    def update_criteria_options(self, criteria_list):
        """Update criteria combo box options"""
        self.sens_criteria_combo['values'] = criteria_list
        if criteria_list:
            self.sens_criteria_combo.current(0)
        else:
            self.sens_criteria_var.set('')
    
    def clear_results(self):
        """Clear results (called from controller)"""
        self.sens_text.delete(1.0, tk.END)
        for widget in self.sens_chart_frame.winfo_children():
            widget.destroy()