from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Race
from .services import fetch_last_race_results

class RaceListView(ListView):
    model = Race
    template_name = 'races/race_list.html'

class RaceCreateView(CreateView):
    model = Race
    fields = ['date', 'name', 'driver', 'position']
    template_name = 'races/race_form.html'
    success_url = reverse_lazy('race-list')

class RaceUpdateView(UpdateView):
    model = Race
    fields = ['date', 'name', 'driver', 'position']
    template_name = 'races/race_form.html'
    success_url = reverse_lazy('race-list')

class RaceDeleteView(DeleteView):
    model = Race
    template_name = 'races/race_confirm_delete.html'
    success_url = reverse_lazy('race-list')

class LastRaceResultsView(View):
    template_name = 'races/last_race_results.html'

    def get(self, request):
        data = fetch_last_race_results()
        return render(request, self.template_name, {
            'race': data['race'],
            'results': data['results'],
        })
