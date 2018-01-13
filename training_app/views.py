from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from training_app.module_apprentissage import generate_model
from django.views.generic import TemplateView,View


# Create your views here.
class ModelGenerationView(TemplateView):
    template_name = 'training_app/model_generation.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['result']=generate_model.generateModel()
        return context

class TestPage(TemplateView):
    template_name = 'training_app/test.html'

class ThanksPage(TemplateView):
    template_name = 'training_app/thanks.html'

class HomePage(TemplateView):
    template_name = "training_app/index.html"








