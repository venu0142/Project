from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import os  # needed for PORT

# -------------------------
# Initialize Flask app
# -------------------------
app = Flask(__name__)

# -------------------------
# Load your Excel data & train model
# -------------------------
data = pd.read_excel("test_results.xlsx")
data["Grade"] = data["Grade"].str.replace("M","").astype(int)
X = data[["Grade","GGBS","Metakaolin"]]
y = data["Strength"]
model = LinearRegression()
model.fit(X, y)

# -------------------------
# Base mix designs
# -------------------------
base_mix = {
    25: {"cement": 413, "FA": 690, "CA": 1127, "water": 186},
    30: {"cement": 450, "FA": 620, "CA": 1159.31, "water": 186}
}

def estimate_materials(grade, ggbs_percent, mk_percent):
    if grade < 25:
        factor = grade/25
        base = base_mix[25]
    elif grade > 30:
        factor = grade/30
        base = base_mix[30]
    elif grade == 25 or grade == 30:
        factor = 1
        base = base_mix[grade]
    else:
        if grade < 30:
            factor = (grade-25)/5
            base = {k: base_mix[25][k]*(1-factor)+base_mix[30][k]*factor for k in base_mix[25]}
        else:
            factor = 1
            base = base_mix[30]

    total_binder = base["cement"]
    cement = total_binder * (1 - (ggbs_percent+mk_percent)/100)
    ggbs = total_binder * (ggbs_percent/100)
    mk = total_binder * (mk_percent/100)

    materials = {
        "cement": round(cement,2),
        "GGBS": round(ggbs,2),
        "Metakaolin": round(mk,2),
        "FA": round(base["FA"]*factor,2),
        "CA": round(base["CA"]*factor,2),
        "water": round(base["water"]*factor,2)
    }
    return materials

# -------------------------
# Flask route
# -------------------------
@app.route("/", methods=["GET","POST"])
def index():
    result = None
    materials = None
    grade = None
    ggbs = None
    mk = None
    if request.method=="POST":
        grade = int(request.form["grade"])
        ggbs = float(request.form["ggbs"])
        mk = float(request.form["mk"])
        pred = model.predict([[grade, ggbs, mk]])[0]
        result = round(pred,2)
        materials = estimate_materials(grade, ggbs, mk)
    return render_template("index.html", result=result, materials=materials,
                           grade=grade, ggbs=ggbs, mk=mk)

# -------------------------
# Run app on Render
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)