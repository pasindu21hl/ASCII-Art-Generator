import tkinter as tk
from tkinter import filedialog, Scale, Button, HORIZONTAL, Text, Scrollbar, Checkbutton, Label, Frame, StringVar, OptionMenu
from PIL import Image, ImageEnhance, ImageOps, ImageTk
import numpy as np

class AsciiArtGenerator:
    ASCII_SETS = {
        "Standard": "@QB#NgWM8RDHdOKq9$6khEPXwmeZaoS2yjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,'.-` ",
        "Simple": "Ñ@#W$9876543210?!abc;:+=-,._    ",
        "Blocks": "▓▒░:.",
        "Detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        "Lines": "||--__||--"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.image_path = None
        self.original_image = None

        # --- Main layout ---
        # Status bar
        self.status_var = StringVar()
        self.status_bar = Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Welcome! Select an image to start.")

        # Main frame
        main_frame = Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Controls frame
        controls_frame = Frame(main_frame, bd=2, relief=tk.GROOVE)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=0)

        # Right frame for previews
        right_frame = Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Image preview frame
        image_preview_frame = Frame(right_frame, bd=2, relief=tk.GROOVE)
        image_preview_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        Label(image_preview_frame, text="Image Preview", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.image_preview_label = Label(image_preview_frame)
        self.image_preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ASCII preview frame
        ascii_preview_frame = Frame(right_frame, bd=2, relief=tk.GROOVE)
        ascii_preview_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Controls ---
        Label(controls_frame, text="Settings", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.width_slider = self._create_slider(controls_frame, "Width:", 1, 50, 300, 180)
        self.contrast_slider = self._create_slider(controls_frame, "Contrast:", 2, 0.5, 3.0, 1.7, 0.1)
        self.brightness_slider = self._create_slider(controls_frame, "Brightness:", 3, 0.5, 2.0, 1.2, 0.1)
        self.gamma_slider = self._create_slider(controls_frame, "Gamma:", 4, 0.5, 2.0, 1.0, 0.1)
        self.aspect_slider = self._create_slider(controls_frame, "Height Factor:", 5, 0.3, 1.0, 0.5, 0.05)

        self.font_size_slider = self._create_slider(controls_frame, "Font Size:", 6, 2, 16, 6)

        self.invert_var = tk.BooleanVar()
        Checkbutton(controls_frame, text="Invert Colors", variable=self.invert_var, command=self.update_preview).grid(row=7, column=0, columnspan=2, pady=5, sticky="w", padx=5)

        self.color_var = tk.BooleanVar()
        Checkbutton(controls_frame, text="Enable Color", variable=self.color_var, command=self.update_preview).grid(row=8, column=0, columnspan=2, pady=5, sticky="w", padx=5)

        self.dither_var = tk.BooleanVar()
        Checkbutton(controls_frame, text="Dithering", variable=self.dither_var, command=self.update_preview).grid(row=9, column=0, columnspan=2, pady=5, sticky="w", padx=5)

        Label(controls_frame, text="Character Set:").grid(row=10, column=0, sticky="w", padx=5)
        self.ascii_set_var = StringVar(value="Standard")
        self.ascii_set_menu = OptionMenu(controls_frame, self.ascii_set_var, *self.ASCII_SETS.keys(), command=lambda _: self.update_preview())
        self.ascii_set_menu.grid(row=10, column=1, pady=5, sticky="ew", padx=5)

        Button(controls_frame, text="Manage Sets", command=self.manage_char_sets).grid(row=11, column=0, columnspan=2, pady=5, sticky="ew", padx=5)

        # Action buttons frame
        button_frame = Frame(controls_frame)
        button_frame.grid(row=12, column=0, columnspan=2, pady=20)
        Button(button_frame, text="Select Image", command=self.select_image).pack(fill=tk.X, pady=2)
        Button(button_frame, text="Save to File", command=self.save_to_file).pack(fill=tk.X, pady=2)
        Button(button_frame, text="Save as HTML", command=self.save_as_html).pack(fill=tk.X, pady=2)
        Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(fill=tk.X, pady=2)

        # --- ASCII Preview ---
        Label(ascii_preview_frame, text="ASCII Preview", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.preview_text = Text(ascii_preview_frame, wrap=tk.WORD, font=("Courier", 6), bg="#2B2B2B", fg="#A9B7C6", insertbackground="white")
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = Scrollbar(self.preview_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.preview_text.yview)

    def _create_slider(self, parent, label, row, from_, to, default, resolution=1):
        Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        slider = Scale(parent, from_=from_, to=to, orient=HORIZONTAL, resolution=resolution, command=lambda _: self.update_preview())
        slider.set(default)
        slider.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        parent.grid_columnconfigure(1, weight=1)
        return slider

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            self.image_path = file_path
            try:
                self.original_image = Image.open(self.image_path)
                self.set_status(f"Image loaded: {file_path.split('/')[-1]}")
                self.update_image_preview()
                self.update_preview()
            except Exception as e:
                self.set_status(f"Error opening image: {e}")
                self.original_image = None

    def update_preview(self, *args):
        if not self.original_image:
            return

        self.update_image_preview()
        self.preview_text.config(font=("Courier", self.font_size_slider.get()))
        new_width = self.width_slider.get()
        
        # Clear previous content and tags
        self.preview_text.delete(1.0, tk.END)
        for tag in self.preview_text.tag_names():
            if tag != "sel":
                self.preview_text.tag_delete(tag)

        if self.color_var.get():
            self.update_preview_color(new_width)
        else:
            self.update_preview_monochrome(new_width)
        
        self.set_status("Preview updated.")

    def manage_char_sets(self):
        manager = CharSetManager(self.root, self.ASCII_SETS)
        self.root.wait_window(manager.top)
        if manager.new_sets:
            self.ASCII_SETS = manager.new_sets
            # Update the OptionMenu
            menu = self.ascii_set_menu["menu"]
            menu.delete(0, "end")
            for name in self.ASCII_SETS.keys():
                menu.add_command(label=name, command=lambda value=name: self.ascii_set_var.set(value))
            self.ascii_set_var.set(list(self.ASCII_SETS.keys())[0])
            self.update_preview()

    def update_image_preview(self):
        if not self.original_image:
            return
        
        image = self.original_image.copy()
        image.thumbnail((300, 300))
        self.img_tk = ImageTk.PhotoImage(image)
        self.image_preview_label.config(image=self.img_tk)

    def update_preview_color(self, new_width):
        image = self._resize_image(self.original_image.copy(), new_width, self.aspect_slider.get())
        
        # Enhance before getting colors
        image = ImageEnhance.Contrast(image).enhance(self.contrast_slider.get())
        image = ImageEnhance.Brightness(image).enhance(self.brightness_slider.get())
        
        # Get color data before converting to grayscale for character selection
        color_pixels = np.array(image.convert("RGB"))
        
        # Grayscale for character mapping
        gray_image = image.convert("L")
        
        if self.dither_var.get():
            pixels = self.floyd_steinberg_dither(gray_image)
        else:
            pixels = np.array(gray_image, dtype=np.int32)
        if self.invert_var.get():
            pixels = 255 - pixels
            
        ascii_chars = self.ASCII_SETS[self.ascii_set_var.get()]
        
        for y in range(pixels.shape[0]):
            for x in range(pixels.shape[1]):
                pixel_brightness = pixels[y, x]
                char_index = min(int(pixel_brightness) * len(ascii_chars) // 256, len(ascii_chars) - 1)
                char = ascii_chars[char_index]
                
                r, g, b = color_pixels[y, x]
                hex_color = f'#{r:02x}{g:02x}{b:02x}'
                
                tag_name = f"color_{y}_{x}"
                self.preview_text.tag_configure(tag_name, foreground=hex_color)
                self.preview_text.insert(tk.END, char, tag_name)
            self.preview_text.insert(tk.END, "\n")

    def update_preview_monochrome(self, new_width):
        ascii_art = self.convert_image_to_ascii(
            self.original_image,
            new_width=new_width,
            contrast=self.contrast_slider.get(),
            brightness=self.brightness_slider.get(),
            gamma=self.gamma_slider.get(),
            aspect_ratio=self.aspect_slider.get(),
            invert=self.invert_var.get(),
            ascii_chars=self.ASCII_SETS[self.ascii_set_var.get()]
        )
        if ascii_art:
            self.preview_text.insert(tk.END, ascii_art)

    def floyd_steinberg_dither(self, image):
        pixels = np.array(image, dtype=float)
        h, w = pixels.shape
        for y in range(h - 1):
            for x in range(1, w - 1):
                old_pixel = pixels[y, x]
                new_pixel = round(old_pixel / 255) * 255
                pixels[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                pixels[y, x + 1] += quant_error * 7 / 16
                pixels[y + 1, x - 1] += quant_error * 3 / 16
                pixels[y + 1, x] += quant_error * 5 / 16
                pixels[y + 1, x + 1] += quant_error * 1 / 16
        return np.array(pixels, dtype=np.int32)

    def convert_image_to_ascii(self, image, new_width, contrast, brightness, gamma, aspect_ratio, invert, ascii_chars):
        image = self._resize_image(image.copy(), new_width, aspect_ratio)
        image = image.convert("L")
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Brightness(image).enhance(brightness)
        
        # Manual gamma correction
        pixels = np.array(image).astype(float)
        pixels = 255 * (pixels / 255) ** gamma
        pixels = np.clip(pixels, 0, 255)
        image = Image.fromarray(np.uint8(pixels))

        pixels = np.array(image, dtype=np.int32)
        if invert:
            pixels = 255 - pixels
        
        ascii_str_list = [ascii_chars[min(int(pixel) * len(ascii_chars) // 256, len(ascii_chars)-1)] for pixel in pixels.flatten()]
        ascii_str = "".join(ascii_str_list)
        
        # Ensure the length of ascii_str is a multiple of new_width
        if len(ascii_str) % new_width != 0:
            ascii_str = ascii_str[:-(len(ascii_str) % new_width)]
            
        ascii_img = "\n".join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
        return ascii_img

    def _resize_image(self, image, new_width, aspect_ratio_factor):
        width, height = image.size
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio * aspect_ratio_factor)
        return image.resize((new_width, new_height), resample=Image.LANCZOS)

    def save_to_file(self):
        ascii_art = self.preview_text.get(1.0, tk.END)
        if not ascii_art.strip():
            self.set_status("Nothing to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save ASCII Art As"
        )
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(ascii_art)
                self.set_status(f"ASCII art saved to: {save_path}")
            except Exception as e:
                self.set_status(f"Error saving file: {e}")

    def save_as_html(self):
        if not self.color_var.get():
            self.set_status("HTML export is only available for colored ASCII art.")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
            title="Save ASCII Art as HTML"
        )
        if not save_path:
            return

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ASCII Art</title>
            <style>
                body { background-color: #2B2B2B; }
                pre { font-family: 'Courier New', Courier, monospace; font-size: 10px; line-height: 0.8; }
            </style>
        </head>
        <body>
            <pre>
        """
        
        for y in range(int(self.preview_text.index('end-1c').split('.')[0])):
            for x in range(len(self.preview_text.get(f"{y+1}.0", f"{y+1}.end"))):
                char = self.preview_text.get(f"{y+1}.{x}")
                tags = self.preview_text.tag_names(f"{y+1}.{x}")
                if tags:
                    color = self.preview_text.tag_cget(tags[0], "foreground")
                    html_content += f'<span style="color:{color}">{char}</span>'
                else:
                    html_content += char
            html_content += "\n"

        html_content += """
            </pre>
        </body>
        </html>
        """
        
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self.set_status(f"HTML saved to: {save_path}")
        except Exception as e:
            self.set_status(f"Error saving HTML file: {e}")

    def copy_to_clipboard(self):
        ascii_art = self.preview_text.get(1.0, tk.END)
        if ascii_art.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(ascii_art)
            self.set_status("ASCII art copied to clipboard.")
        else:
            self.set_status("Nothing to copy.")

    def set_status(self, message):
        self.status_var.set(message)

if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiArtGenerator(root)
    root.mainloop()

class CharSetManager:
    def __init__(self, parent, current_sets):
        self.top = tk.Toplevel(parent)
        self.top.title("Manage Character Sets")
        self.new_sets = current_sets.copy()

        self.listbox = tk.Listbox(self.top)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.populate_list()

        btn_frame = Frame(self.top)
        btn_frame.pack(pady=5)

        Button(btn_frame, text="Add", command=self.add_set).pack(side=tk.LEFT, padx=5)
        Button(btn_frame, text="Edit", command=self.edit_set).pack(side=tk.LEFT, padx=5)
        Button(btn_frame, text="Delete", command=self.delete_set).pack(side=tk.LEFT, padx=5)
        Button(self.top, text="Done", command=self.top.destroy).pack(pady=10)

    def populate_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.new_sets.keys():
            self.listbox.insert(tk.END, name)

    def add_set(self):
        self.show_dialog("Add New Set")

    def edit_set(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        name = self.listbox.get(selected[0])
        self.show_dialog("Edit Set", name, self.new_sets[name])

    def delete_set(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        name = self.listbox.get(selected[0])
        if name in ["Standard", "Simple", "Blocks", "Detailed", "Lines"]:
            return # Don't delete default sets
        del self.new_sets[name]
        self.populate_list()

    def show_dialog(self, title, name="", chars=""):
        dialog = tk.Toplevel(self.top)
        dialog.title(title)

        Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, name)

        Label(dialog, text="Characters:").grid(row=1, column=0, padx=5, pady=5)
        chars_entry = tk.Entry(dialog)
        chars_entry.grid(row=1, column=1, padx=5, pady=5)
        chars_entry.insert(0, chars)

        def save():
            new_name = name_entry.get()
            new_chars = chars_entry.get()
            if new_name and new_chars:
                self.new_sets[new_name] = new_chars
                self.populate_list()
                dialog.destroy()

        Button(dialog, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)
