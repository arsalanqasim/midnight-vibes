#!/usr/bin/env python3
"""
Advanced Image File Converter with GUI
Allows users to select files, choose source and destination formats, and pick output location.
Features: Batch processing, quality settings, preview, file management, and more.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import threading
import os
import json
from datetime import datetime

# Optional: try to enable HEIC/HEIF support if pillow-heif is installed.
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:
    pass

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image File Converter")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Supported formats
        self.supported_formats = {
            "PNG": [".png"],
            "JPEG": [".jpg", ".jpeg"],
            "GIF": [".gif"],
            "BMP": [".bmp"],
            "TIFF": [".tiff", ".tif"],
            "WEBP": [".webp"],
            "HEIC": [".heic", ".heif"]
        }
        
        self.selected_files = []
        self.output_dir = ""
        self.conversion_history = []
        
        # Load settings
        self.load_settings()
        
        self.setup_ui()
    
    def load_settings(self):
        """Load saved settings"""
        try:
            with open("converter_settings.json", "r") as f:
                settings = json.load(f)
                self.output_dir = settings.get("output_dir", "")
                self.quality = settings.get("quality", 95)
                self.resize_enabled = settings.get("resize_enabled", False)
                self.max_width = settings.get("max_width", 1920)
                self.max_height = settings.get("max_height", 1080)
        except FileNotFoundError:
            self.quality = 95
            self.resize_enabled = False
            self.max_width = 1920
            self.max_height = 1080
    
    def save_settings(self):
        """Save current settings"""
        settings = {
            "output_dir": self.output_dir,
            "quality": self.quality,
            "resize_enabled": self.resize_enabled,
            "max_width": self.max_width,
            "max_height": self.max_height
        }
        with open("converter_settings.json", "w") as f:
            json.dump(settings, f)
    
    def setup_ui(self):
        # Create main container with scrollbar
        self.create_main_container()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure main frame grid
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create tabs
        self.create_conversion_tab()
        self.create_batch_tab()
        self.create_settings_tab()
        self.create_history_tab()
        
        # Create bottom control panel
        self.create_bottom_panel()
    
    def create_main_container(self):
        """Create main container with scrollbar"""
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Set main_frame to scrollable_frame
        self.main_frame = self.scrollable_frame
    
    def create_conversion_tab(self):
        """Create the main conversion tab"""
        conversion_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(conversion_frame, text="Convert")
        
        # Configure grid
        conversion_frame.columnconfigure(1, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(conversion_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Browse Files", command=self.browse_files).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Button(file_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        ttk.Button(file_frame, text="Clear All", command=self.clear_files).grid(row=0, column=2, sticky=tk.W)
        
        self.files_label = ttk.Label(file_frame, text="No files selected", foreground="gray")
        self.files_label.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # File list with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=6)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        file_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        file_scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        # Format selection section
        format_frame = ttk.LabelFrame(conversion_frame, text="Format & Quality", padding="10")
        format_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        format_frame.columnconfigure(1, weight=1)
        
        ttk.Label(format_frame, text="From:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.source_format = ttk.Combobox(format_frame, values=["Auto-detect"] + list(self.supported_formats.keys()), state="readonly")
        self.source_format.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        self.source_format.set("Auto-detect")
        
        ttk.Label(format_frame, text="To:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.dest_format = ttk.Combobox(format_frame, values=list(self.supported_formats.keys()), state="readonly")
        self.dest_format.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        self.dest_format.set("PNG")
        
        # Quality settings
        quality_frame = ttk.Frame(format_frame)
        quality_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        quality_frame.columnconfigure(1, weight=1)
        
        ttk.Label(quality_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.quality_var = tk.IntVar(value=self.quality)
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, variable=self.quality_var, orient="horizontal", command=self.update_quality_label)
        self.quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.quality_label = ttk.Label(quality_frame, text=f"{self.quality}%")
        self.quality_label.grid(row=0, column=2, sticky=tk.W)
        
        # Resize options
        resize_frame = ttk.LabelFrame(conversion_frame, text="Resize Options", padding="10")
        resize_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        resize_frame.columnconfigure(1, weight=1)
        resize_frame.columnconfigure(3, weight=1)
        
        self.resize_var = tk.BooleanVar(value=self.resize_enabled)
        ttk.Checkbutton(resize_frame, text="Enable resizing", variable=self.resize_var, command=self.toggle_resize).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(resize_frame, text="Max Width:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.width_var = tk.IntVar(value=self.max_width)
        self.width_entry = ttk.Entry(resize_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        ttk.Label(resize_frame, text="Max Height:").grid(row=1, column=2, sticky=tk.W, padx=(20, 10), pady=(10, 0))
        self.height_var = tk.IntVar(value=self.max_height)
        self.height_entry = ttk.Entry(resize_frame, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=1, column=3, sticky=tk.W, pady=(10, 0))
        
        # Output directory section
        output_frame = ttk.LabelFrame(conversion_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Button(output_frame, text="Browse Folder", command=self.browse_output_dir).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_label = ttk.Label(output_frame, text="No output directory selected", foreground="gray")
        self.output_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Options section
        options_frame = ttk.LabelFrame(conversion_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.overwrite_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Overwrite existing files", variable=self.overwrite_var).grid(row=0, column=0, sticky=tk.W)
        
        self.preserve_structure_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve folder structure", variable=self.preserve_structure_var).grid(row=1, column=0, sticky=tk.W)
        
        self.add_metadata_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve metadata", variable=self.add_metadata_var).grid(row=2, column=0, sticky=tk.W)
    
    def create_batch_tab(self):
        """Create batch processing tab"""
        batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(batch_frame, text="Batch")
        
        batch_frame.columnconfigure(0, weight=1)
        
        # Batch operations
        ttk.Label(batch_frame, text="Batch Operations", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Quick convert buttons
        quick_frame = ttk.LabelFrame(batch_frame, text="Quick Convert", padding="10")
        quick_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(quick_frame, text="HEIC → PNG", command=lambda: self.quick_convert("HEIC", "PNG")).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(quick_frame, text="JPEG → PNG", command=lambda: self.quick_convert("JPEG", "PNG")).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(quick_frame, text="PNG → JPEG", command=lambda: self.quick_convert("PNG", "JPEG")).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(quick_frame, text="All → WEBP", command=lambda: self.quick_convert("Auto-detect", "WEBP")).grid(row=0, column=3)
        
        # Batch folder processing
        folder_frame = ttk.LabelFrame(batch_frame, text="Folder Processing", padding="10")
        folder_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        ttk.Label(folder_frame, text="Source Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.batch_source_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.batch_source_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(folder_frame, text="Browse", command=self.browse_batch_source).grid(row=0, column=2)
        
        ttk.Label(folder_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.batch_output_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.batch_output_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        ttk.Button(folder_frame, text="Browse", command=self.browse_batch_output).grid(row=1, column=2, pady=(10, 0))
        
        ttk.Button(folder_frame, text="Process Entire Folder", command=self.process_folder).grid(row=2, column=0, columnspan=3, pady=(20, 0))
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="Settings")
        
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Application Settings", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Default settings
        default_frame = ttk.LabelFrame(settings_frame, text="Default Settings", padding="10")
        default_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        default_frame.columnconfigure(1, weight=1)
        
        ttk.Label(default_frame, text="Default Output Format:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.default_format = ttk.Combobox(default_frame, values=list(self.supported_formats.keys()), state="readonly")
        self.default_format.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.default_format.set("PNG")
        
        ttk.Label(default_frame, text="Default Quality:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.default_quality_var = tk.IntVar(value=95)
        ttk.Scale(default_frame, from_=1, to=100, variable=self.default_quality_var, orient="horizontal").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Save/Load settings
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).grid(row=2, column=0, sticky=tk.W, pady=20)
        ttk.Button(settings_frame, text="Reset to Defaults", command=self.reset_settings).grid(row=2, column=1, sticky=tk.W, pady=20)
    
    def create_history_tab(self):
        """Create conversion history tab"""
        history_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(history_frame, text="History")
        
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)
        
        ttk.Label(history_frame, text="Conversion History", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # History list
        history_list_frame = ttk.Frame(history_frame)
        history_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_list_frame.columnconfigure(0, weight=1)
        history_list_frame.rowconfigure(0, weight=1)
        
        self.history_listbox = tk.Listbox(history_list_frame)
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        history_scrollbar = ttk.Scrollbar(history_list_frame, orient="vertical", command=self.history_listbox.yview)
        history_scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
        
        # History controls
        history_controls = ttk.Frame(history_frame)
        history_controls.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(history_controls, text="Clear History", command=self.clear_history).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(history_controls, text="Export History", command=self.export_history).grid(row=0, column=1)
    
    def create_bottom_panel(self):
        """Create bottom control panel with progress and convert button"""
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        
        # Progress section
        progress_frame = ttk.Frame(bottom_frame)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to convert")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Control buttons
        control_frame = ttk.Frame(bottom_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.convert_button = ttk.Button(control_frame, text="Convert Files", command=self.start_conversion, style="Accent.TButton")
        self.convert_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_conversion, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        self.preview_button = ttk.Button(control_frame, text="Preview", command=self.show_preview)
        self.preview_button.grid(row=0, column=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(bottom_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def browse_files(self):
        filetypes = [
            ("All Images", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.tif *.webp *.heic *.heif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff *.tif"),
            ("WEBP files", "*.webp"),
            ("HEIC files", "*.heic *.heif"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select image files to convert",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files.extend(list(files))
            self.update_file_list()
    
    def browse_folder(self):
        """Browse and add all images from a folder"""
        folder = filedialog.askdirectory(title="Select folder containing images")
        if folder:
            folder_path = Path(folder)
            image_files = []
            for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif"]:
                image_files.extend(folder_path.rglob(f"*{ext}"))
                image_files.extend(folder_path.rglob(f"*{ext.upper()}"))
            
            if image_files:
                self.selected_files.extend([str(f) for f in image_files])
                self.update_file_list()
            else:
                messagebox.showinfo("No Images", "No image files found in the selected folder.")
    
    def clear_files(self):
        """Clear all selected files"""
        self.selected_files = []
        self.update_file_list()
    
    def update_file_list(self):
        """Update the file list display"""
        if not self.selected_files:
            self.files_label.config(text="No files selected", foreground="gray")
            self.file_listbox.delete(0, tk.END)
        else:
            file_count = len(self.selected_files)
            self.files_label.config(text=f"{file_count} files selected", foreground="black")
            
            # Update listbox
            self.file_listbox.delete(0, tk.END)
            for file_path in self.selected_files:
                self.file_listbox.insert(tk.END, Path(file_path).name)
    
    def toggle_resize(self):
        """Toggle resize controls"""
        state = "normal" if self.resize_var.get() else "disabled"
        self.width_entry.config(state=state)
        self.height_entry.config(state=state)
    
    def browse_batch_source(self):
        """Browse for batch source folder"""
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.batch_source_var.set(folder)
    
    def browse_batch_output(self):
        """Browse for batch output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.batch_output_var.set(folder)
    
    def quick_convert(self, source_format, dest_format):
        """Quick convert with predefined settings"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        
        # Set formats
        self.source_format.set(source_format)
        self.dest_format.set(dest_format)
        
        # Set output directory if not set
        if not self.output_dir:
            self.output_dir = str(Path(self.selected_files[0]).parent / "converted")
            self.output_label.config(text=f"Output: {Path(self.output_dir).name}", foreground="black")
        
        # Start conversion
        self.start_conversion()
    
    def process_folder(self):
        """Process entire folder"""
        source_folder = self.batch_source_var.get()
        output_folder = self.batch_output_var.get()
        
        if not source_folder or not output_folder:
            messagebox.showerror("Error", "Please select both source and output folders.")
            return
        
        # Find all image files in source folder
        source_path = Path(source_folder)
        image_files = []
        for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif"]:
            image_files.extend(source_path.rglob(f"*{ext}"))
            image_files.extend(source_path.rglob(f"*{ext.upper()}"))
        
        if not image_files:
            messagebox.showinfo("No Images", "No image files found in the source folder.")
            return
        
        # Set files and output directory
        self.selected_files = [str(f) for f in image_files]
        self.output_dir = output_folder
        self.output_label.config(text=f"Output: {Path(output_folder).name}", foreground="black")
        
        # Update file list
        self.update_file_list()
        
        # Start conversion
        self.start_conversion()
    
    def reset_settings(self):
        """Reset settings to defaults"""
        self.quality = 95
        self.resize_enabled = False
        self.max_width = 1920
        self.max_height = 1080
        self.default_format.set("PNG")
        self.default_quality_var.set(95)
        messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")
    
    def clear_history(self):
        """Clear conversion history"""
        self.conversion_history = []
        self.history_listbox.delete(0, tk.END)
        messagebox.showinfo("History Cleared", "Conversion history has been cleared.")
    
    def export_history(self):
        """Export conversion history to file"""
        if not self.conversion_history:
            messagebox.showinfo("No History", "No conversion history to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export History",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write("Image Conversion History\n")
                    f.write("=" * 50 + "\n\n")
                    for entry in self.conversion_history:
                        f.write(f"Date: {entry['date']}\n")
                        f.write(f"Files: {entry['file_count']}\n")
                        f.write(f"From: {entry['source_format']} → To: {entry['dest_format']}\n")
                        f.write(f"Successful: {entry['successful']}, Failed: {entry['failed']}\n")
                        f.write("-" * 30 + "\n")
                messagebox.showinfo("Success", f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history: {str(e)}")
    
    def show_preview(self):
        """Show preview of selected files"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("File Preview")
        preview_window.geometry("600x400")
        
        # File list with preview
        list_frame = ttk.Frame(preview_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File listbox
        file_listbox = tk.Listbox(list_frame)
        file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Preview frame
        preview_frame = ttk.Frame(list_frame)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        preview_label = ttk.Label(preview_frame, text="Select a file to preview")
        preview_label.pack(expand=True)
        
        # Populate file list
        for file_path in self.selected_files:
            file_listbox.insert(tk.END, Path(file_path).name)
        
        def show_file_preview(event):
            selection = file_listbox.curselection()
            if selection:
                file_path = self.selected_files[selection[0]]
                try:
                    with Image.open(file_path) as img:
                        # Resize for preview
                        img.thumbnail((300, 300))
                        photo = ImageTk.PhotoImage(img)
                        preview_label.config(image=photo, text="")
                        preview_label.image = photo  # Keep a reference
                except Exception as e:
                    preview_label.config(image="", text=f"Preview error:\n{str(e)}")
        
        file_listbox.bind("<<ListboxSelect>>", show_file_preview)
    
    def stop_conversion(self):
        """Stop the current conversion"""
        self.conversion_stopped = True
        self.stop_button.config(state="disabled")
        self.convert_button.config(state="normal")
        self.progress_var.set("Conversion stopped by user")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"Output: {Path(directory).name}", foreground="black")
    
    def get_file_format(self, file_path):
        """Detect file format from extension"""
        ext = Path(file_path).suffix.lower()
        for format_name, extensions in self.supported_formats.items():
            if ext in extensions:
                return format_name
        return "Unknown"
    
    def convert_file(self, src_path, dst_path, dest_format):
        """Convert a single file with enhanced features"""
        try:
            # Ensure parent directory exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists and overwrite is disabled
            if dst_path.exists() and not self.overwrite_var.get():
                return f"Skipped (exists): {dst_path.name}"
            
            with Image.open(src_path) as img:
                # Store original metadata if requested
                metadata = {}
                if self.add_metadata_var.get():
                    metadata = img.info.copy()
                
                # Convert to RGB/RGBA based on transparency
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGBA")
                elif img.mode == "P":
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                
                # Apply resizing if enabled
                if self.resize_var.get():
                    max_width = self.width_var.get()
                    max_height = self.height_var.get()
                    
                    if img.width > max_width or img.height > max_height:
                        # Calculate new size maintaining aspect ratio
                        ratio = min(max_width / img.width, max_height / img.height)
                        new_width = int(img.width * ratio)
                        new_height = int(img.height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Get current quality setting
                current_quality = self.quality_var.get()
                
                # Save in the requested format
                save_kwargs = {"format": dest_format}
                
                # Format-specific options
                if dest_format == "JPEG":
                    save_kwargs["quality"] = current_quality
                    save_kwargs["optimize"] = True
                    # Remove alpha channel for JPEG
                    if img.mode == "RGBA":
                        # Create white background
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                elif dest_format == "PNG":
                    save_kwargs["optimize"] = True
                elif dest_format == "WEBP":
                    save_kwargs["quality"] = current_quality
                    save_kwargs["method"] = 6
                elif dest_format == "TIFF":
                    save_kwargs["compression"] = "tiff_lzw"
                
                # Add metadata if preserving
                if metadata and dest_format in ["PNG", "TIFF"]:
                    save_kwargs.update(metadata)
                
                img.save(dst_path, **save_kwargs)
                return f"Converted: {src_path.name} -> {dst_path.name}"
                
        except Exception as e:
            return f"Failed: {src_path.name} - {str(e)}"
    
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if not self.selected_files:
            messagebox.showerror("Error", "Please select files to convert")
            return
        
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        dest_format = self.dest_format.get()
        if not dest_format:
            messagebox.showerror("Error", "Please select a destination format")
            return
        
        # Initialize conversion state
        self.conversion_stopped = False
        
        # Disable/enable buttons
        self.convert_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Update quality from scale
        self.quality = self.quality_var.get()
        self.quality_label.config(text=f"{self.quality}%")
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_files, args=(dest_format,))
        thread.daemon = True
        thread.start()
    
    def convert_files(self, dest_format):
        """Convert all selected files with enhanced features"""
        total_files = len(self.selected_files)
        successful = 0
        failed = 0
        skipped = 0
        
        self.progress_bar.config(maximum=total_files)
        
        # Record conversion start
        start_time = datetime.now()
        
        for i, src_path in enumerate(self.selected_files):
            if self.conversion_stopped:
                break
                
            src_path = Path(src_path)
            
            # Update progress
            self.root.after(0, lambda p=src_path.name: self.progress_var.set(f"Converting {p}..."))
            self.root.after(0, lambda v=i: self.progress_bar.config(value=v))
            self.root.after(0, lambda: self.status_var.set(f"Processing {i+1}/{total_files}"))
            
            # Determine destination path
            if self.preserve_structure_var.get():
                # Preserve folder structure
                rel_path = src_path.relative_to(src_path.parents[0])
                dst_path = Path(self.output_dir) / rel_path
            else:
                # Flat structure
                dst_path = Path(self.output_dir) / src_path.name
            
            # Change extension to destination format
            dst_path = dst_path.with_suffix(f".{dest_format.lower()}")
            
            # Convert file
            result = self.convert_file(src_path, dst_path, dest_format)
            
            if "Failed:" in result:
                failed += 1
            elif "Skipped:" in result:
                skipped += 1
            else:
                successful += 1
        
        # Record conversion end
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Add to history
        history_entry = {
            "date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_count": total_files,
            "source_format": self.source_format.get(),
            "dest_format": dest_format,
            "successful": successful,
            "failed": failed,
            "skipped": skipped,
            "duration": str(duration).split('.')[0]
        }
        self.conversion_history.append(history_entry)
        
        # Update history display
        self.root.after(0, lambda: self.update_history_display())
        
        # Update final progress
        self.root.after(0, lambda: self.progress_bar.config(value=total_files))
        self.root.after(0, lambda: self.progress_var.set(f"Complete! {successful} successful, {failed} failed, {skipped} skipped"))
        self.root.after(0, lambda: self.status_var.set("Ready"))
        
        # Re-enable buttons
        self.root.after(0, lambda: self.convert_button.config(state="normal"))
        self.root.after(0, lambda: self.stop_button.config(state="disabled"))
        
        # Show completion message
        if failed == 0 and skipped == 0:
            self.root.after(0, lambda: messagebox.showinfo("Success", f"All {successful} files converted successfully in {duration}!"))
        elif failed == 0:
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Converted {successful} files successfully, {skipped} skipped in {duration}!"))
        else:
            self.root.after(0, lambda: messagebox.showwarning("Partial Success", f"Converted {successful} files successfully, {failed} failed, {skipped} skipped in {duration}"))
    
    def update_history_display(self):
        """Update the history listbox display"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.conversion_history[-10:]):  # Show last 10 entries
            display_text = f"{entry['date']} - {entry['file_count']} files ({entry['successful']}✓, {entry['failed']}✗)"
            self.history_listbox.insert(tk.END, display_text)
    
    def update_quality_label(self, value):
        """Update quality label when scale changes"""
        self.quality_label.config(text=f"{int(float(value))}%")

def main():
    root = tk.Tk()
    app = ImageConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
