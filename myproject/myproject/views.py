from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import json
import os
import joblib

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, 'MLmodel', 'model.pkl')
vectorizer_path = os.path.join(base_dir, 'MLmodel', 'vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def predict_news(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    return prediction[0]

@csrf_exempt
def extract_text(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        link = body.get('link')

        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            # Predict
            prediction =int( predict_news(text))

            return JsonResponse({'text': text, 'prediction': prediction})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
