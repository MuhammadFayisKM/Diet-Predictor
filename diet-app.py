import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import joblib as jb

# load model and encoder
model = jb.load("diet_model.pkl")
encoder = jb.load("diet_label_encoder.pkl")


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
            "Physical_Activity_Level": int(vars["Activity Level"].get()),
            "AgeDaily_Caloric_Intake": int(vars["Calories Intake"].get()),
            "Cholesterol_mg/dl": float(vars["Cholesterol"].get()),
            "Blood_Pressure_mmHg": int(vars["Blood Pressure"].get()),
            "Glucose_mg/dl": float(vars["Glucose"].get()),
            "Dietary_Restrictions": int(vars["Dietary Restrictions"].get()),
            "Allergies": int(vars["Allergies"].get()),
            "Preferred_Cuisine": int(vars["Preferred Cuisine"].get()),
            "Weekly_Excercise_Hours": float(vars["Excercise Hours/Week"].get()),
            "Adherence_to_Diet_Plan": int(vars["Adherence to Plan"].get()),
            "Dietary_Nutrient_Imbalance_Score": int(
                vars["Nutrient Imbalance Score"].get()
            ),
        }

        colleced_dataset = pd.DataFrame([input_data])
        pred = model.predict(colleced_dataset)
        result = encoder.inverse_transform(pred)[0]
        messagebox.showinfo("Prediction", f"Recommended Diet: {result}")
    except Exception as error:
        messagebox.showerror("Error", str(error))


# diet_App
diet_app = tk.Tk()
diet_app.title("Diet Recommendation App")
frame = ttk.Frame(diet_app, padding="20")
frame.pack()

# define from the labels
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

vars = {field: tk.StringVar()  for field in fields}

#createing input fields

for row_num , field in enumerate(fields):
    ttk.Label(frame, text=field).grid(row=row_num, column = 0, sticky=tk.W, pady=2)
    ttk.Entry(frame, textvariable=vars[field]).grid(row=row_num, column = 1, pady=2)
    
ttk.Button(frame, text="Get Diet Plan", command=predict_diet).grid(row=len(fields),  columnspan=2, pady=10)
    
diet_app.mainloop()