import pandas as pd
from sklearn.linear_model import LinearRegression

# Load Excel data
data = pd.read_excel("test_results.xlsx")

# Convert Grade to numeric (M25 -> 25)
data["Grade"] = data["Grade"].str.replace("M", "").astype(int)

# Input features
X = data[["Grade", "GGBS", "Metakaolin"]]

# Output
y = data["Strength"]

# Train model
model = LinearRegression()
model.fit(X, y)

print("Model trained using your experimental data.\n")

# Ask user input
grade_input = int(input("Enter Grade (example: 20,25,30,40): "))
ggbs_input = float(input("Enter GGBS (10-50)percentage: "))
mk_input = float(input("Enter Metakaolin (5-30)percentage: "))

# Prediction
prediction = model.predict([[grade_input, ggbs_input, mk_input]])

print("\n===== PREDICTED COMPRESSIVE STRENGTH =====")
print(f"Grade M{grade_input}")
print(f"GGBS: {ggbs_input}%")
print(f"Metakaolin: {mk_input}%")
print(f"Predicted Compressive Strength = {prediction[0]:.2f} MPa")