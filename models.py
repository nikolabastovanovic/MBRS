import os
from django.db import models

class Grad(models.Model):
	naziv=models.TextField(max_length=5, null=True),
	oblast=models.TextField(max_length=5),
	postanski_broj=models.CharField(max_length=5, null=True, default=1)

	'''
	You can chose one of these atributes to be returned instead of type object!
	def __str__(self):
		return self.naziv
		return self.oblast
		return self.postanski_broj
	'''

class Osoba(models.Model):
	grad=models.ForeignKey(Grad, on_delete=models.CASCADE)
	ime=models.CharField(max_length=5, null=True, default=1)
	prezime=models.TextField(max_length=6, null=True),
	jmbg=models.TextField(default=1, max_length=6),
	bracno_stanje=models.TextField(max_length=6),
	zaposlenje=models.CharField(max_length=6, default=0)

	'''
	You can chose one of these atributes to be returned instead of type object!
	def __str__(self):
		return self.grad
		return self.ime
		return self.prezime
		return self.jmbg
		return self.bracno_stanje
		return self.zaposlenje
	'''