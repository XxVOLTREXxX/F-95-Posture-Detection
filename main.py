import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from posture_detection import run_posture_detection

class PostureApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("F-95")
        
        # Set the theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to 80% of screen
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Calculate center position
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Create main container
        self.container = ctk.CTkFrame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Initialize pages
        self.pages = {}
        self.create_start_page()
        self.create_main_page()
        
        # Show start page
        self.show_page("start")
        
    def create_start_page(self):
        start_page = ctk.CTkFrame(self.container)
        
        # Welcome text with gradient effect
        welcome_frame = ctk.CTkFrame(start_page, fg_color="transparent")
        welcome_frame.pack(expand=True, fill="both", padx=20, pady=(50, 20))
        
        title = ctk.CTkLabel(
            welcome_frame, 
            text="Welcome to F-95",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            welcome_frame,
            text="Your Personal Posture Assistant",
            font=ctk.CTkFont(family="Helvetica", size=24),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))
        
        # Features section
        features_frame = ctk.CTkFrame(start_page, fg_color="transparent")
        features_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        features = [
            "Real-time Posture Detection",
            "Instant Feedback",
            "Easy to Use Interface",
            "Helps Prevent Back Pain"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=f"✓ {feature}",
                font=ctk.CTkFont(family="Helvetica", size=18),
                text_color="#4CAF50"
            )
            feature_label.pack(pady=10)
        
        # Start button
        start_button = ctk.CTkButton(
            start_page,
            text="Get Started",
            font=ctk.CTkFont(family="Helvetica", size=20),
            width=200,
            height=50,
            corner_radius=25,
            command=lambda: self.show_page("main")
        )
        start_button.pack(pady=(20, 50))
        
        self.pages["start"] = start_page
        
    def create_main_page(self):
        main_page = ctk.CTkFrame(self.container)
        
        # Header
        header = ctk.CTkLabel(
            main_page,
            text="Posture Detection",
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold")
        )
        header.pack(pady=(50, 30))
        
        # Center frame for the button
        center_frame = ctk.CTkFrame(main_page, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Start detection button with hover effect
        start_detection_button = ctk.CTkButton(
            center_frame,
            text="Start Posture Detection",
            font=ctk.CTkFont(family="Helvetica", size=24),
            width=300,
            height=100,
            corner_radius=30,
            command=self.start_detection,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        start_detection_button.pack(pady=20)
        
        # Back button
        back_button = ctk.CTkButton(
            main_page,
            text="Back to Home",
            font=ctk.CTkFont(family="Helvetica", size=16),
            width=150,
            height=40,
            corner_radius=20,
            command=lambda: self.show_page("start"),
            fg_color="#757575",
            hover_color="#616161"
        )
        back_button.pack(pady=(0, 30))
        
        self.pages["main"] = main_page
        
    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()
        
        # Show selected page
        self.pages[page_name].pack(fill="both", expand=True)
        
    def start_detection(self):
        self.root.iconify()  # Minimize the window
        run_posture_detection()
        self.root.deiconify()  # Restore the window
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PostureApp()
    app.run()

