from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
import numpy as np
from django.conf import settings
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
from django.http import JsonResponse

load_dotenv()

class Main(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'data', 'data.csv')
        data = pd.read_csv(file_path).to_numpy()

        context = super(Main, self).get_context_data(**kwargs)
        context['items'] = data

        return context
    

class ItemView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'data', 'data.csv')
        
        data = pd.read_csv(file_path)
        
        filtered_data = data[data['model'] == self.kwargs['model']]

        context = super(ItemView, self).get_context_data(**kwargs)
        context['items'] = filtered_data.to_numpy()

        return context
    

class CategoryView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'data', 'data.csv')
        
        data = pd.read_csv(file_path)
        
        filtered_data = data[data['item_category'] == self.kwargs['category']]

        context = super(CategoryView, self).get_context_data(**kwargs)
        context['items'] = filtered_data.to_numpy()

        return context
    
def send_message(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if not query:
            return JsonResponse({'error': 'No query provided'}, status=400)

    try:
        ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
        ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

        # Ensure both environment variables are set
        if not ls_prediction_endpoint or not ls_prediction_key:
            raise ValueError("LS_CONVERSATIONS_ENDPOINT or LS_CONVERSATIONS_KEY not found.")

        # Initialize the client for the Language service model
        client = ConversationAnalysisClient(
            ls_prediction_endpoint, 
            AzureKeyCredential(ls_prediction_key)
        )

        # Call the Language service model to get intent and entities
        cls_project = 'shop-chatbot'
        deployment_slot = 'shop_chatbot'

        # Call the analyze_conversation method
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": cls_project,
                    "deploymentName": deployment_slot,
                    "verbose": True
                }
            }
        )

        # Check if the result has the expected structure
        if "result" in result and "prediction" in result["result"]:
            top_intent = result["result"]["prediction"]["topIntent"]
            entities = result["result"]["prediction"].get("entities", [])

            # You could also log or process these results if needed
            print(f"Top Intent: {top_intent}")
            print(f"Entities: {entities}")

            # Return the full result as a JsonResponse
            return JsonResponse(result)

        else:
            return JsonResponse({"error": "Unexpected response structure."}, status=500)

    except Exception as ex:
        print(f"An error occurred: {ex}")
        return JsonResponse({"error": str(ex)}, status=500)