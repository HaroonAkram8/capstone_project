import pandas as pd
import json

def excel_to_json(excel_file, json_file, system_prompt_path):
    # Read the Excel file (assuming it is in the same directory)
    df = pd.read_excel(excel_file)
    
    # Rename the columns to match the JSON keys
    df = df.rename(columns={
        "Test Input": "instruction",
        "Object Position": "input",
        "Output": "output"
    })
    
    # Replace NaN in 'input' column with an empty string
    df["input"] = df["input"].fillna("")
    
    # Read the system prompt content from the file
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # Add a new column 'system' with the system prompt content
    df["system"] = system_prompt
    
    # Convert the DataFrame to a list of dictionaries
    data_list = df.to_dict(orient='records')
    
    # Write the list to a JSON file with pretty printing
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    excel_file = "data.xlsx"
    json_file = "data.json"
    system_prompt_path = "system_prompts/default_system_prompt.txt"
    excel_to_json(excel_file, json_file, system_prompt_path)
    print(f"Converted '{excel_file}' to '{json_file}' successfully!")
