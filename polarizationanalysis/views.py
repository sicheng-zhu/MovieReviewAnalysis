from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from polarizationanalysis import polarizationanalysis
import json


# Home page view
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


# Polarization analysis view
class CustomersPageView(TemplateView):
    @csrf_exempt
    def processInput(request):
        json_data = json.loads(request.body)
        classification = polarizationanalysis.doPolarizationAnalysis(json_data['review'])
        return HttpResponse('{ "classification":"' + classification + '" }')
