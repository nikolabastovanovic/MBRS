from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Osoba
from .models import Grad

#Create view for Osoba model.
class OsobaCreateView(CreateView):
	template_name='.html'
	model=Osoba
	fields=['ime', 'prezime', 'jmbg', 'bracno_stanje', 'zaposlenje']
	success_url=reverse_lazy('')

#Update view for Osoba model.
class OsobaUpdateView(UpdateView):
	template_name='.html'
	model=Osoba
	fields=['ime', 'prezime', 'jmbg', 'bracno_stanje', 'zaposlenje']

#Delete view for Osoba model.
class OsobaDeleteView(DeleteView):
	template_name='.html'
	model=Osoba
	success_url=reverse_lazy('')

#List view for Osoba model.
class OsobaListView(generic.ListView):
	template_name='.html'
	context_object_name='all_Osoba'
	def get_queryset(self):
		return Osoba.object.all

#Create view for Grad model.
class GradCreateView(CreateView):
	template_name='.html'
	model=Grad
	fields=['naziv', 'oblast', 'postanski_broj']
	success_url=reverse_lazy('')

#Update view for Grad model.
class GradUpdateView(UpdateView):
	template_name='.html'
	model=Grad
	fields=['naziv', 'oblast', 'postanski_broj']

#Delete view for Grad model.
class GradDeleteView(DeleteView):
	template_name='.html'
	model=Grad
	success_url=reverse_lazy('')

#List view for Grad model.
class GradListView(generic.ListView):
	template_name='.html'
	context_object_name='all_Grad'
	def get_queryset(self):
		return Grad.object.all