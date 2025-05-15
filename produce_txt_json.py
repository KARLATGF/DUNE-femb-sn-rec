import json
import re
import os


def sanitize_filename(filename):
     # Replace slashes with underscores first to avoid directory paths
    filename = filename.replace('/', '_')
    invalid_chars = '<>:"/\\|?*'
    return "".join([c if c.isalnum() or c in ['_', '.'] else '_' for c in filename if c not in invalid_chars])



def extract_chip_sn(lines, chip_index, offset, pattern):

    chip_key = f"* Chip {chip_index} "

    for i, line in enumerate(lines):

        if line.startswith(chip_key):
            target_line = lines[i + offset].strip()
            if re.match(pattern, target_line):
                return target_line

    return "Not found"

def extract_chip_sn_combined(lines, chip_index, offset_4th, offset_5th):
    #EXtracts and combines values from two lines to form a serial number in the format: stripped_4th-stripped_5th.

    chip_key = f"* Chip {chip_index} "

    for i, line in enumerate(lines):
        if line.startswith(chip_key):
            # Extract 4th line value
            line_4th = lines[i + offset_4th].strip()

            # Extract 5th line value
            line_5th = lines[i + offset_5th].strip()

            # Combine parts
            return f"{line_5th}-{line_4th}"

    return "Not found"




def create_json(front_file, back_file, name, output_dir):

    with open(front_file, 'r', encoding='utf-8') as f:
        front_lines = f.readlines()
    with open(back_file, 'r', encoding='utf-8') as f:
        back_lines = f.readlines()

    # Extract required information
    #qr_code = front_lines[0].strip()
    qr_code = front_lines[0].replace("FEMB SN: ", "").strip()
    sanitized_qr_code = sanitize_filename(qr_code)
    date = front_lines[2].strip()

    #serial_number = qr_code

    specifications = {

        "(F) COLDATA 1 SN": extract_chip_sn_combined(front_lines, 0, 5, 6),
        "(F) COLDATA 2 SN": extract_chip_sn_combined(front_lines, 1, 5, 6),
        "(F) ColdADC 1 SN": extract_chip_sn_combined(front_lines, 2, 5, 6),
        "(F) ColdADC 2 SN": extract_chip_sn_combined(front_lines, 3, 5, 6),
        "(F) ColdADC 3 SN": extract_chip_sn_combined(front_lines, 4, 5, 6),
        "(F) ColdADC 4 SN": extract_chip_sn_combined(front_lines, 5, 5, 6),
        "(F) LArASIC 1 SN": extract_chip_sn(front_lines, 6, 8, r'\d{3}-\d{5}'),
        "(F) LArASIC 2 SN": extract_chip_sn(front_lines, 7, 8, r'\d{3}-\d{5}'),
        "(F) LArASIC 3 SN": extract_chip_sn(front_lines, 8, 8, r'\d{3}-\d{5}'),
        "(F) LArASIC 4 SN": extract_chip_sn(front_lines, 9, 8, r'\d{3}-\d{5}'),
        "(B) ColdADC 1 SN": extract_chip_sn_combined(back_lines, 0, 5, 6),
        "(B) ColdADC 2 SN": extract_chip_sn_combined(back_lines, 1, 5, 6),
        "(B) ColdADC 3 SN": extract_chip_sn_combined(back_lines, 2, 5, 6),
        "(B) ColdADC 4 SN": extract_chip_sn_combined(back_lines, 3, 5, 6),
        "(B) LArASIC 1 SN": extract_chip_sn(back_lines, 4, 8, r'\d{3}-\d{5}'),
        "(B) LArASIC 2 SN": extract_chip_sn(back_lines, 5, 8, r'\d{3}-\d{5}'),
        "(B) LArASIC 3 SN": extract_chip_sn(back_lines, 6, 8, r'\d{3}-\d{5}'),
        "(B) LArASIC 4 SN": extract_chip_sn(back_lines, 7, 8, r'\d{3}-\d{5}')
    }

    json_data = {
        "component_type": {
            "part_type_id": "D08100400001"
        },
        "country_code": "US",
        "comments": f"Picture taken on {date}, by {name}",
        "serial_number": f"{qr_code}",
        "institution": {
            "id": 128
        },
        "manufacturer": {
            "id": 58
        },
        "specifications": specifications
    }

    #output_filename = f"{qr_code}.json"
    output_filename = os.path.join(output_dir, f"{sanitized_qr_code}.JSON")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

    print(f"JSON file '{output_filename}' created successfully.")






