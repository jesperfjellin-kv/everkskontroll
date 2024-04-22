
'''Dette scriptet trengs bare å kjøres én gang for å generere en liste over alle .SOS filer i en mappe og dens undermapper. Lista som blir
generert blir brukt av Extract_and_SOSI_check.py for å sammenligne med en ny liste for å finne nye .SOS filer som har blitt lagt til i mappen.'''

import os

# Specify the directory to search and the output file
search_directory = "C:\\FKKOslo\\Kartkontroll\\Ledning_fra_everk\\Nextcloud"
output_file_path = "last_check_sos_files.txt"

def find_files(directory):
    """Finds all .SOS files in the given directory and its subdirectories."""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.sos'):
                file_paths.append(os.path.join(root, file))
    return file_paths

def update_file_list(file_paths, file_path):
    """Updates the given file with the list of file paths."""
    with open(file_path, 'w') as f:
        for path in file_paths:
            f.write(f"{path}\n")

def main():
    # Find all files in the specified directory
    file_paths = find_files(search_directory)
    
    # Update the output file with the found file paths
    update_file_list(file_paths, output_file_path)

    print(f"Updated {output_file_path} with the current list of files.")

if __name__ == "__main__":
    main()
