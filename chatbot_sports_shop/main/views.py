from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
import numpy as np
from django.conf import settings
import os


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