def write_femb_parts(front_file, back_file, output_dir):

    with open(front_file, 'r', encoding='utf-8') as f:
        front_lines = f.readlines()
    with open(back_file, 'r', encoding='utf-8') as f:
        back_lines = f.readlines()

    # Extract FEMB serial number
    qr_code = front_lines[0].replace("FEMB SN: ", "").strip()

    femb_parts = [
        ["(F) COLDATA 1 SN", extract_chip_sn_combined(front_lines, 0, 5, 6)],
        ["(F) COLDATA 2 SN", extract_chip_sn_combined(front_lines, 1, 5, 6)],
        ["(F) ColdADC 1 SN", extract_chip_sn_combined(front_lines, 2, 5, 6)],
        ["(F) ColdADC 2 SN", extract_chip_sn_combined(front_lines, 3, 5, 6)],
        ["(F) ColdADC 3 SN", extract_chip_sn_combined(front_lines, 4, 5, 6)],
        ["(F) ColdADC 4 SN", extract_chip_sn_combined(front_lines, 5, 5, 6)],
        ["(F) LArASIC 1 SN", extract_chip_sn(front_lines, 6, 8, r'\d{3}-\d{5}')],
        ["(F) LArASIC 2 SN", extract_chip_sn(front_lines, 7, 8, r'\d{3}-\d{5}')],
        ["(F) LArASIC 3 SN", extract_chip_sn(front_lines, 8, 8, r'\d{3}-\d{5}')],
        ["(F) LArASIC 4 SN", extract_chip_sn(front_lines, 9, 8, r'\d{3}-\d{5}')],
        ["(B) ColdADC 1 SN", extract_chip_sn_combined(back_lines, 0, 5, 6)],
        ["(B) ColdADC 2 SN", extract_chip_sn_combined(back_lines, 1, 5, 6)],
        ["(B) ColdADC 3 SN", extract_chip_sn_combined(back_lines, 2, 5, 6)],
        ["(B) ColdADC 4 SN", extract_chip_sn_combined(back_lines, 3, 5, 6)],
        ["(B) LArASIC 1 SN", extract_chip_sn(back_lines, 4, 8, r'\d{3}-\d{5}')],
        ["(B) LArASIC 2 SN", extract_chip_sn(back_lines, 5, 8, r'\d{3}-\d{5}')],
        ["(B) LArASIC 3 SN", extract_chip_sn(back_lines, 6, 8, r'\d{3}-\d{5}')],
        ["(B) LArASIC 4 SN", extract_chip_sn(back_lines, 7, 8, r'\d{3}-\d{5}')]]


    # Write to femb_parts.txt
    output_file = os.path.join(output_dir, "femb_parts.txt")

    with open(output_file, 'w', encoding='utf-8') as f:

        # Write the FEMB serial number
        f.write(f"femb_sn = \"{qr_code}\"\n")

        # Write the FEMB parts array
        f.write("femb_parts = [\n")
        for i, part in enumerate(femb_parts):
            if i < len(femb_parts) - 1:
                f.write(f"[\"{part[0]}\", \"{part[1]}\"],\n")
            else:
                f.write(f"[\"{part[0]}\", \"{part[1]}\"]")  # No comma or newline for the last part
        f.write("]")

    print(f"File '{output_file}' created successfully.")


#################################################################################




def process_all_folders(batch_number, base_results_dir, name):

    batch_dir = None

    for d in os.listdir(base_results_dir):
        if os.path.isdir(os.path.join(base_results_dir,d)) and d.startswith("batch_"):
            if d.split("_")[1] == batch_number:
                batch_dir = d
                break

    if not batch_dir:
        print(f"No batch folder found for number '{batch_number}' under '{base_results_dir}'.")
        return

    batch_path = os.path.join(base_results_dir, batch_dir)

    print(f"Processing batch folder: {batch_path}")

    for folder_name in os.listdir(batch_path):
        folder_path = os.path.join(batch_path, folder_name)

        if os.path.isdir(folder_path):

            front_file = os.path.join(folder_path, "front_results.txt")
            back_file = os.path.join(folder_path, "back_results.txt")

            if os.path.exists(front_file) and os.path.exists(back_file):
                write_femb_parts(front_file, back_file, folder_path)

            else:
                print(f"Skipping folder '{folder_name}' (missing result files)")



# User input
NAME = "Karla F."
BASE_DIR = "results"

batch_number = input("Enter batch number (e.g. 1 or 01 for batch_1): ").strip()

process_all_folders(batch_number, BASE_DIR, NAME)

