import os
import yaml
import pandas as pd

base_path = r"D:\Sathish\Guvi_HCL\Project_2\data"
output_csv = r"D:\Sathish\Guvi_HCL\Project_2\final_output.csv"

all_rows = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith((".yaml", ".yml")):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            # Convert to DataFrame
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame({"value": [data]})

            all_rows.append(df)

# Combine everything
final_df = pd.concat(all_rows, ignore_index=True)

print(final_df)

# Save to CSV
final_df.to_csv(output_csv, index=False, encoding="utf-8")

print("CSV file created successfully at:")
print(output_csv)
