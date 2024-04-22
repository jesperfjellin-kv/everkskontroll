import re

# Define the path to the .SOS file
file_path = r'C:\FKKOslo\Kartkontroll\Ledning_fra_everk\Nextcloud\Føie\Traseer.sos'

# Define the patterns to be replaced and their replacement
patterns = [r'luftledninghsp\S*', r'hengekabel']
replacement = 'Trase'

# Compile the patterns into a regular expression object with case-insensitive matching
pattern_re = re.compile('|'.join(patterns), re.IGNORECASE)

try:
    # Attempt to open the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='windows-1252') as file:
        file_contents = file.read()

# Use the regular expression to replace all occurrences of the patterns
modified_contents = pattern_re.sub(replacement, file_contents)

# Write the modified contents back to the file, using the same encoding
with open(file_path, 'w', encoding='windows-1252') as file:
    file.write(modified_contents)

print(".SOS file has been processed.")
