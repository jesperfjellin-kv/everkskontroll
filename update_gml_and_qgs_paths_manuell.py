# -*- coding: UTF-8 -*-

import os
import re
import sys
import tkinter as tk
from tkinter import filedialog

def update_specific_gml_files(directory, gml_files):
    # Pattern to find the <gml:Envelope tag and insert srsDimension
    pattern = re.compile(r'(<gml:Envelope)')
    
    # Walk through the specified GML files and update them
    for gml_file, srs_dimension in gml_files.items():
        file_path = os.path.join(directory, gml_file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Insert srsDimension if not already present
            if f'srsDimension="{srs_dimension}"' not in content:
                new_content = pattern.sub(rf'\1 srsDimension="{srs_dimension}"', content, count=1)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                    
            print(f"Updated {gml_file} with srsDimension={srs_dimension}.")
        else:
            print(f"{gml_file} not found in {directory}.")

def main():
    # Setup the root Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main Tk window

    # Open a dialog to select the directory
    directory = filedialog.askdirectory(
        title="Select the Directory Containing GML Files"
    )
    
    if not directory:
        print("No directory selected, exiting.")
        sys.exit(1)

    # Dictionary of specific GML files and their required srsDimension values
    gml_files = {
        '0_Manglende_FKB_traser_hos_Everket_gml.gml': '3',
        '1_FKB-traseer_som_mangler_eierinfo_gml.gml': '3',
        '2_Manglende_Everks_traser_i_FKB_gml.gml': '2'
    }

    # Update the specified GML files in the selected directory
    update_specific_gml_files(directory, gml_files)
    print("Process completed. Specified GML files have been updated if found.")

if __name__ == "__main__":
    main()
