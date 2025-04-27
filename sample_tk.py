import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import joblib as jb

# Load model and encoder
model = jb.load("diet_model.pkl")
encoder = jb.load("diet_label_encoder.pkl")

# Dropdown options
dropdown_options = {
    "Gender": ["Female", "Male"],
    "Activity Level": ["Active", "Sedentary"],
    "Preferred Cuisine": ["American", "Chinese", "Indian", "Italian", "Mediterranean", "Mexican"],
    "Disease Type": ["None", "Diabetes", "Hypertension", "Heart Disease"],  # Example
    "Severity": ["Mild", "Moderate", "Severe"],
    "Dietary Restrictions": ["None", "Vegetarian", "Vegan", "Gluten-Free"],
    "Allergies": ["None", "Nuts", "Dairy", "Gluten"],
    "Adherence to Plan": ["Low", "Medium", "High"]
}


def predict_diet():
    try:
        input_data = {
            "Age": int(vars["Age"].get()),
            "Gender": 1 if vars["Gender"].get().lower() == "male" else 0,
            "Weight_kg": float(vars["Weight (kg)"].get()),
            "Height_cm": float(vars["Height (cm)"].get()),
            "BMI": float(vars["BMI"].get()),
            "Disease_Type": int(vars["Disease Type"].get()),
            "Severity": int(vars["Severity"].get()),
            "Physical_Activity_Level": 1 if vars["Activity Level"].get().lower() == "active" else 0,
            "AgeDaily_Caloric_Intake": int(vars["Calories Intake"].get()),
            "Cholesterol_mg/dl": float(vars["Cholesterol"].get()),
            "Blood_Pressure_mmHg": int(vars["Blood Pressure"].get()),
            "Glucose_mg/dl": float(vars["Glucose"].get()),
            "Dietary_Restrictions": int(vars["Dietary Restrictions"].get()),
            "Allergies": int(vars["Allergies"].get()),
            "Preferred_Cuisine": dropdown_options["Preferred Cuisine"].index(vars["Preferred Cuisine"].get()),
            "Weekly_Excercise_Hours": float(vars["Excercise Hours/Week"].get()),
            "Adherence_to_Diet_Plan": int(vars["Adherence to Plan"].get()),
            "Dietary_Nutrient_Imbalance_Score": int(
                vars["Nutrient Imbalance Score"].get()
            ),
        }

        collected_dataset = pd.DataFrame([input_data])
        pred = model.predict(collected_dataset)
        result = encoder.inverse_transform(pred)[0]
        messagebox.showinfo("Prediction", f"Recommended Diet: {result}")
    except Exception as error:
        messagebox.showerror("Error", str(error))


# GUI Setup
diet_app = tk.Tk()
diet_app.title("Diet Recommendation App")
frame = ttk.Frame(diet_app, padding="20")
frame.pack()

fields = [
    "Age",
    "Gender",
    "Weight (kg)",
    "Height (cm)",
    "BMI",
    "Disease Type",
    "Severity",
    "Activity Level",
    "Calories Intake",
    "Cholesterol",
    "Blood Pressure",
    "Glucose",
    "Dietary Restrictions",
    "Allergies",
    "Preferred Cuisine",
    "Excercise Hours/Week",
    "Adherence to Plan",
    "Nutrient Imbalance Score",
]

vars = {field: tk.StringVar() for field in fields}

# Input widgets
for row_num, field in enumerate(fields):
    ttk.Label(frame, text=field).grid(row=row_num, column=0, sticky=tk.W, pady=2)
    if field in dropdown_options:
        ttk.OptionMenu(frame, vars[field], dropdown_options[field][0], *dropdown_options[field]).grid(
            row=row_num, column=1, pady=2
        )
    else:
        ttk.Entry(frame, textvariable=vars[field]).grid(row=row_num, column=1, pady=2)

# Submit button
ttk.Button(frame, text="Get Diet Plan", command=predict_diet).grid(row=len(fields), columnspan=2, pady=10)

# Start App
diet_app.mainloop()


"Gender": OPTIONS["Gender"].index(vars_["Gender"].get()),

1 if vars["Gender"].get().lower() == "male" else 0



            "Gender":                      OPTIONS["Gender"].index(vars_["Gender"].get()),
            "Disease_Type":                OPTIONS["Disease Type"].index(vars_["Disease Type"].get()),
            "Severity":                    OPTIONS["Severity"].index(vars_["Severity"].get()),
            "Physical_Activity_Level":     OPTIONS["Activity Level"].index(vars_["Activity Level"].get()),+

            "Dietary_Restrictions":        OPTIONS["Dietary Restrictions"].index(vars_["Dietary Restrictions"].get()),
            "Allergies":                   OPTIONS["Allergies"].index(vars_["Allergies"].get()),
            "Preferred_Cuisine":           OPTIONS["Preferred Cuisine"].index(vars_["Preferred Cuisine"].get()),
