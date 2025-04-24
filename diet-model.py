import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib as jb

dataset = pd.read_csv("diet_recommendations_dataset.csv")

# print(dataset.info())

# refined_dataset = dataset.fillna()
# print(dataset.isnull().sum())

# filling with "unknwon" in thenull area

dataset[["Disease_Type", "Dietary_Restrictions", "Allergies"]] = dataset[
    ["Disease_Type", "Dietary_Restrictions", "Allergies"]
].fillna("Unknown")
# print(dataset.isnull().sum())

# print(dataset.info())

label_encode_cols = [
    "Gender",
    "Severity",
    "Physical_Activity_Level",
    "Diet_Recommendation",  # our target
]

embedding_cols = [
    "Disease_Type",
    "Dietary_Restrictions",
    "Allergies",
    "Preferred_Cuisine",
]


predi_convert = {}  # if we need to convert the prediction to the original value

for cols in label_encode_cols:
    conve = LabelEncoder()
    dataset[cols] = conve.fit_transform(dataset[cols])
    predi_convert[cols] = conve

for cols in embedding_cols:
    dataset[cols] = dataset[cols].astype("category").cat.codes

# spliting the dataset for training and testing
patient_id = dataset["Patient_ID"]
xval = dataset.drop(["Diet_Recommendation", "Patient_ID"], axis=1)
yval = dataset["Diet_Recommendation"]

xval_train, xval_test, yval_train, yval_test = train_test_split(
    xval, yval, test_size=0.2, random_state=42
)

# train
model = LogisticRegression(max_iter=600)
model.fit(xval_train, yval_train)

# predict
yval_predict = model.predict(xval_test)

accuracy = accuracy_score(yval_test, yval_predict)
# print("Model Accuracy: ", accuracy) ## output gives like - # Model Accuracy:  0.97
print("Model Accuracy: {:.2f}%".format(accuracy * 100)) # output gives like - Model Accuracy: 97.00%

jb.dump(model, "diet_model.pkl") #model
jb.dump(predi_convert["Diet_Recommendation"], "diet_label_encoder.pkl") #encoder
