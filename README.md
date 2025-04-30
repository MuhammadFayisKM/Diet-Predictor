# Diet-Predictor App

**Diet-Predictor App** is a Python-based application that uses machine learning to predict personalized diet plans for users. The app features an interactive GUI built with Tkinter, making it user-friendly and accessible for a wide audience.

---

## Features
- **Machine Learning-Based Diet Recommendations**: Uses Logistic Regression to predict diet plans based on inputs like health conditions, activity level, and dietary preferences.
- **Interactive User Interface**: Built with Tkinter, the app dynamically generates forms for user input.
- **Data Persistence**: Saves user inputs and predictions into a CSV file for record-keeping.
- **Customizable Dropdown Options**: Predefined options for fields like "Gender," "Disease Type," and "Preferred Cuisine."

---

## Technologies Used
- **Programming Language**: Python
- **Frameworks and Libraries**:
  - `Tkinter`: For the graphical user interface.
  - `pandas`: For data processing.
  - `scikit-learn`: For machine learning.
  - `joblib`: For saving and loading trained models.
  - `csv`: For logging user inputs and predictions.

---

## Installation
Follow these steps to set up the app:

1. Clone the repository:
   ```bash
   git clone https://github.com/MuhammadFayisKM/Diet-planner-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Diet-planner-app
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python diet_app.py
   ```

---

## Usage
1. Launch the application using the steps above.
2. Fill in the required fields in the form:
   - Gender
   - Disease Type
   - Severity
   - Physical Activity Level
   - Dietary Restrictions
   - Allergies
   - Preferred Cuisine
3. Click the **"Get Diet"** button to receive a personalized diet recommendation.
4. To reset the form, click the **"Clear Fields"** button.

---

## How It Works
1. **Training the Model**: If the necessary model files are not found, the app trains a Logistic Regression model on the dataset and saves the files (`diet_model.pkl`, etc.).
2. **Making Predictions**: The app uses the trained model to predict diet plans based on user inputs.
3. **Saving Results**: User inputs and predictions are logged in a CSV file (`diet_app_history.csv`).

---

## Contribution
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch with your feature/fix.
3. Commit your changes and push the branch.
4. Open a pull request.

---

## Author
- **[Muhammad Fayis KM](https://github.com/MuhammadFayisKM)**

For any further inquiries, feel free to reach out!
