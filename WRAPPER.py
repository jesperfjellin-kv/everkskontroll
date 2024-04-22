import subprocess
import os
import sys

def run_command(command):
    """Runs a command through the subprocess module."""
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Successfully executed: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)} - {e}")
        

def get_new_files(new_files_path):
    """Reads the new files paths from the given file and returns a list of tuples with the directory and file path."""
    new_files_info = []
    try:
        # First attempt to open the file with UTF-8 encoding
        with open(new_files_path, 'r', encoding='utf-8') as new_files_file:
            new_files_info = [(os.path.dirname(line.strip()), line.strip())
                              for line in new_files_file if line.strip()]
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, attempt to open with Windows-1252 encoding
            with open(new_files_path, 'r', encoding='windows-1252') as new_files_file:
                new_files_info = [(os.path.dirname(line.strip()), line.strip())
                                  for line in new_files_file if line.strip()]
        except UnicodeDecodeError:
            print(f"Failed to decode {new_files_path} with both UTF-8 and Windows-1252 encodings.")
            return []
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []

    return new_files_info

def main():
    # Paths
    winscp_batch_file = r"C:\FKKOslo\PyScripts\Download_from_Nextcloud\sync_winscp.bat"
    extract_and_sosi_check_script_path = r"C:\FKKOslo\PyScripts\Download_from_Nextcloud\Extract_and_SOSI_check.py"
    new_files_path = r"C:\FKKOslo\PyScripts\Download_from_Nextcloud\New_SOSI_files.txt"
    omkod_objnavn_script = r"C:\FKKOslo\PyScripts\fymass_fkb_ledning\Omkod_objnavn.py"
    ledning_sjekk_trase_mot_everk_batch = r"C:\FKKOslo\PyScripts\fymass_fkb_ledning\Ledning_sjekk_Trase_mot_Everk.bat"
    update_gml_and_qgs_paths_batch = r"C:\FKKOslo\PyScripts\fymass_fkb_ledning\run_update_gml.bat"

    # Start the WinSCP synchronization
    print("Starting WinSCP synchronization...")
    run_command([winscp_batch_file])

    # Run the Extract_and_SOSI_check.py script to update New_SOSI_files.txt based on the latest sync
    print("Running Extract and SOSI check...")
    run_command(["python", extract_and_sosi_check_script_path])

    # Check if New_SOSI_files.txt has been populated with new files
    if not os.path.exists(new_files_path) or os.path.getsize(new_files_path) == 0:
        print("No new files detected after Extract and SOSI check. Stopping.")
        return

    # Read new files from New_SOSI_files.txt for further processing
    with open(new_files_path, 'r') as file:
        new_files = [line.strip() for line in file if line.strip()]

    for file_path in new_files:
        directory = os.path.dirname(file_path)
        arbeidsmappe_path = os.path.join(directory, 'arbeidsmappe')
        if not os.path.exists(arbeidsmappe_path):
            os.makedirs(arbeidsmappe_path)
        print(f"Processing new file: {file_path}")

        # Remap object names according to product specifications
        print(f"Remapping object names in {file_path}...")
        run_command(["python", omkod_objnavn_script, file_path])

        # Main GIS component of the workflow
        print(f"Running main GIS component for {file_path}...")
        run_command([ledning_sjekk_trase_mot_everk_batch, directory])

        # Run GML update batch file
        print(f"Calling run_update_gml.bat with arbeidsmappe_path: {arbeidsmappe_path}")
        run_command([update_gml_and_qgs_paths_batch, arbeidsmappe_path])

        print(f"All operations for {file_path} completed successfully.")

    # Optionally, clear New_SOSI_files.txt after processing
    open(new_files_path, 'w').close()
    print("Cleared New_SOSI_files.txt for the next run.")

if __name__ == "__main__":
    main()