from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
from newspaper import Article
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def extract_text(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        link = body.get('link')

        if not link:
            return JsonResponse({'error': 'No link provided'}, status=400)

        # Call to AI agent or fake news checker logic goes here
        # For now, just mock a response
        print(f"Received link: {link}")
        
        # Simulated prediction for demo
        prediction = 1 if "fake" in link else 0

        return JsonResponse({'prediction': prediction})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)







@api_view(['POST'])
def analyze_article(request):
    """
    Takes a news article URL, extracts the text, and uses OpenAI to classify it.
    """
    link = request.data.get("link")
    if not link:
        return Response({"error": "No link provided"}, status=400)

    try:
        # Extract text from link
        article = Article(link)
        article.download()
        article.parse()
        text = article.text

        if not text:
            return Response({"error": "Unable to extract article text."}, status=400)

        # Ask OpenAI to classify
        prompt = (
            "You are a fake news detection agent.\n\n"
            "Classify the following article as 'Real' or 'Fake'. "
            "Just respond with either 'Real' or 'Fake'.\n\n"
            f"{text[:3000]}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response['choices'][0]['message']['content'].strip().lower()

        # Interpret OpenAI's reply
        if 'fake' in reply:
            prediction = 1
        elif 'real' in reply:
            prediction = 0
        else:
            prediction = -1  # uncertain

        return Response({
            "prediction": prediction,
            "reply": reply
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
