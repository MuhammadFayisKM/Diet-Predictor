import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from diet_model import DietRecommender

import csv
import os

# load model file
recommender = DietRecommender()

# auto fetch fields
fields = recommender.features

# custom dropdown options

dropdown_options = {
    "Gender": ["Male", "Female"],
    "Disease_Type": ["Diabetes", "Hypertension", "Obesity", "None"],
    "Severity": ["Mild - low", "Moderate - medium", "Severe - high"],
    "Physical_Activity_Level": [
        "Sedentary",
        "Moderate ",
        "Active",
    ],
    "Dietary_Restrictions": [
        "None",
        "Low Sugar",
        "Low Sodium",
    ],
    "Allergies": [
        "None",
        "Gluten",
        "Peanuts",
    ],
    "Preffered_Cuisine": ["Mexican", "Chinese", "Italian", "Indian"],
}

# app
diet_app = tk.Tk()
diet_app.title("Diet Planner")
frame = ttk.Frame(diet_app, padding="10")
frame.pack()

# create forms dynamically
vars = {}

for row_num, field in enumerate(fields):
    pretty_name = field.replace("_", " ").replace("kg", "kg").replace("cm", "cm")
    ttk.Label(frame, text=pretty_name).grid(row=row_num, column=0, sticky=tk.W, pady=2)

    vars[field] = tk.StringVar()

    if field in dropdown_options:
        options = dropdown_options[field]
        ttk.OptionMenu(frame, vars[field], options[0], *options).grid(
            row=row_num, column=1, pady=2
        )
    else:
        ttk.Entry(frame, textvariable=vars[field]).grid(row=row_num, column=1, pady=2)

# predict button


def predict_diet():
    try:
        predict_button.config(state=tk.DISABLED)
        diet_app.update_idletasks()

        input_data = {}
        for field in fields:
            value = vars[field].get()

            if field in dropdown_options:
                input_data[field] = dropdown_options[field].index(value)
            else:
                input_data[field] = float(value) if "." in value else int(value)

        # prediction
        result = recommender.predict_diet(input_data)

        messagebox.showinfo("Diet Recommendation", f"Recommended Diet: {result}")

        # save data to csv
        save_user_input(input_data, result)

    except Exception as error:
        messagebox.showerror("Error", f"Solve: {error}")

    finally:
        predict_button.config(state=tk.NORMAL)


# save data
def save_user_input(input_data, result):
    file_exists = os.path.isfile("diet_app_history.csv")
    with open("diet_app_history.csv", mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(list(input_data.keys()) + ["Prediction"])
        writer.writerow(list(input_data.values()) + [result])


# clear fields


def clear_fields():
    for var in vars.values():
        var.set("")


# predict button
predict_button = ttk.Button(frame, text="Get Diet", command=predict_diet)
predict_button.grid(row=len(fields), columnspan=2, pady=10)

clear_button = ttk.Button(frame, text="Clear Fields", command=clear_fields)
clear_button.grid(row=len(fields), column=1, pady=10)

diet_app.mainloop()
