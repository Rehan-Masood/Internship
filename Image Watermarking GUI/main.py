import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class WatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PNG/JPG Watermark Studio Pro")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # File state variables
        self.image_path = None
        self.original_image = None
        self.preview_image = None

        # UI Layout setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_preview_panel()

    def _create_sidebar(self):
        """Creates control sidebar for watermark configuration."""
        sidebar = ctk.CTkFrame(self, width=320, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            sidebar, text="Watermark Controls", font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(padx=20, pady=(20, 10))

        # 1. Load Image Button
        self.btn_load = ctk.CTkButton(
            sidebar, text="📁 Open Image", command=self.load_image, height=40
        )
        self.btn_load.pack(padx=20, pady=10, fill="x")

        # 2. Text Input Entry
        ctk.CTkLabel(sidebar, text="Watermark Text:", anchor="w").pack(
            padx=20, pady=(15, 2), fill="x"
        )
        self.entry_text = ctk.CTkEntry(
            sidebar, placeholder_text="e.g. © 2026 Dev Studio"
        )
        self.entry_text.insert(0, "© 2026 Developer Portfolio")
        self.entry_text.pack(padx=20, pady=5, fill="x")
        self.entry_text.bind("<KeyRelease>", lambda event: self.update_preview())

        # 3. Font Size Slider
        ctk.CTkLabel(sidebar, text="Font Size:", anchor="w").pack(
            padx=20, pady=(15, 2), fill="x"
        )
        self.slider_size = ctk.CTkSlider(
            sidebar, from_=10, to=150, number_of_steps=140, command=self.update_preview
        )
        self.slider_size.set(40)
        self.slider_size.pack(padx=20, pady=5, fill="x")

        # 4. Opacity Slider
        ctk.CTkLabel(sidebar, text="Opacity / Transparency:", anchor="w").pack(
            padx=20, pady=(15, 2), fill="x"
        )
        self.slider_opacity = ctk.CTkSlider(
            sidebar, from_=10, to=255, number_of_steps=245, command=self.update_preview
        )
        self.slider_opacity.set(128)
        self.slider_opacity.pack(padx=20, pady=5, fill="x")

        # 5. Position Selection Dropdown
        ctk.CTkLabel(sidebar, text="Watermark Position:", anchor="w").pack(
            padx=20, pady=(15, 2), fill="x"
        )
        self.option_position = ctk.CTkOptionMenu(
            sidebar,
            values=[
                "Bottom-Right",
                "Bottom-Left",
                "Top-Right",
                "Top-Left",
                "Center",
            ],
            command=self.update_preview,
        )
        self.option_position.set("Bottom-Right")
        self.option_position.pack(padx=20, pady=5, fill="x")

        # 6. Export Button
        self.btn_export = ctk.CTkButton(
            sidebar,
            text="💾 Export Image",
            command=self.export_image,
            fg_color="#22c55e",
            hover_color="#16a34a",
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.btn_export.pack(padx=20, pady=(30, 20), fill="x")

    def _create_preview_panel(self):
        """Creates main canvas preview region."""
        self.preview_frame = ctk.CTkFrame(self, corner_radius=10)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No Image Loaded\nClick 'Open Image' to start",
            font=ctk.CTkFont(size=16),
        )
        self.preview_label.grid(row=0, column=0, padx=20, pady=20)

    def load_image(self):
        """Loads an image file into memory."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path).convert("RGBA")
            self.update_preview()

    def generate_watermarked_image(self):
        """Applies text watermark based on current controls."""
        if not self.original_image:
            return None

        base = self.original_image.copy()
        txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        text = self.entry_text.get()
        font_size = int(self.slider_size.get())
        opacity = int(self.slider_opacity.get())
        position_mode = self.option_position.get()

        # Load standard font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        # Calculate text bounding dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        width, height = base.size
        margin = 30

        # Position placement logic
        if position_mode == "Bottom-Right":
            x = width - text_width - margin
            y = height - text_height - margin
        elif position_mode == "Bottom-Left":
            x = margin
            y = height - text_height - margin
        elif position_mode == "Top-Right":
            x = width - text_width - margin
            y = margin
        elif position_mode == "Top-Left":
            x = margin
            y = margin
        else:  # Center
            x = (width - text_width) // 2
            y = (height - text_height) // 2

        # Draw semi-transparent white text
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

        # Composite original image with watermark layer
        watermarked = Image.alpha_composite(base, txt_layer)
        return watermarked

    def update_preview(self, *args):
        """Renders processed preview image on canvas."""
        watermarked = self.generate_watermarked_image()
        if watermarked is None:
            return

        # Scale image dynamically to fit preview frame dimensions
        preview_w = self.preview_frame.winfo_width() - 40
        preview_h = self.preview_frame.winfo_height() - 40

        if preview_w < 100 or preview_h < 100:
            preview_w, preview_h = 600, 500

        preview_copy = watermarked.copy()
        preview_copy.thumbnail((preview_w, preview_h), Image.Resampling.LANCZOS)

        ctk_img = ctk.CTkImage(
            light_image=preview_copy, dark_image=preview_copy, size=preview_copy.size
        )

        self.preview_label.configure(image=ctk_img, text="")
        self.preview_label.image = ctk_img

    def export_image(self):
        """Saves final watermarked image to user selected directory."""
        if not self.original_image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        final_img = self.generate_watermarked_image()
        if final_img:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("All Files", "*.*"),
                ],
            )
            if save_path:
                # Convert back to RGB if saving as JPEG
                if save_path.lower().endswith((".jpg", ".jpeg")):
                    final_img = final_img.convert("RGB")

                final_img.save(save_path)
                messagebox.showinfo(
                    "Success", f"Watermarked image exported successfully to:\n{save_path}"
                )


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()