# -*- coding: UTF-8 -*-

import os
import re
import sys
import xml.etree.ElementTree as ET
from osgeo import ogr
import json

def convert_gml_to_geojson(input_gml, output_geojson):
    # Open the source GML file
    src_ds = ogr.Open(input_gml)
    if src_ds is None:
        print(f"Unable to open {input_gml}")
        return
    
    # Get the first layer of the GML file
    src_lyr = src_ds.GetLayer()
    
    # Create the output GeoJSON file
    driver = ogr.GetDriverByName('GeoJSON')
    if driver is None:
        print("GeoJSON driver not available.")
        return
    
    # Remove output GeoJSON file if it already exists to avoid conflicts
    if os.path.exists(output_geojson):
        driver.DeleteDataSource(output_geojson)
    
    # Create the destination data source and copy the layer from GML
    dst_ds = driver.CreateDataSource(output_geojson)
    dst_ds.CopyLayer(src_lyr, src_lyr.GetName())
    
    # Cleanup
    del src_ds, dst_ds

    print(f"Successfully converted {input_gml} to {output_geojson}")

if len(sys.argv) > 1:
    arbeidsmappe_path = sys.argv[1]
    directory = os.path.dirname(arbeidsmappe_path)
else:
    print("The path to arbeidsmappe was not provided.")
    sys.exit(1)

# Dictionary of GML files and their respective srsDimension values
""" gml_files = {
    '0_Manglende_FKB_traser_hos_Everket_gml.gml': '3',
    '1_FKB-traseer_som_mangler_eierinfo_gml.gml': '3',
    '2_Manglende_Everks_traser_i_FKB_gml.gml': '2'
}

# Edit the GML files to insert srsDimension
for gml_file, srs_dimension in gml_files.items():
    gml_file_path = os.path.join(arbeidsmappe_path, gml_file)
    with open(gml_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Look for the first occurrence of <gml:Envelope and insert srsDimension
    pattern = re.compile(r'(<gml:Envelope)')
    
    # If srsDimension is not already present, add it
    if f'srsDimension="{srs_dimension}"' not in content:
        new_content = pattern.sub(rf'\1 srsDimension="{srs_dimension}"', content, count=1)
        
        # Write the modified content back to the GML file
        with open(gml_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content) """

# Update the .qgs project file paths
qgs_file_path = os.path.join(directory, 'Presentasjon_analyse_NIS-FKB_test.qgs')
tree = ET.parse(qgs_file_path)
root = tree.getroot()

for layer in root.iter('datasource'):
    if layer.text and 'arbeidsmappe' in layer.text:
        gml_relative_path = os.path.relpath(layer.text, directory)
        layer.text = os.path.join('./arbeidsmappe', os.path.basename(gml_relative_path))

tree.write(qgs_file_path)
print('Project file paths corrected.')

# Now convert the edited GML files to GeoJSON
for gml_file in gml_files.keys():
    gml_file_path = os.path.join(arbeidsmappe_path, gml_file)
    output_geojson = gml_file_path.replace('.gml', '.geojson')
    convert_gml_to_geojson(gml_file_path, output_geojson)

print('All GML files converted to GeoJSON.')

geojson_files = [os.path.join(arbeidsmappe_path, gml_file.replace('.gml', '.geojson')) for gml_file in gml_files.keys()]

# Function to restructure coordinates for a GeoJSON file
def remove_height_values(coords):
    new_coords = []
    for coord in coords:
        # Assuming each 'coord' is a list [x, y, z], we take only the first two elements (x and y)
        new_coords.append(coord[:2])  # This slices each list to include only x and y
    return new_coords

# Adjusted function to process and clean up the GeoJSON files without height values
def clean_geojson_files_without_height(file_paths):
    for file_path in file_paths:
        # Load the GeoJSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Remove height values for each feature
        for feature in data['features']:
            # Check if the geometry type is 'LineString' or 'MultiLineString'
            if feature['geometry']['type'] == 'LineString':
                # Directly remove height values
                feature['geometry']['coordinates'] = remove_height_values(feature['geometry']['coordinates'])
            elif feature['geometry']['type'] == 'MultiLineString':
                # Remove height values for each LineString in the MultiLineString
                feature['geometry']['coordinates'] = [remove_height_values(line) for line in feature['geometry']['coordinates']]

        # Write the cleaned up data back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print(f"Height values removed and cleaned GeoJSON file written to {file_path}")

# Use the adjusted cleanup function
clean_geojson_files_without_height(geojson_files)

print('All GeoJSON files cleaned up.')
