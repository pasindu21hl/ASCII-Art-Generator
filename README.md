# ASCII Art Generator

## Overview
The ASCII Art Generator is a Python application that converts images into ASCII art. It provides a graphical user interface (GUI) built with Tkinter, allowing users to load images, adjust conversion settings, and save the resulting ASCII art as text or HTML files. The application supports both monochrome and colored ASCII output, with customizable character sets and image processing options.

## Features
- **Image to ASCII Conversion**: Convert images (PNG, JPG, JPEG, BMP, GIF) to ASCII art.
- **Customizable Settings**:
  - Adjust width, contrast, brightness, gamma, and height factor.
  - Toggle color output, inversion, and dithering using checkboxes.
  - Choose from predefined or custom ASCII character sets.
- **Preview**: Real-time preview of the image and ASCII output.
- **Export Options**:
  - Save ASCII art as a text file.
  - Save colored ASCII art as an HTML file with styling (color mode recommended for mid-range and high-end PCs).
  - Copy ASCII art to the clipboard.
- **Character Set Management**: Add, edit, or delete custom ASCII character sets.
- **Color Mode Performance Note**: The color mode, which applies individual RGB colors to ASCII characters, is computationally intensive and recommended for mid-range and high-end PCs to ensure smooth performance.

## Requirements
The project dependencies are listed in `requirements.txt`:
```
Pillow
numpy
```

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ascii-art-generator
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python ascii_art_generator.py
   ```

## Usage
1. **Launch the Application**:
   Run `ascii_art_generator.py` to open the GUI.

2. **Select an Image**:
   Click "Select Image" to load an image file (PNG, JPG, JPEG, BMP, or GIF).

3. **Adjust Settings**:
   - Use sliders to modify width, contrast, brightness, gamma, height factor, and font size.
   - Enable/disable color, inversion, or dithering using checkboxes. **Note**: Color mode is recommended for mid-range and high-end PCs due to performance demands.
   - Select an ASCII character set from the dropdown or manage custom sets with the "Manage Sets" button.

4. **Preview**:
   The image and ASCII art previews update automatically as settings change. Color mode may slow down preview updates on low-end systems.

5. **Save or Copy**:
   - Click "Save to File" to save the ASCII art as a `.txt` file.
   - Click "Save as HTML" to export colored ASCII art as an HTML file (only available with color enabled, recommended for mid-range and high-end PCs).
   - Click "Copy to Clipboard" to copy the ASCII art to your clipboard.

6. **Manage Character Sets**:
   - Click "Manage Sets" to add, edit, or delete custom ASCII character sets.
   - Default sets (Standard, Simple, Blocks, Detailed, Lines) cannot be deleted.

## File Structure
- `ascii_art_generator.py`: Main application script containing the GUI and ASCII conversion logic.
- `requirements.txt`: Lists the required Python packages (Pillow and NumPy).

## Notes
- The application uses Tkinter for the GUI, which is included with standard Python installations.
- **Color Mode**: Enabled via the "Enable Color" checkbox, this mode applies RGB colors to each ASCII character, which increases processing time and memory usage. For optimal performance, use on mid-range or high-end PCs (e.g., systems with at least 8GB RAM and a multi-core processor).
- Colored ASCII art is displayed in the GUI using Tkinter's text widget and can be exported as HTML for web viewing.
- The Floyd-Steinberg dithering algorithm is implemented for improved grayscale-to-ASCII conversion when dithering is enabled.
- Ensure your system has a compatible Tkinter installation for the GUI to function properly.

## Acknowledgments
- Built with [Pillow](https://python-pillow.org/) for image processing.
- Uses [NumPy](https://numpy.org/) for efficient array operations.
- Inspired by classic ASCII art generation techniques.
