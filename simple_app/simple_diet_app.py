# simple_diet_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from simple_diet_model import DietRecommenderSimple

# Initialize the simple recommender
recommender = DietRecommenderSimple()
fields = recommender.features  # ['Age', 'Weight_kg', 'Height_cm', 'Gender']

# GUI setup
app = tk.Tk()
app.title("Simple Diet Planner")
frame = ttk.Frame(app, padding=20)
frame.pack()

# Dropdown options for gender
dropdown_options = {"Gender": ["Male", "Female"]}

# Store tk variables
vars = {}

# Build form for basic fields
for i, field in enumerate(fields):
    # Pretty labels
    label = field
    if field == "Weight_kg": label = "Weight (kg)"
    if field == "Height_cm": label = "Height (cm)"
    ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
    vars[field] = tk.StringVar()

    # Dropdown for Gender, Entry for others
    if field == "Gender":
        opts = dropdown_options["Gender"]
        ttk.OptionMenu(frame, vars[field], opts[0], *opts).grid(row=i, column=1)
    else:
        ttk.Entry(frame, textvariable=vars[field]).grid(row=i, column=1)

# Predict button callback
def predict_simple_diet():
    try:
        data = {}
        for field in fields:
            val = vars[field].get()
            if field == "Gender":
                # map Male/Female to 0/1
                data[field] = dropdown_options["Gender"].index(val)
            else:
                data[field] = float(val) if '.' in val else int(val)

        result = recommender.predict(data)
        messagebox.showinfo("Recommended Diet", f"You should follow: {result}")
    except Exception as e:
        messagebox.showerror("Error", f"Please enter valid values.\nDetails: {e}")

# Clear fields function
def clear_fields():
    for var in vars.values():
        var.set("")

# Buttons
ttk.Button(frame, text="Get Recommendation", command=predict_simple_diet).grid(row=len(fields), column=0, pady=10)
ttk.Button(frame, text="Clear", command=clear_fields).grid(row=len(fields), column=1, pady=10)

app.mainloop()
