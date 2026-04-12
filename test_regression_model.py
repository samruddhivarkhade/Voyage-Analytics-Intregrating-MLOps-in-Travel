import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

flights = pd.read_csv("data/flights.csv")
users = pd.read_csv("data/users.csv")

flight_data = pd.merge(flights, users, left_on="userCode", right_on="code")

df = flight_data.copy()

df = df.drop([
    'travelCode', 'userCode', 'code',
    'name', 'company', 'date', 'from', 'to'
], axis=1)

encoders = {}

for col in ['flightType', 'agency', 'gender']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred_test = model.predict(X_test)
y_pred_train = model.predict(X_train)

print('Model evaluation on the test data : ')
print("R2 Score:", r2_score(y_test, y_pred_test))
print("MAE:", mean_absolute_error(y_test, y_pred_test))

print('Model evaluation on the train data : ')
print("R2 Score:", r2_score(y_train, y_pred_train))
print("MAE:", mean_absolute_error(y_train, y_pred_train))

joblib.dump(model, "models/flight_price_model.pkl")
joblib.dump(encoders, "models/regression_encoders.pkl")

print("\n✅ Regression model saved successfully!")
print("✅ Encoders saved successfully!")