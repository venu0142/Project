import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

# Load Excel data
data = pd.read_excel("test_results.xlsx")

# Convert Grade (M25 → 25)
data["Grade"] = data["Grade"].str.replace("M","").astype(int)

# Inputs
X = data[["Grade","GGBS","Metakaolin"]]

# Output
y = data["Strength"]

# Train model
model = LinearRegression()
model.fit(X,y)

print("Model trained using experimental data.\n")

# User input
grade = int(input("Enter Grade (20–40): "))
ggbs = float(input("Enter GGBS %: "))
mk = float(input("Enter Metakaolin %: "))

prediction = model.predict([[grade,ggbs,mk]])

print("\nPredicted Compressive Strength =",round(prediction[0],2),"MPa")

# -----------------------------
# 3D SURFACE GRAPH
# -----------------------------

ggbs_range = np.arange(0,50,2)
mk_range = np.arange(0,30,2)

GGBS, MK = np.meshgrid(ggbs_range,mk_range)

strength_surface = model.predict(
    np.column_stack([np.full(GGBS.size,grade),
                     GGBS.ravel(),
                     MK.ravel()])
)

strength_surface = strength_surface.reshape(GGBS.shape)

fig = plt.figure()

ax = fig.add_subplot(111,projection='3d')

ax.plot_surface(GGBS,MK,strength_surface)

ax.set_xlabel("GGBS (%)")
ax.set_ylabel("Metakaolin (%)")
ax.set_zlabel("Compressive Strength (MPa)")

ax.set_title(f"Strength Surface for Grade M{grade}")

plt.show()