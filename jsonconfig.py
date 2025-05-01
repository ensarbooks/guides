import os
import json

# Folder containing your JSON files
input_folder = "config"
output_file = "config/config.json"
output_file_basename = os.path.basename(output_file)

# Create an empty list to collect all items
merged_list = []

# Loop through all files
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".json") and filename != output_file_basename:
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    merged_list.extend(data)
                elif isinstance(data, dict):
                    merged_list.append(data)

            print(f"Processed {filename}")

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

# Save the final merged list
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_list, f, indent=4)
    print(f"\nConsolidated config saved as {output_file}")
