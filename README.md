***Car Dheko - Car Price Prediction App***

**Overview**

Car Dheko is a machine learning-based web application designed to predict the price of cars based on various features like brand, fuel type, model year, and more. It helps users estimate the market value of a car using a pre-trained RandomForest Regressor model.

**Features**

- Predict the price of a car by inputting key details such as brand, fuel type, ownership history, and more.
- Streamlit-powered web interface for easy user interaction.
- Built using a machine learning model trained on real car market data.

**Tech Stack and Packages Used**
- Python: Programming language.
- NumPy: For numerical operations.
- Pandas: For data manipulation and preprocessing.
- Scikit-learn: To implement and train the machine learning model (RandomForest Regressor).
- Streamlit: For creating the web interface.

**Dataset**

The raw data was gathered from a .xlsx file, which included car details such as brand, fuel type, model year, registration year, and other car features. This data was cleaned and preprocessed using Pandas.

**Model**

The model was trained using the RandomForest Regressor algorithm provided by scikit-learn. After training, the model was serialized into a .pkl file, which is used to make predictions in the web app.
- Mean Absolute Error (MAE): 129,121.62
- Mean Squared Error (MSE): 187,349,940,163.45
- Root Mean Squared Error (RMSE): 432,839.39
- R² Score: 0.8995

**Application Workflow**

- Data Preprocessing: Clean and preprocess the car dataset using Pandas.
- Model Training: Train the machine learning model using the RandomForest Regressor.
- Web Interface: Developed a Streamlit web app to accept user inputs and predict the car price using the trained model.

**How to Run**
- Run the Streamlit app: **streamlit run webapp_CarDheko.py**
- Open the provided local URL in your browser and start predicting car prices!
