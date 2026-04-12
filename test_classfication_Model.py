import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

flights = pd.read_csv("data/flights.csv")
hotels = pd.read_csv("data/hotels.csv")
users = pd.read_csv("data/users.csv")

flight_data = pd.merge(flights, users, left_on="userCode", right_on="code")
hotel_data = pd.merge(hotels, users, left_on="userCode", right_on="code")

flight_features = flight_data.groupby("userCode").agg({
    "price": "mean",
    "distance": "mean",
    "time": "mean"
}).reset_index()

hotel_features = hotel_data.groupby("userCode").agg({
    "total": "mean",
    "days": "mean"
}).reset_index()

user_behavior = pd.merge(flight_features, hotel_features, on="userCode", how="outer")

user_behavior = pd.merge(user_behavior, users, left_on="userCode", right_on="code")

user_behavior = user_behavior.fillna(0)

df = user_behavior.copy()

le = LabelEncoder()
df['gender'] = le.fit_transform(df['gender'])

joblib.dump(le, "models/gender_encoder.pkl")

df = df.drop(['userCode', 'code', 'name', 'company'], axis=1)

X = df.drop('gender', axis=1)
y = df['gender']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred_test = model.predict(X_test)
y_pred_train = model.predict(X_train)

y_pred_labels_test = le.inverse_transform(y_pred_test)
y_test_labels_test = le.inverse_transform(y_test)

y_pred_labels_train = le.inverse_transform(y_pred_train)
y_test_labels_train = le.inverse_transform(y_train)

print('Accuracy on the test data : ')
print("Accuracy:", accuracy_score(y_test, y_pred_test))
print("\nClassification Report:\n", classification_report(y_pred_labels_test, y_test_labels_test))

print('Accuracy on the train data : ')
print("Accuracy:", accuracy_score(y_train, y_pred_train))
print("\nClassification Report:\n", classification_report(y_pred_labels_train, y_test_labels_train))

joblib.dump(model, "models/gender_model.pkl")

print("\n✅ Gender model saved successfully!")
print("✅ Encoder saved successfully!")