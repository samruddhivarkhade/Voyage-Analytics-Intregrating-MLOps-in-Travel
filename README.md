# Voyage-Analytics-Integrating-MLOps-in-Travel

This repository contains the machine learning models for:

Flight Price Prediction (Regression)
Gender Classification (Classification)

Follow the steps below to set up the project locally.

⚙️ Step 1: Clone the Repository

git clone
cd Voyage-Analytics

🧪 Step 2: Create Virtual Environment
Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

📦 Step 3: Install Dependencies

pip install -r requirements.txt

▶️ Step 4: Run the Models
Run Regression Model:

python regression_model.py

Run Gender Classification Model:

python gender_model.py

📁 Project Structure

project/
│
├── data/ → datasets (flights, hotels, users)
├── models/ → saved ML models & encoders
├── regression_model.py
├── gender_model.py
├── requirements.txt

⚠️ Important Instructions
Always activate the virtual environment before running code
Do not modify model input features without informing the team
Ensure datasets are placed correctly inside the data/ folder
Encoders are saved and must be used during prediction
