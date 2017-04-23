from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Grad',
			fields=[
				('id',models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('naziv',models.TextField(max_length=5, null=True)),
				('oblast',models.TextField(max_length=5)),
				('postanski_broj',models.CharField(max_length=5, null=True, default=1)),
			],
		),
		migrations.CreateModel(
			name='Osoba',
			fields=[
				('id',models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('grad',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Grad')),
				('ime',models.CharField(max_length=5, null=True, default=1)),
				('prezime',models.TextField(max_length=6, null=True)),
				('jmbg',models.TextField(default=1, max_length=6)),
				('bracno_stanje',models.TextField(max_length=6)),
				('zaposlenje',models.CharField(max_length=6, default=0)),
			],
		),
	]