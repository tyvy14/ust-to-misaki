# UST to Misaki Converter

This is a Python-based tool that converts UTAU `.ust` files into Sugar Cape `.misaki` format files. The software provides a simple graphical interface using Tkinter to select a UST file, convert it, and export the results.

## Features
- Converts UTAU `.ust` files to `.misaki` format compatible with Sugar Cape.
- Automatically adjusts the note range from UTAU (C1 to C7) to Sugar Cape (C1 to B5).
- Automatically ensures the `length` in the header is always at least `10`.
- Removes the field `小節の数`, as it is not required in the `.misaki` file format.
- Simple GUI to load UST files and save Misaki files.

## Requirements
- Python 3.x
- Tkinter (comes pre-installed with Python)
- xml.etree.ElementTree for XML generation

## How to Install
1. Clone this repository or download the ZIP file.
   ```bash
   git clone https://github.com/yourusername/ust-to-misaki.git
