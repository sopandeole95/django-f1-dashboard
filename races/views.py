from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Race

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
