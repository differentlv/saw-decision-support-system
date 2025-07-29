import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseTabView


class InputTabView(BaseTabView):
    """Input tab for entering alternatives, criteria, and decision matrix"""
    
    def create_widgets(self):
        """Create input widgets"""
        self.matrix_entries = []
        
        # Alternatives section
        self._create_alternatives_section()
        
        # Criteria section
        self._create_criteria_section()
        
        # Decision Matrix section
        self._create_matrix_section()
    
    def _create_alternatives_section(self):
        """Create alternatives input section"""
        alt_frame = ttk.LabelFrame(self.scrollable_frame, text="Alternatif Keputusan", padding=10)
        alt_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(alt_frame, text="Nama Alternatif:").pack(anchor='w')
        self.alt_entry = ttk.Entry(alt_frame, width=50)
        self.alt_entry.pack(fill='x', pady=2)
        self.alt_entry.bind('<Return>', lambda e: self.add_alternative())
        
        # Buttons
        alt_button_frame = ttk.Frame(alt_frame)
        alt_button_frame.pack(fill='x', pady=5)
        
        ttk.Button(alt_button_frame, text="Tambah Alternatif", 
                  command=self.add_alternative, style='green.TButton').pack(side='left', padx=5)
        ttk.Button(alt_button_frame, text="Hapus Alternatif", 
                  command=self.remove_alternative, style='red.TButton').pack(side='left', padx=5)
        
        # Listbox with scrollbar
        alt_list_frame = ttk.Frame(alt_frame)
        alt_list_frame.pack(fill='x', pady=5)
        
        self.alt_listbox = tk.Listbox(alt_list_frame, height=4)
        self.alt_listbox.pack(side='left', fill='x', expand=True)
        
        alt_scrollbar = ttk.Scrollbar(alt_list_frame, orient='vertical', command=self.alt_listbox.yview)
        alt_scrollbar.pack(side='right', fill='y')
        
        self.alt_listbox.config(yscrollcommand=alt_scrollbar.set)
    
    def _create_criteria_section(self):
        """Create criteria input section"""
        crit_frame = ttk.LabelFrame(self.scrollable_frame, text="Kriteria Keputusan", padding=10)
        crit_frame.pack(fill='x', padx=10, pady=5)
        
        crit_input_frame = ttk.Frame(crit_frame)
        crit_input_frame.pack(fill='x')
        
        ttk.Label(crit_input_frame, text="Nama Kriteria:").grid(row=0, column=0, sticky='w', padx=5)
        self.crit_entry = ttk.Entry(crit_input_frame, width=30)
        self.crit_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(crit_input_frame, text="Bobot:").grid(row=0, column=2, sticky='w', padx=5)
        self.weight_entry = ttk.Entry(crit_input_frame, width=10)
        self.weight_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(crit_input_frame, text="Tipe:").grid(row=0, column=4, sticky='w', padx=5)
        self.type_var = tk.StringVar(value="benefit")
        type_combo = ttk.Combobox(crit_input_frame, textvariable=self.type_var, 
                                 values=["benefit", "cost"], width=10)
        type_combo.grid(row=0, column=5, padx=5, pady=2)
        
        # Bind Enter key
        self.crit_entry.bind('<Return>', lambda e: self.add_criteria())
        self.weight_entry.bind('<Return>', lambda e: self.add_criteria())
        
        crit_button_frame = ttk.Frame(crit_frame)
        crit_button_frame.pack(fill='x', pady=5)
        
        ttk.Button(crit_button_frame, text="Tambah Kriteria", 
                  command=self.add_criteria, style='green.TButton').pack(side='left', padx=5)
        ttk.Button(crit_button_frame, text="Hapus Kriteria", 
                  command=self.remove_criteria, style='red.TButton').pack(side='left', padx=5)
        
        # Listbox with scrollbar
        crit_list_frame = ttk.Frame(crit_frame)
        crit_list_frame.pack(fill='x', pady=5)
        
        self.crit_listbox = tk.Listbox(crit_list_frame, height=4)
        self.crit_listbox.pack(side='left', fill='x', expand=True)
        
        crit_scrollbar = ttk.Scrollbar(crit_list_frame, orient='vertical', command=self.crit_listbox.yview)
        crit_scrollbar.pack(side='right', fill='y')
        
        self.crit_listbox.config(yscrollcommand=crit_scrollbar.set)
    
    def _create_matrix_section(self):
        """Create decision matrix input section"""
        matrix_frame = ttk.LabelFrame(self.scrollable_frame, text="Matriks Keputusan", padding=10)
        matrix_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Button(matrix_frame, text="Generate Matriks Input", 
                  command=self.generate_matrix).pack(pady=5)
        
        # Matrix container
        self.matrix_container = ttk.Frame(matrix_frame)
        self.matrix_container.pack(fill='both', expand=True, pady=5)
        
        ttk.Button(matrix_frame, text="Simpan Data", 
                  command=self.save_data, style='Accent.TButton').pack(pady=10)
    
    def add_alternative(self):
        """Add new alternative"""
        alt_name = self.alt_entry.get().strip()
        validator = self.get_validator()
        model = self.get_model()
        
        # Validate input
        is_valid, error_msg = validator.validate_alternative_name(alt_name)
        if not is_valid:
            messagebox.showwarning("Peringatan", error_msg)
            return
        
        # Check for duplicates
        if validator.check_duplicate_names(model.alternatives, alt_name):
            messagebox.showwarning("Peringatan", "Nama alternatif sudah ada!")
            return
        
        # Add to model and update UI
        model.alternatives.append(alt_name)
        self.alt_listbox.insert(tk.END, alt_name)
        self.alt_entry.delete(0, tk.END)
        
        # Clear matrix if it exists
        self._clear_matrix()
    
    def remove_alternative(self):
        """Remove selected alternative"""
        selected = self.alt_listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih alternatif yang akan dihapus!")
            return
        
        index = selected[0]
        model = self.get_model()
        model.alternatives.pop(index)
        self.alt_listbox.delete(index)
        
        # Clear matrix if it exists
        self._clear_matrix()
    
    def add_criteria(self):
        """Add new criteria"""
        crit_name = self.crit_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        crit_type = self.type_var.get()
        
        validator = self.get_validator()
        model = self.get_model()
        
        # Validate criteria name
        is_valid, error_msg = validator.validate_criteria_name(crit_name)
        if not is_valid:
            messagebox.showwarning("Peringatan", error_msg)
            return
        
        # Check for duplicates
        if validator.check_duplicate_names(model.criteria, crit_name):
            messagebox.showwarning("Peringatan", "Nama kriteria sudah ada!")
            return
        
        # Validate weight
        is_valid, weight, error_msg = validator.validate_weight(weight_str)
        if not is_valid:
            messagebox.showwarning("Peringatan", error_msg)
            return
        
        # Validate criteria type
        is_valid, error_msg = validator.validate_criteria_type(crit_type)
        if not is_valid:
            messagebox.showwarning("Peringatan", error_msg)
            return
        
        # Add to model and update UI
        model.criteria.append(crit_name)
        model.weights.append(weight)
        model.criteria_types.append(crit_type)
        
        display_text = f"{crit_name} (Bobot: {weight}, Tipe: {crit_type})"
        self.crit_listbox.insert(tk.END, display_text)
        
        # Clear input fields
        self.crit_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        
        # Update sensitivity combo in controller
        self.controller.update_sensitivity_criteria()
        
        # Clear matrix if it exists
        self._clear_matrix()
    
    def remove_criteria(self):
        """Remove selected criteria"""
        selected = self.crit_listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih kriteria yang akan dihapus!")
            return
        
        index = selected[0]
        model = self.get_model()
        model.criteria.pop(index)
        model.weights.pop(index)
        model.criteria_types.pop(index)
        self.crit_listbox.delete(index)
        
        # Update sensitivity combo in controller
        self.controller.update_sensitivity_criteria()
        
        # Clear matrix if it exists
        self._clear_matrix()
    
    def generate_matrix(self):
        """Generate matrix input grid"""
        model = self.get_model()
        
        if not model.alternatives or not model.criteria:
            messagebox.showwarning("Peringatan", "Tambahkan alternatif dan kriteria terlebih dahulu!")
            return
        
        # Clear previous matrix
        self._clear_matrix()
        
        # Create matrix input grid
        self.matrix_entries = []
        
        # Headers
        tk.Label(self.matrix_container, text="Alternatif\\Kriteria", 
                font=('Arial', 10, 'bold'), relief='ridge', bd=1).grid(row=0, column=0, sticky='nsew')
        
        for j, criteria in enumerate(model.criteria):
            tk.Label(self.matrix_container, text=criteria, 
                    font=('Arial', 10, 'bold'), relief='ridge', bd=1).grid(row=0, column=j+1, sticky='nsew')
        
        # Matrix entries
        for i, alternative in enumerate(model.alternatives):
            tk.Label(self.matrix_container, text=alternative, 
                    font=('Arial', 10, 'bold'), relief='ridge', bd=1).grid(row=i+1, column=0, sticky='nsew')
            
            row_entries = []
            for j in range(len(model.criteria)):
                entry = tk.Entry(self.matrix_container, width=10, justify='center')
                entry.grid(row=i+1, column=j+1, padx=1, pady=1)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
        
        # Configure grid weights for resizing
        for i in range(len(model.alternatives) + 1):
            self.matrix_container.grid_rowconfigure(i, weight=1)
        for j in range(len(model.criteria) + 1):
            self.matrix_container.grid_columnconfigure(j, weight=1)
    
    def save_data(self):
        """Save matrix data to model"""
        if not self.matrix_entries:
            messagebox.showwarning("Peringatan", "Generate matriks terlebih dahulu!")
            return
        
        model = self.get_model()
        validator = self.get_validator()
        
        try:
            # Collect matrix data
            decision_matrix = []
            for i, row_entries in enumerate(self.matrix_entries):
                row_data = []
                for j, entry in enumerate(row_entries):
                    value_str = entry.get().strip()
                    if not value_str:
                        messagebox.showerror("Error", f"Nilai pada baris {i+1}, kolom {j+1} kosong!")
                        return
                    
                    is_valid, value, error_msg = validator.validate_matrix_value(value_str)
                    if not is_valid:
                        messagebox.showerror("Error", f"Baris {i+1}, kolom {j+1}: {error_msg}")
                        return
                    
                    row_data.append(value)
                decision_matrix.append(row_data)
            
            # Validate complete data
            is_valid, error_msg = validator.validate_complete_data(
                model.alternatives, model.criteria, model.weights, decision_matrix
            )
            if not is_valid:
                messagebox.showerror("Error", error_msg)
                return
            
            # Set data to model
            model.set_data(
                model.alternatives, 
                model.criteria, 
                model.weights, 
                decision_matrix, 
                model.criteria_types
            )
            
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
            
            # Refresh other views
            self.controller.refresh_all_views()
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def _clear_matrix(self):
        """Clear matrix input grid"""
        for widget in self.matrix_container.winfo_children():
            widget.destroy()
        self.matrix_entries = []