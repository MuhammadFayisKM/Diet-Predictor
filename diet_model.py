import os
import pandas as pd
import joblib as jb
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class DietRecommender:
    def __init__(self):
        if not (
            os.path.exists("diet_model.pkl")
            and os.path.exists("diet_label_encoder.pkl")
            and os.path.exists("diet_model_features.pkl")
        ):
            print("Model Files not found, training new one")
            self.train_model()
        else:
            print("Loading Model Files")
            self.model = jb.load("diet_model.pkl")
            self.encoder = jb.load("diet_label_encoder.pkl")
            self.features = jb.load(
                "diet_model_features.pkl"
            )  # to get the column names automatically to the dropdowns!

    def train_model(self):
        dataset = pd.read_csv("diet_recommendations_dataset.csv")

        dataset[["Disease_Type", "Dietary_Restrictions", "Allergies"]] = dataset[
            ["Disease_Type", "Dietary_Restrictions", "Allergies"]
        ].fillna(
            "Unknown"
        )  # filling miss values

        label_encode_cols = [
            "Gender",
            "Severity",
            "Physical_Activity_Level",
            "Diet_Recommendation",  # target!
        ]

        embedding_cols = [
            "Disease_Type",
            "Dietary_Restrictions",
            "Allergies",
            "Preferred_Cuisine",
        ]

        self.label_encoders = {}

        for col in label_encode_cols:
            encoder = LabelEncoder()
            dataset[col] = encoder.fit_transform(dataset[col])
            self.label_encoders[col] = encoder

        for col in embedding_cols:
            dataset[col] = dataset[col].astype("category").cat.codes

        # splitting the datasets
        xval = dataset.drop(["Diet_Recommendation", "Patient_ID"], axis=1)

        yval = dataset["Diet_Recommendation"]

        xval_train, xval_test, yval_train, yval_test = train_test_split(
            xval, yval, test_size=0.2, random_state=42
        )

        model = LogisticRegression(max_iter=600)
        model.fit(xval_train, yval_train)

        accuracy = accuracy_score(yval_test, model.predict(xval_test))

        print(f"Model Trained with Accuracy: {accuracy * 100:.2f}%")

        jb.dump(model, "diet_model.pkl")
        jb.dump(self.label_encoders["Diet_Recommendation"], "diet_label_encoder.pkl")
        jb.dump(list(xval.columns), "diet_model_features.pkl")  
        # save the fields

        self.model = model
        self.encoder = self.label_encoders["Diet_Recommendation"]
        self.features = list(xval.columns)

    def predict_diet(self, input_data: dict):
        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])
        input_df = input_df[self.features]
        # Ensure the input has the same columns as the model
        prediction = self.model.predict(input_df)
        decoded = self.encoder.inverse_transform(prediction)[0]
        return decoded

    # return the predicted value
    
