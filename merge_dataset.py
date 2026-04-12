import pandas as pd

flights = pd.read_csv("data/flights.csv")
hotels = pd.read_csv("data/hotels.csv")
users = pd.read_csv("data/users.csv")

flight_data = pd.merge(flights, users, left_on="userCode", right_on="code")

hotel_data = pd.merge(hotels, users, left_on="userCode", right_on="code")

print("Flight Data Shape:", flight_data.shape)
print("Hotel Data Shape:", hotel_data.shape)