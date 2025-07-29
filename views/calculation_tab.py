import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from views.base_view import BaseTabView


class CalculationTabView(BaseTabView):
    """Calculation tab for SAW method calculations"""
    
    def create_widgets(self):
        """Create calculation widgets"""
        # Calculation controls
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Hitung SAW", 
                  command=self.calculate_saw, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="Reset", 
                  command=self.reset_calculation, style='red.TButton').pack(side='left', padx=5)
        
        # Results display
        self.calc_text = scrolledtext.ScrolledText(self.scrollable_frame, height=30, 
                                                  font=('Courier', 10))
        self.calc_text.pack(fill='both', expand=True, padx=10, pady=5)
    
    def calculate_saw(self):
        """Perform SAW calculation and display results"""
        model = self.get_model()
        
        if not model.decision_matrix:
            messagebox.showwarning("Peringatan", "Simpan data terlebih dahulu!")
            return
        
        try:
            # Clear previous results
            self.calc_text.delete(1.0, tk.END)
            
            # Get calculation steps
            steps = model.get_calculation_steps()
            
            # Display calculation steps
            self._display_calculation_steps(steps)
            
            messagebox.showinfo("Sukses", "Perhitungan SAW selesai!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan dalam perhitungan: {str(e)}")
    
    def _display_calculation_steps(self, steps):
        """Display detailed calculation steps"""
        self.calc_text.insert(tk.END, "=== PERHITUNGAN METODE SAW ===\n\n")
        
        # Step 1: Original matrix
        self._display_original_matrix(steps)
        
        # Step 2: Normalization
        self._display_normalization(steps)
        
        # Step 3: Calculate weighted scores
        self._display_score_calculation(steps)
        
        # Step 4: Final ranking
        self._display_ranking(steps)
    
    def _display_original_matrix(self, steps):
        """Display original decision matrix"""
        self.calc_text.insert(tk.END, "1. MATRIKS KEPUTUSAN AWAL:\n")
        self.calc_text.insert(tk.END, f"{'Alternatif':<15}")
        
        for criteria in steps['criteria']:
            self.calc_text.insert(tk.END, f"{criteria:<12}")
        self.calc_text.insert(tk.END, "\n")
        
        matrix = steps['original_matrix']
        for i, alt in enumerate(steps['alternatives']):
            self.calc_text.insert(tk.END, f"{alt:<15}")
            for j in range(len(steps['criteria'])):
                self.calc_text.insert(tk.END, f"{matrix[i,j]:<12.3f}")
            self.calc_text.insert(tk.END, "\n")
    
    def _display_normalization(self, steps):
        """Display normalization process"""
        self.calc_text.insert(tk.END, "\n2. NORMALISASI MATRIKS:\n")
        
        matrix = steps['original_matrix']
        normalized_matrix = steps['normalized_matrix']
        
        # Show normalization formula for each criteria
        for j, criteria in enumerate(steps['criteria']):
            if steps['criteria_types'][j] == 'benefit':
                max_val = np.max(matrix[:, j])
                self.calc_text.insert(tk.END, 
                    f"Kriteria {criteria} (Benefit): R_ij = X_ij / {max_val:.3f}\n")
            else:
                min_val = np.min(matrix[:, j])
                self.calc_text.insert(tk.END, 
                    f"Kriteria {criteria} (Cost): R_ij = {min_val:.3f} / X_ij\n")
        
        # Show normalized matrix
        self.calc_text.insert(tk.END, "\nMatriks Ternormalisasi:\n")
        self.calc_text.insert(tk.END, f"{'Alternatif':<15}")
        
        for criteria in steps['criteria']:
            self.calc_text.insert(tk.END, f"{criteria:<12}")
        self.calc_text.insert(tk.END, "\n")
        
        for i, alt in enumerate(steps['alternatives']):
            self.calc_text.insert(tk.END, f"{alt:<15}")
            for j in range(len(steps['criteria'])):
                self.calc_text.insert(tk.END, f"{normalized_matrix[i,j]:<12.3f}")
            self.calc_text.insert(tk.END, "\n")
    
    def _display_score_calculation(self, steps):
        """Display score calculation process"""
        self.calc_text.insert(tk.END, "\n3. PERHITUNGAN SKOR AKHIR:\n")
        self.calc_text.insert(tk.END, "Bobot Kriteria:\n")
        
        for criteria, weight in zip(steps['criteria'], steps['weights']):
            self.calc_text.insert(tk.END, f"{criteria}: {weight:.3f}\n")
        
        self.calc_text.insert(tk.END, "\nFormula: Si = Σ(Wj × Rij)\n\n")
        
        normalized_matrix = steps['normalized_matrix']
        weights = steps['weights']
        
        for i, alt in enumerate(steps['alternatives']):
            self.calc_text.insert(tk.END, f"{alt}: ")
            calculation = " + ".join([f"({weights[j]:.3f} × {normalized_matrix[i,j]:.3f})" 
                                    for j in range(len(steps['criteria']))])
            score = np.sum(weights * normalized_matrix[i, :])
            self.calc_text.insert(tk.END, f"{calculation} = {score:.4f}\n")
    
    def _display_ranking(self, steps):
        """Display final ranking"""
        self.calc_text.insert(tk.END, "\n4. PERINGKAT AKHIR:\n")
        self.calc_text.insert(tk.END, f"{'Peringkat':<10}{'Alternatif':<20}{'Skor':<15}\n")
        self.calc_text.insert(tk.END, "-" * 45 + "\n")
        
        scores = steps['scores']
        for rank, (alt, score) in enumerate(scores, 1):
            self.calc_text.insert(tk.END, f"{rank:<10}{alt:<20}{score:<15.4f}\n")
    
    def reset_calculation(self):
        """Reset calculation results"""
        self.calc_text.delete(1.0, tk.END)
        model = self.get_model()
        model.results = []
        model.normalized_matrix = None
    
    def clear_results(self):
        """Clear results (called from controller)"""
        self.calc_text.delete(1.0, tk.END)