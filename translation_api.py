from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import openai

# Configurez votre clé API OpenAI ici
openai.api_key = 'votre_cle_api_openai'

# Modèle pour stocker les traductions
class Translation(models.Model):
    original_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=50, default='fr')
    target_language = models.CharField(max_length=50, default='en')
    created_at = models.DateTimeField(auto_now_add=True)

# Endpoint pour soumettre une phrase à traduire
@csrf_exempt
@api_view(['POST'])
def translate_text(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        original_text = data.get('text')
        
        if not original_text:
            return JsonResponse({'error': 'Texte non fourni'}, status=400)

        try:
            # Utilisation de l'API ChatGPT pour traduire
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a translator from French to English."},
                    {"role": "user", "content": original_text}
                ]
            )

            translated_text = response['choices'][0]['message']['content'].strip()

            # Sauvegarde dans la base de données
            translation = Translation.objects.create(
                original_text=original_text,
                translated_text=translated_text
            )

            return JsonResponse({
                'id': translation.id,
                'original_text': translation.original_text,
                'translated_text': translation.translated_text
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Endpoint pour récupérer toutes les traductions
@api_view(['GET'])
def get_translations(request):
    if request.method == 'GET':
        translations = Translation.objects.filter(
            source_language='fr', target_language='en'
        )
        data = [
            {
                'id': translation.id,
                'original_text': translation.original_text,
                'translated_text': translation.translated_text,
                'created_at': translation.created_at
            }
            for translation in translations
        ]
        return JsonResponse(data, safe=False)

# Configuration des URLs
from django.urls import path

urlpatterns = [
    path('translate/', translate_text, name='translate_text'),
    path('translations/', get_translations, name='get_translations'),
]
