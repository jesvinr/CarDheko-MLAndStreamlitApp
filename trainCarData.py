import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics as mt
from sklearn.preprocessing import StandardScaler
import math
import pickle

final_df = pd.read_csv("D:\\python\\VsCodePythonWorkplace\\car_dheko_project\\datasets\\AllCarDetailAfterPreprepcessing.csv")
# Assuming final_df is your DataFrame
X = final_df.drop('price', axis=1)  # features
y = final_df['price']  # target

# Identify numeric and categorical columns

categorical_cols = X.select_dtypes(include=['object']).columns
# Standardize numeric columns
numeric_cols = X.select_dtypes(include=['int64', 'float64', 'int32']).columns
scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
X['ownerno']    = 1 / X['ownerno']     #since owner number is inserly proportial to price.
X['km']         = 1 / X['km']

# Ensure categorical columns are strings
X[categorical_cols] = X[categorical_cols].astype(str)

# Initialize LabelEncoder
label_encoders = {}

# Encode categorical columns using LabelEncoder
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le  # Store the encoder for potential inverse transformation later


# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

# Train RandomForest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
print("training completed")
# Predict and evaluate
y_pred = rf.predict(X_test)

mae = mt.mean_absolute_error(y_test, y_pred)
mse = mt.mean_squared_error(y_test, y_pred) 
R2Score = mt.r2_score(y_test, y_pred)
rmse = math.sqrt(mse)
print("mean_absolute_error: ", mae)
print("mean_squared_error: ", mse)
print("Root_mean_squared_error: ", rmse)
print("R2Score: ", R2Score)

userInput = input("Do you want to save the model? [yes / no]")
if userInput in ["yes", "y"]:
    fileName = input("Name of the file: ")
    with open('D:\\python\\VsCodePythonWorkplace\\car_dheko_project\\datasets\\'+fileName+'.pkl', 'wb') as file:
        pickle.dump({'model': rf, 'label_encoders': label_encoders, 'scaler': scaler}, file)
        print("file written successfully...")