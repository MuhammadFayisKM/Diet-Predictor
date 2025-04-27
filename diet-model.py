# diet_model_manager.py
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib as jb

class DietModelManager:
    def __init__(self, model_path="diet_model.pkl", encoder_path="diet_label_encoder.pkl", dataset_path="diet_recommendations_dataset.csv"):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.dataset_path = dataset_path
        self.model = None
        self.encoder = None
        self.predi_convert = {}
        self.ensure_model()

    def ensure_model(self):
        """Load model and encoder if available, else train."""
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.model = jb.load(self.model_path)
            self.encoder = jb.load(self.encoder_path)
        else:
            self.train_model()
            self.model = jb.load(self.model_path)
            self.encoder = jb.load(self.encoder_path)

    def train_model(self):
        """Train and save model and label encoder."""
        dataset = pd.read_csv(self.dataset_path)

        # Fill missing values
        dataset[["Disease_Type", "Dietary_Restrictions", "Allergies"]] = dataset[
            ["Disease_Type", "Dietary_Restrictions", "Allergies"]
        ].fillna("Unknown")

        label_encode_cols = [
            "Gender",
            "Severity",
            "Physical_Activity_Level",
            "Diet_Recommendation",  # Target column
        ]

        embedding_cols = [
            "Disease_Type",
            "Dietary_Restrictions",
            "Allergies",
            "Preferred_Cuisine",
        ]

        # Label Encoding
        predi_convert = {}
        for col in label_encode_cols:
            le = LabelEncoder()
            dataset[col] = le.fit_transform(dataset[col])
            predi_convert[col] = le

        # Category Encoding
        for col in embedding_cols:
            dataset[col] = dataset[col].astype("category").cat.codes

        # Prepare data
        xval = dataset.drop(["Diet_Recommendation", "Patient_ID"], axis=1)
        yval = dataset["Diet_Recommendation"]

        # Split
        x_train, x_test, y_train, y_test = train_test_split(xval, yval, test_size=0.2, random_state=42)

        # Train
        model = LogisticRegression(max_iter=600)
        model.fit(x_train, y_train)

        # Evaluate
        y_pred = model.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model trained successfully! Accuracy: {acc*100:.2f}%")

        # Save model and encoder
        jb.dump(model, self.model_path)
        jb.dump(predi_convert["Diet_Recommendation"], self.encoder_path)

    def predict(self, input_df):
        """Predict and decode the output."""
        if self.model is None or self.encoder is None:
            raise ValueError("Model or encoder not available.")

        prediction = self.model.predict(input_df)
        decoded_prediction = self.encoder.inverse_transform(prediction)[0]
        return decoded_prediction
