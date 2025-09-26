from django.shortcuts import render
import pandas as pd  # type: ignore
import numpy as np
from django.http import JsonResponse
from datetime import datetime
import os
from django.conf import settings

# Try to load model and scaler - handle missing files gracefully
model_wave = None
scaler_features = None
scaler_target = None

try:
    from tensorflow.keras.models import load_model  # type: ignore
    import joblib  # type: ignore
    
    # Use relative paths from project root
    base_path = settings.BASE_DIR
    model_path = os.path.join(base_path, "static", "model_swh2.keras")
    scaler_features_path = os.path.join(base_path, "static", "scaler_features.pkl")
    scaler_target_path = os.path.join(base_path, "static", "scaler_target.pkl")
    
    if os.path.exists(model_path):
        model_wave = load_model(model_path)
    if os.path.exists(scaler_features_path):
        scaler_features = joblib.load(scaler_features_path)
    if os.path.exists(scaler_target_path):
        scaler_target = joblib.load(scaler_target_path)
except Exception as e:
    print(f"Warning: Could not load prediction models: {e}")


def index(request):
    return render(request, 'predict.html')

def predict_wave_height(request):
    prediction = None  # Default value if there's no prediction
    if request.method == 'POST':
        # Check if models are loaded
        if not all([model_wave, scaler_features, scaler_target]):
            return JsonResponse({'prediction': None, 'error': 'Prediction models not available'})
            
        try:
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
        except Exception as e:
            return JsonResponse({'prediction': None, 'error': str(e)})
    return JsonResponse({'prediction': None})
