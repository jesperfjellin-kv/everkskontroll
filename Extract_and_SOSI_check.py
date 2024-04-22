import os
import subprocess

# Directory to scan and 7-Zip executable path
local_dir = "C:\\FKKOslo\\Kartkontroll\\Ledning_fra_everk\\Nextcloud"
seven_zip_exe = "C:\\Program Files\\7-Zip\\7z.exe"
synced_files_path = "C:\\FKKOslo\\PyScripts\\Download_from_Nextcloud\\synced_files.txt"

def extract_zip(zip_path):
    """Extracts the given zip file using 7-Zip, skipping existing files."""
    extraction_dir = os.path.dirname(zip_path)
    subprocess.run([seven_zip_exe, 'x', '-aos', f'-o{extraction_dir}', zip_path], check=True)

def find_and_extract_zips(directory):
    """Finds and extracts all zip files in the given directory."""
    zip_found = False
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_path = os.path.join(root, file)
                extract_zip(zip_path)
                zip_found = True
    if not zip_found:
        print("No zip files found in the directory.")

def main():
    find_and_extract_zips(local_dir)
    
    # Identify new .SOS files
    new_files = set()
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.lower().endswith('.sos'):
                file_path = os.path.join(root, file)
                new_files.add(file_path)
    
    # Read existing synced files
    existing_synced_files = set()
    if os.path.exists(synced_files_path):
        with open(synced_files_path, 'r') as file:
            existing_synced_files = set(file.read().splitlines())
    
    # Determine genuine new .SOS files
    genuine_new_files = new_files - existing_synced_files
    
    # Update New_SOSI_files.txt with genuine new files
    if genuine_new_files:
        with open("C:\\FKKOslo\\PyScripts\\Download_from_Nextcloud\\New_SOSI_files.txt", 'w') as file:
            for path in genuine_new_files:
                file.write(f"{path}\n")
        print(f"Updated New_SOSI_files.txt with {len(genuine_new_files)} new files.")
    else:
        print("No new .SOS files were found.")
    
    # Update synced_files.txt with all current .SOS files
    with open(synced_files_path, 'w') as file:
        for path in new_files:
            file.write(f"{path}\n")
    print("Updated synced_files.txt with the current state of .SOS files.")

if __name__ == "__main__":
    main()
