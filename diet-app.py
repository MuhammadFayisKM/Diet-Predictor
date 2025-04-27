import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import joblib as jb

# Load model and encoder
model = jb.load("diet_model.pkl")
encoder = jb.load("diet_label_encoder.pkl")

# Dropdown options
dropdown_options = {
    "Gender": ["Male", "Female"],
    "Disease_Type": ["Obesity", "Diabetes", "Hypertension", "None"],
    "Severity": ["Mild", "Moderate", "Severe"],
    "Physical_Activity_Level": ["Sedentary", "Moderate", "Active"],
    "Dietary_Restrictions": ["None", "Low_Sugar", "Low_Sodium"],
    "Allergies": ["None","Peanuts", "Gluten"],
    "Preferred_Cuisine": ["Mexican", "Chinese", "Italian", "Indian"],
}

# Field mappings
field_mappings = {
    "Age": "Age",
    "Gender": "Gender",
    "Weight (kg)": "Weight_kg",
    "Height (cm)": "Height_cm",
    "BMI": "BMI",
    "Disease Type": "Disease_Type",
    "Severity": "Severity",
    "Activity Level": "Physical_Activity_Level",
    "Calories Intake": "Daily_Caloric_Intake",
    "Cholesterol": "Cholesterol_mg/dl",
    "Blood Pressure": "Blood_Pressure_mmHg",
    "Glucose": "Glucose_mg/dl",
    "Dietary Restrictions": "Dietary_Restrictions",
    "Allergies": "Allergies",
    "Preferred Cuisine": "Preferred_Cuisine",
    "Excercise Hours/Week": "Weekly_Excercise_Hours",
    "Adherence to Plan": "Adherence_to_Diet_Plan",
    "Nutrient Imbalance Score": "Dietary_Nutrient_Imbalance_Score",
}


def predict_diet():
    try:
        input_data = {}
        for field, model_field in field_mappings.items():
            value = vars[field].get()

            if model_field in dropdown_options:
                input_data[model_field] = dropdown_options[model_field].index(value)
            else:
                # Handle numerical fields
                if "Age" in field or "Calories" in field or "Blood Pressure" in field or "Adherence" in field or "Score" in field:
                    input_data[model_field] = int(value)
                else:
                    input_data[model_field] = float(value)

        collected_dataset = pd.DataFrame([input_data])
        pred = model.predict(collected_dataset)
        result = encoder.inverse_transform(pred)[0]
        messagebox.showinfo("Prediction", f"Recommended Diet: {result}")

    except Exception as error:
        messagebox.showerror("Error", f"An error occurred:\n{error}")


# Create Tkinter App
diet_app = tk.Tk()
diet_app.title("Diet Recommendation App")
frame = ttk.Frame(diet_app, padding="20")
frame.pack()

# Define form fields
fields = list(field_mappings.keys())

vars = {field: tk.StringVar() for field in fields}

# Create input fields
for row_num, field in enumerate(fields):
    ttk.Label(frame, text=field).grid(row=row_num, column=0, sticky=tk.W, pady=2)
    if field in dropdown_options or field_mappings[field] in dropdown_options:
        options = dropdown_options.get(field, dropdown_options.get(field_mappings[field]))
        ttk.OptionMenu(frame, vars[field], options[0], *options).grid(row=row_num, column=1, pady=2)
    else:
        ttk.Entry(frame, textvariable=vars[field]).grid(row=row_num, column=1, pady=2)

# Button to predict
ttk.Button(frame, text="Get Diet Plan", command=predict_diet).grid(
    row=len(fields), columnspan=2, pady=10
)

diet_app.mainloop()
