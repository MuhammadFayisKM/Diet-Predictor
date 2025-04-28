### simple_diet_model.py
import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class DietRecommenderSimple:
    def __init__(
        self,
        model_path="simple_diet_model.pkl",
        encoder_path="simple_diet_label_encoder.pkl",
        features_path="simple_diet_model_features.pkl",
    ):
        if not (
            os.path.exists(model_path)
            and os.path.exists(encoder_path)
            and os.path.exists(features_path)
        ):
            print("Training simple model on basic features...")
            self.train_model(model_path, encoder_path, features_path)
        else:
            print("Loading existing simple model...")
            self.model = joblib.load(model_path)
            self.encoder = joblib.load(encoder_path)
            self.features = joblib.load(features_path)

    def train_model(self, model_path, encoder_path, features_path):
        # Load full dataset
        df = pd.read_csv("diet_recommendations_dataset.csv")
        # Keep only basic necessary columns
        df = df[
            ["Age", "Weight_kg", "Height_cm", "Gender", "Diet_Recommendation"]
        ].dropna()

        # Encode Gender and target
        le_gender = LabelEncoder()
        df["Gender"] = le_gender.fit_transform(df["Gender"])

        le_target = LabelEncoder()
        df["Diet_Recommendation"] = le_target.fit_transform(df["Diet_Recommendation"])

        # Features and target
        X = df[["Age", "Weight_kg", "Height_cm", "Gender"]]
        y = df["Diet_Recommendation"]

        # Train/Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train a simple logistic regression
        model = LogisticRegression(max_iter=500)
        model.fit(X_train, y_train)

        # Evaluate
        acc = accuracy_score(y_test, model.predict(X_test))
        print(f"Simple model trained. Accuracy: {acc*100:.2f}%")

        # Save artifacts
        joblib.dump(model, model_path)
        joblib.dump(le_target, encoder_path)
        joblib.dump(list(X.columns), features_path)

        # Set instance attributes
        self.model = model
        self.encoder = le_target
        self.features = list(X.columns)

    def predict(self, input_data):
        # input_data is dict with keys matching self.features
        df = pd.DataFrame([input_data])
        df = df[self.features]
        pred = self.model.predict(df)
        return self.encoder.inverse_transform(pred)[0]
