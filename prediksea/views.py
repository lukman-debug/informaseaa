from django.shortcuts import render
import pandas as pd  # type: ignore
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
import joblib  # type: ignore
from datetime import datetime
from django.http import JsonResponse
# Muat model dan scaler
model_path = "C:/dev/informasea/informasea/static/model_swh2.keras"
scaler_features_path = "C:/dev/informasea/informasea/static/scaler_features.pkl"
scaler_target_path = "C:/dev/informasea/informasea/static/scaler_target.pkl"

model_wave = load_model(model_path)
scaler_features = joblib.load(scaler_features_path)
scaler_target = joblib.load(scaler_target_path)


def index(request):
    return render(request, 'predict.html')

def predict_wave_height(request):
    prediction = None  # Default value if there's no prediction
    if request.method == 'POST':
        # Get data from the form
        longitude = float(request.POST['longitude'])
        latitude = float(request.POST['latitude'])
        time = request.POST['time']
        print(f"Longitude: {longitude}, Latitude: {latitude}, Time: {time}")  # Debugging
        # Convert time
        time = pd.to_datetime(time)
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        
        # Dataframe for prediction
        new_data = pd.DataFrame({
            'longitude': [longitude],
            'latitude': [latitude],
            'swh': [0],  # Dummy SWH value for input
            'year': [year],
            'month': [month],
            'day': [day],
        })
        
        # Scale features
        scaled_new_data = scaler_features.transform(new_data)
        X_new = scaled_new_data.reshape(1, 1, scaled_new_data.shape[1])  # Reshape for LSTM

        # Prediction
        wave_prediction = model_wave.predict(X_new)
        predicted_wave = scaler_target.inverse_transform(wave_prediction)

        # Convert the prediction to a native Python float (avoid float32)
        prediction = float(predicted_wave[0][0])
        print(f"Prediction: {prediction}") 
        
        # Return prediction as JSON response
        return JsonResponse({'prediction': prediction})
    return JsonResponse({'prediction': None})
