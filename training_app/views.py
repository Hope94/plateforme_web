import os
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from pfe_plateforme_web import settings
from training_app.module_apprentissage import generate_model
from django.views.generic import TemplateView, View, ListView, DetailView
from django.views.generic.edit import FormView
from training_app.forms import DatasetsForm
from main.models import Apk
from main.forms import SearchApkForm
from main.search_engine import apk_search


# Create your views here.
class ModelGenerationView (TemplateView):
    template_name = 'training_app/model_generation.html'

    def get_context_data(self, **kwargs):
        context = super ().get_context_data (**kwargs)
        context['result'] = generate_model.generateModel ()
        return context


class HomePage (TemplateView):
    template_name = "training_app/dashboard.html"


class DrebinPage (TemplateView):
    template_name = "training_app/drebin.html"


# apprentissage module drebin
class DrebinTrainingView (FormView):
    template_name = 'training_app/drebin.html'
    form_class = DatasetsForm
    success_url = reverse_lazy ('training_app:thanks')
    validation_report = dict ()

    def form_valid(self, form):
        begnin_dataset = form.cleaned_data['list_begin_datasets']
        malware_dataset = form.cleaned_data['list_malware_datasets']
        messages.add_message (self.request, messages.INFO, 'training started')
        validation_report = generate_model.generateModel (begnin_dataset=begnin_dataset,
                                                          malware_dataset=malware_dataset)
        self.validation_report['result'] = validation_report
        return render (self.request, 'training_app/drebin_report.html',
                       context={'validation_report': validation_report})


# téléchargment du fichier csv
class DownloadView (TemplateView):
    template_name = 'training_app/download_csv.html'


class DownloadCSV (View):

    def get(self, request, *args, **kwargs):
        path_to_file = os.path.join (os.path.join (settings.MEDIA_ROOT, 'feature_weights_csv_files'),
                                     'feature_weight_mapping.csv')
        print (path_to_file)
        with open (path_to_file, 'rb') as file:
            response = HttpResponse (file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=feature_weight_mapping.csv'
            return response


class ApkListView (ListView):
    context_object_name = 'apks'
    model = Apk
    form_class = SearchApkForm
    template_name = "training_app/apks.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super (ApkListView, self).get_context_data (**kwargs)
        q=self.request.GET.get('q',None)
        if q is not None:
            context['apks']=apk_search.serach_for_apks(q)
        return context

class ApkDetailView (DetailView):
    context_object_name = 'apk_detail'
    model = Apk
    template_name = 'training_app/apk_detail.html'
