import re

# Path to the text file containing the list of .SOS files to process
list_file_path = r'C:\FKKOslo\PyScripts\Download_from_Nextcloud\New_SOSI_files.txt'

# Define the patterns to be replaced and their replacement
patterns = [r'luftledning.*', r'hengekabel']
replacement = 'Trase'

# Compile the patterns into a regular expression object with case-insensitive matching
pattern_re = re.compile('|'.join(patterns), re.IGNORECASE)
unwanted_pattern_re = re.compile(r'\.(PUNKT|FLATE)\s+\d+:')

# Function to modify file contents
def modify_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='windows-1252') as file:
            file_contents = file.read()

    if unwanted_pattern_re.search(file_contents):
        print(f"Unwanted objects found in file: {file_path}. Exiting workflow.")
        #sys.exit(1)
    
    modified_contents = pattern_re.sub(replacement, file_contents)
    
    with open(file_path, 'w', encoding='windows-1252') as file:
        file.write(modified_contents)

    print(f"Processed file: {file_path}")

# Read the list of file paths from New_SOSI_files.txt and process each file
with open(list_file_path, 'r') as list_file:
    for file_path in list_file:
        file_path = file_path.strip()  
        if file_path:  
            modify_file_contents(file_path)
