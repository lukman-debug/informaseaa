import os
from django.shortcuts import render # type: ignore
import json
# Create your views here.
from django.shortcuts import render # type: ignore
from django.http import JsonResponse # type: ignore
import base64
import numpy as np # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from io import BytesIO
from PIL import Image # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore


# Mapping of classes
dic = {0: 'Fresh_Eyes',  
       1: 'Fresh_Gills',
       2: 'Nonfresh_Eyes', 
       3: 'Nonfresh_Gills', }

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'models', 'ikan.keras')
# Memuat model
model = load_model(model_path)
model.make_predict_function()

def predict_label(img_array):
    # Preprocess image array
    img_array = image.img_to_array(img_array) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Get model prediction
    prediction = model.predict(img_array)
    confidence_score = np.max(prediction)

    # Set threshold, e.g., 0.7 (70%)
    threshold = 0.7
    if confidence_score < threshold:
        return "No Data", confidence_score

    predicted_class = np.argmax(prediction, axis=1)
    return dic[predicted_class[0]], confidence_score

# Index route (serve the main page with the camera)
def index(request):
    return render(request, 'ikansegar.html')

# Predict route (handle image classification requests)
@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            # Load the incoming JSON data
            data = json.loads(request.body)
            image_data = data.get('image')  # Get the image base64 data from the request

            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)

            # Check if the data contains the expected base64 format and split it
            if ',' in image_data:
                image_data = base64.b64decode(image_data.split(",")[1])
            else:
                return JsonResponse({'error': 'Invalid base64 image data'}, status=400)

            # Process the image
            img = Image.open(BytesIO(image_data))
            img = img.resize((224, 224))  # Resize image to match model input

            # Convert to numpy array
            img_array = np.array(img)

            # Get prediction
            prediction, confidence_score = predict_label(img_array)

            return JsonResponse({
                'prediction': prediction,
                'confidence': round(confidence_score * 100, 2)  # Convert to percentage
            })

        except Exception as e:
            print(f"Error during prediction: {e}")
            return JsonResponse({'error': 'Error during prediction'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

