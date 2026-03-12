import pandas as pd

# Load Excel File
file_path = "test_results.xlsx"   # <-- Change to your file name
data = pd.read_excel(file_path)

# Take User Inputs
grade_input = input("Enter Grade ( M25, M30): ").strip()
ggbs_input = float(input("Enter GGBS percentage: "))
mk_input = float(input("Enter Metakaolin percentage: "))

# Filter Data
filtered_data = data[
    (data["Grade"].str.upper() == grade_input.upper()) &
    (data["GGBS"] == ggbs_input) &
    (data["Metakaolin"] == mk_input)
]

# Output
if not filtered_data.empty:
    average_strength = filtered_data["Strength"].mean()
    
    print("\n===== RESULT =====")
    print(f"Grade: {grade_input.upper()}")
    print(f"GGBS: {ggbs_input}%")
    print(f"Metakaolin: {mk_input}%")
    print(f"Average Compressive Strength = {average_strength:.2f} MPa")
else:
    print("\nNo data found for this combination.")