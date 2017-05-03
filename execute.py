'''
Created on 06.12.2015.

@author: xx
'''

from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
import pydot, os
import hashlib


class Proba(object):
    def __init__(self):
        self.query_set = []

    def interpreter(self, model):

        return self.query_set


def execute(path, grammar_file_name, example_file_name, export_dot, export_png):
    '''U svrhe brzeg testiranja, metoda koja prima putanju do foldera, naziv fajla gde je gramatika i naziv fajla gde je
        primer programa u nasem jeziku i indikator da li da se eksportuju .dot i .png fajlovi'''

    meta_path = os.path.join(path, grammar_file_name)
    meta_name = os.path.splitext(meta_path)[0]
    metamodel = metamodel_from_file(meta_path)

    if export_dot:
        metamodel_export(metamodel, meta_name + '.dot')
        if export_png:
            graph = pydot.graph_from_dot_file(meta_name + '.dot')
            #graph[0].write_png(meta_name + '.png')

    model_path = os.path.join(path, example_file_name)
    model_name = os.path.splitext(model_path)[0]

    model = metamodel.model_from_file(model_path)

    if export_dot:
        model_export(model, model_name + '.dot')
    if export_png:
        graph = pydot.graph_from_dot_file(model_name + '.dot')
        #graph[0].write_png(model_name + '.png')

    #print(model.models[0].elements[0].datatype.charfield.parameters[0].max_length.number)
    '''proba = Proba()
    query_set = []
    query_set = proba.interpreter(model)'''

    models = model.models
    models1 = []
    for model in models:
        elements = model.elements
        dict = {}
        #elements1 = []
        dict['model'] = model.name
        dict['elements'] = elements
        '''for element in elements:
            dict['name'] = element.name
            if element.datatype.charfield is not None:
                dict['DataType'] = 'CharField'
                dict['maxLength'] = element.datatype.charfield.parameters[0].max_length.number
                dict['null'] = element.datatype.charfield.parameters[1].null.value
            else:
                dict['DataType'] = 'TextField'
                dict['maxLength'] = element.datatype.textfield.parameters[0].max_length.number
                dict['null'] = element.datatype.textfield.parameters[1].null.value'''
        print(dict)
        models1.append(dict)

    print('bla bla')
    print(models1)
    md5_object = hashlib.md5()

    #Generator koda za initial.py
    def test(models):
        string = 'from __future__ import unicode_literals\nfrom django.db import migrations, models\nimport django.db.models.deletion\nimport django.utils.timezone\n\n\nclass Migration(migrations.Migration):\n\n\tinitial = True\n\n\tdependencies = [\n\t]\n\n\toperations = ['
        for model in models:
            string += '\n\t\t'
            string += 'migrations.CreateModel('
            string += '\n\t\t\tname=' + "'" + str(model['model']) + "',"
            string += '\n\t\t\tfields=['
            string += '\n\t\t\t\t(' + "'id'" + ",models.AutoField" + "(auto_created=True, primary_key=True, serialize=False, verbose_name=" + "'ID')),"
            for element in model['elements']:
                string += '\n\t\t\t\t(' + "'"
                string += element.name + "'," + "models."

                if element.datatype.foreignkey is not None:
                    string += 'ForeignKey('
                    if element.datatype.foreignkey.parameters[0].default is not None:
                        string += 'default=' + element.datatype.foreignkey.parameters[0].default.number
                    if element.datatype.foreignkey.parameters[0].on_delete is not None:
                        string += 'on_delete=django.db.models.deletion.CASCADE, '
                    string += 'to=' + "'" + 'myapp.' + element.datatype.foreignkey.classs + "')),"

                elif element.datatype.charfield is not None:
                    string += 'CharField' + "("

                    if len(element.datatype.charfield.parameters) == 0:
                        string += ")),"

                    elif len(element.datatype.charfield.parameters) == 1:
                        if element.datatype.charfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ")),"
                        if element.datatype.charfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.charfield.parameters[0].null.value + ")),"
                        if element.datatype.charfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.charfield.parameters[0].default.number + ")),"

                    elif len(element.datatype.charfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.charfield.parameters[2].default.number + ")),"

                    elif element.datatype.charfield.parameters[0].max_length and element.datatype.charfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ")),"

                    elif element.datatype.charfield.parameters[0].null and element.datatype.charfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.charfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.charfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.charfield.parameters[0].max_length and element.datatype.charfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.charfield.parameters[1].default.number + ")),"

                    elif element.datatype.charfield.parameters[0].default and element.datatype.charfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.charfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.charfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.charfield.parameters[0].null and element.datatype.charfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.charfield.parameters[0].null.value + ","
                        string += 'default=' + element.datatype.charfield.parameters[1].default.number + ")),"

                    elif element.datatype.charfield.parameters[0].default and element.datatype.charfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.charfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ")),"

                elif element.datatype.emailfield is not None:
                    string += 'EmailField' + "("

                    if len(element.datatype.emailfield.parameters) == 0:
                        string += ")),"

                    elif len(element.datatype.emailfield.parameters) == 1:
                        if element.datatype.emailfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ")),"
                        if element.datatype.emailfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ")),"
                        if element.datatype.emailfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ")),"

                    elif len(element.datatype.emailfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.emailfield.parameters[2].default.number + ")),"

                    elif element.datatype.emailfield.parameters[0].max_length and element.datatype.emailfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ")),"

                    elif element.datatype.emailfield.parameters[0].null and element.datatype.emailfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.emailfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.emailfield.parameters[0].max_length and element.datatype.emailfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.emailfield.parameters[1].default.number + ")),"

                    elif element.datatype.emailfield.parameters[0].default and element.datatype.emailfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.emailfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.emailfield.parameters[0].null and element.datatype.emailfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ", "
                        string += 'default=' + element.datatype.emailfield.parameters[1].default.number + ")),"

                    elif element.datatype.emailfield.parameters[0].default and element.datatype.emailfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ")),"


                elif element.datatype.datetimefield is not None:
                    string += 'DateTimeField' + "("

                    if len(element.datatype.datetimefield.parameters) == 0:
                        string += ")),"

                    elif len(element.datatype.datetimefield.parameters) == 1:
                        if element.datatype.datetimefield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ")),"
                        if element.datatype.datetimefield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ")),"
                        if element.datatype.datetimefield.parameters[0].default is not None:
                            string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"

                    elif len(element.datatype.datetimefield.parameters) == 3:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ", "
                        string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"

                    elif element.datatype.datetimefield.parameters[0].max_length and element.datatype.datetimefield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ")),"

                    elif element.datatype.datetimefield.parameters[0].null and element.datatype.datetimefield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.datetimefield.parameters[1].max_length.number + ")),"

                    elif element.datatype.datetimefield.parameters[0].max_length and element.datatype.datetimefield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"

                    elif element.datatype.datetimefield.parameters[0].default and element.datatype.datetimefield.parameters[1].max_length is not None:
                        string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"
                        string += 'max_length=' + element.datatype.datetimefield.parameters[1].max_length.number + ")),"

                    elif element.datatype.datetimefield.parameters[0].null and element.datatype.datetimefield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ", "
                        string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"

                    elif element.datatype.datetimefield.parameters[0].default and element.datatype.datetimefield.parameters[1].null is not None:
                        string += 'default=django.utils.timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")),"
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ")),"


                elif element.datatype.booleanfield is not None:
                    string += 'BooleanField' + "("

                    if len(element.datatype.booleanfield.parameters) == 0:
                        string += ")),"

                    else:
                        string += 'default=' + element.datatype.booleanfield.parameters[0].default.value + ')),'


                else:
                    string += 'IntegerField' + "("

                    if len(element.datatype.integerfield.parameters) == 0:
                        string += ")),"

                    elif len(element.datatype.integerfield.parameters) == 1:
                        if element.datatype.integerfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ")),"
                        if element.datatype.integerfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ")),"
                        if element.datatype.integerfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ")),"

                    elif len(element.datatype.integerfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[2].default.number + ")),"

                    elif element.datatype.integerfield.parameters[0].max_length and element.datatype.integerfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ")),"

                    elif element.datatype.integerfield.parameters[0].null and element.datatype.integerfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.integerfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.integerfield.parameters[0].max_length and element.datatype.integerfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[1].default.number + ")),"

                    elif element.datatype.integerfield.parameters[0].default and element.datatype.integerfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.integerfield.parameters[1].max_length.number + ")),"

                    elif element.datatype.integerfield.parameters[0].null and element.datatype.integerfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[1].default.number + ")),"

                    elif element.datatype.integerfield.parameters[0].default and element.datatype.integerfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ")),"

            string += '\n\t\t\t],'
            string += '\n\t\t),'
        string += '\n\t]'
        return string


    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/migrations/0001_initial.py', 'w') as f:
        a = test(models1)
        f.write(a)

    # Generator koda za models.py
    def test1(models):
        string = 'import os\nfrom django.db import models\nfrom django.utils import timezone'
        for model in models:
            string += '\n\nclass '
            string += str(model['model']) + "(" + 'models.Model' + "):"
            for element in model['elements']:
                string += '\n\t'
                string += element.name + "=" + "models."

                if element.datatype.foreignkey is not None:
                    string += 'ForeignKey(' + element.datatype.foreignkey.classs + ', ' + 'on_delete=models.CASCADE'
                    if element.datatype.foreignkey.parameters[0].default is not None:
                        string += ', ' + 'default=' + element.datatype.foreignkey.parameters[0].default.number + ')'
                    else:
                        string += ')'

                elif element.datatype.charfield is not None:
                    string += 'CharField' + "("

                    if len(element.datatype.charfield.parameters) == 0:
                        string += ")"

                    elif len(element.datatype.charfield.parameters) == 1:
                        if element.datatype.charfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ")"
                        if element.datatype.charfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.charfield.parameters[0].null.value + ")"
                        if element.datatype.charfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.charfield.parameters[0].default.number + ")"

                    elif len(element.datatype.charfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.charfield.parameters[2].default.number + ")"

                    elif element.datatype.charfield.parameters[0].max_length and element.datatype.charfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ")"

                    elif element.datatype.charfield.parameters[0].null and element.datatype.charfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.charfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.charfield.parameters[1].max_length.number + ")"

                    elif element.datatype.charfield.parameters[0].max_length and element.datatype.charfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.charfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.charfield.parameters[1].default.number + ")"

                    elif element.datatype.charfield.parameters[0].default and element.datatype.charfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.charfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.charfield.parameters[1].max_length.number + ")"

                    elif element.datatype.charfield.parameters[0].null and element.datatype.charfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.charfield.parameters[0].null.value + ","
                        string += 'default=' + element.datatype.charfield.parameters[1].default.number + ")"

                    elif element.datatype.charfield.parameters[0].default and element.datatype.charfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.charfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.charfield.parameters[1].null.value + ")"


                elif element.datatype.emailfield is not None:
                    string += 'EmailField' + "("

                    if len(element.datatype.emailfield.parameters) == 0:
                        string += ")"

                    elif len(element.datatype.emailfield.parameters) == 1:
                        if element.datatype.emailfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ")"
                        if element.datatype.emailfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ")"
                        if element.datatype.emailfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ")"

                    elif len(element.datatype.emailfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.emailfield.parameters[2].default.number + ")"

                    elif element.datatype.emailfield.parameters[0].max_length and element.datatype.emailfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ")"

                    elif element.datatype.emailfield.parameters[0].null and element.datatype.emailfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.emailfield.parameters[1].max_length.number + ")"

                    elif element.datatype.emailfield.parameters[0].max_length and element.datatype.emailfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.emailfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.emailfield.parameters[1].default.number + ")"

                    elif element.datatype.emailfield.parameters[0].default and element.datatype.emailfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.emailfield.parameters[1].max_length.number + ")"

                    elif element.datatype.emailfield.parameters[0].null and element.datatype.emailfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.emailfield.parameters[0].null.value + ","
                        string += 'default=' + element.datatype.emailfield.parameters[1].default.number + ")"

                    elif element.datatype.emailfield.parameters[0].default and element.datatype.emailfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.emailfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.emailfield.parameters[1].null.value + ")"


                elif element.datatype.datetimefield is not None:
                    string += 'DateTimeField' + "("

                    if len(element.datatype.datetimefield.parameters) == 0:
                        string += ")"

                    elif len(element.datatype.datetimefield.parameters) == 1:
                        if element.datatype.datetimefield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ")"
                        if element.datatype.datetimefield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ")"
                        if element.datatype.datetimefield.parameters[0].default is not None:
                            string += 'default=timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ")"

                    elif len(element.datatype.datetimefield.parameters) == 3:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ", "
                        string += 'default=timezone.' + element.datatype.datetimefield.parameters[2].default.timezone.var + ")"

                    elif element.datatype.datetimefield.parameters[0].max_length and element.datatype.datetimefield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ")"

                    elif element.datatype.datetimefield.parameters[0].null and element.datatype.datetimefield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.datetimefield.parameters[1].max_length.number + ")"

                    elif element.datatype.datetimefield.parameters[0].max_length and element.datatype.datetimefield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.datetimefield.parameters[0].max_length.number + ", "
                        string += 'default=timezone.' + element.datatype.datetimefield.parameters[1].default.timezone.var + ")"

                    elif element.datatype.datetimefield.parameters[0].default and element.datatype.datetimefield.parameters[1].max_length is not None:
                        string += 'default=timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ", "
                        string += 'max_length=' + element.datatype.datetimefield.parameters[1].max_length.number + ")"

                    elif element.datatype.datetimefield.parameters[0].null and element.datatype.datetimefield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.datetimefield.parameters[0].null.value + ","
                        string += 'default=timezone.' + element.datatype.datetimefield.parameters[1].default.timezone.var + ")"

                    elif element.datatype.datetimefield.parameters[0].default and element.datatype.datetimefield.parameters[1].null is not None:
                        string += 'default=timezone.' + element.datatype.datetimefield.parameters[0].default.timezone.var + ", "
                        string += 'null=' + element.datatype.datetimefield.parameters[1].null.value + ")"


                elif element.datatype.booleanfield is not None:
                    string += 'BooleanField' + "("

                    if len(element.datatype.booleanfield.parameters) == 0:
                        string += ")"

                    else:
                        string += 'default=' + element.datatype.booleanfield.parameters[0].default.value + ')'

                else:
                    string += 'IntegerField' + "("

                    if len(element.datatype.integerfield.parameters) == 0:
                        string += ")"

                    elif len(element.datatype.integerfield.parameters) == 1:
                        if element.datatype.integerfield.parameters[0].max_length is not None:
                            string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ")"
                        if element.datatype.integerfield.parameters[0].null is not None:
                            string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ")"
                        if element.datatype.integerfield.parameters[0].default is not None:
                            string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ")"

                    elif len(element.datatype.integerfield.parameters) == 3:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[2].default.number + ")"

                    elif element.datatype.integerfield.parameters[0].max_length and element.datatype.integerfield.parameters[1].null is not None:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ")"

                    elif element.datatype.integerfield.parameters[0].null and element.datatype.integerfield.parameters[1].max_length is not None:
                        string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ", "
                        string += 'max_length=' + element.datatype.integerfield.parameters[1].max_length.number + ")"

                    elif element.datatype.integerfield.parameters[0].max_length and element.datatype.integerfield.parameters[1].default is not None:
                        string += 'max_length=' + element.datatype.integerfield.parameters[0].max_length.number + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[1].default.number + ")"

                    elif element.datatype.integerfield.parameters[0].default and element.datatype.integerfield.parameters[1].max_length is not None:
                        string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ", "
                        string += 'max_length=' + element.datatype.integerfield.parameters[1].max_length.number + ")"

                    elif element.datatype.integerfield.parameters[0].null and element.datatype.integerfield.parameters[1].default is not None:
                        string += 'null=' + element.datatype.integerfield.parameters[0].null.value + ", "
                        string += 'default=' + element.datatype.integerfield.parameters[1].default.number + ")"

                    elif element.datatype.integerfield.parameters[0].default and element.datatype.integerfield.parameters[1].null is not None:
                        string += 'default=' + element.datatype.integerfield.parameters[0].default.number + ", "
                        string += 'null=' + element.datatype.integerfield.parameters[1].null.value + ")"

            string += '\n\n'
            string += '\n\tdef __str__(self):\n'
            string += '\t\treturn '
            counter = 0
            for element in model['elements']:
                if element.datatype.charfield is not None:
                    counter = counter + 1
            for element in model['elements']:
                if element.datatype.charfield is not None:
                    string += 'self.' + element.name
                    counter = counter - 1
                    if counter == 0:
                        string += ''
                    else:
                        string += ' + ' + '"/"' + ' + '

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/models.py', 'w') as f:
        a = test1(models1)
        f.write(a)

    #Generator koda za views.py
    def test2(models):
        string = 'from django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.core.urlresolvers import reverse_lazy, reverse\nfrom django.shortcuts import render, redirect\n'
        string += 'from django.contrib.auth import authenticate, login, logout\n'
        string += 'from .forms import UserForm\n'
        for model in models:
            string += '\n'
            string += 'from .models import ' + str(model['model'])
        string += '\n\ndef index(request):\n'
        string += '\treturn render(request, ' + "'" + 'layout/index.html' + "')\n"
        for model in models:
            #CreateView generator
            string += '\n\n'
            string += '#Create view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'CreateView' + '(CreateView):'
            string += '\n\ttemplate_name=' + "'" + 'layout/' + str(model['model']) + 'CreateView.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tfields=['
            last = len(model['elements']) - 1
            for i, element in enumerate(model['elements']):
                string += "'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n\tsuccess_url=reverse_lazy(' + "'myapp:" + str(model['model']) + "ListView'" + ")"

            #UpdateView generator
            string += '\n\n'
            string += '#Update view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'UpdateView' + '(UpdateView):'
            string += '\n\ttemplate_name=' + "'" + 'layout/' + str(model['model']) + 'UpdateView.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tfields=['
            last = len(model['elements']) - 1
            for i, element in enumerate(model['elements']):
                string += "'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n\tsuccess_url=reverse_lazy(' + "'myapp:" + str(model['model']) + "ListView'" + ")"

            #DeleteView generator
            string += '\n\n'
            string += '#Delete view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'DeleteView' + '(DeleteView):'
            string += '\n\ttemplate_name=' + "'layout/" + str(model['model']) + 'ListView.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\t#success_url=reverse_lazy(' + "'" + "'" + ')\n\n'

            string += '\tdef __init__(self, **kwargs):\n'
            string += '\t\tsuper(' + str(model['model']) + 'DeleteView, self).__init__(**kwargs)\n'
            string += '\t\tself.request = None\n\n'
            string += '\tdef get_success_url(self):\n'
            string += '\t\t#Redirect to previous url\n'
            string += '\t\treturn self.request.META.get(' + "'" + 'HTTP_REFERER' + "'" + ', None)\n'

            #ListView generator
            string += '\n\n'
            string += '#List view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'ListView' + '(generic.ListView):'
            string += '\n\ttemplate_name=' + "'layout/" + str(model['model']) + 'ListView.html' + "'"
            string += '\n\tcontext_object_name=' + "'" + 'all_' + str(model['model']) + "'"
            string += '\n\tdef get_queryset(self):'
            string += '\n\t\treturn ' + str(model['model']) + '.objects.all'

            #DetailView generator
            string += '\n\n'
            string += '#Detail view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'DetailView' + '(generic.DetailView):\n'
            string += '\ttemplate_name = ' + "'" + 'layout/' + str(model['model']) + 'DetailView.html' + "'\n"
            string += '\tmodel = ' + str(model['model']) + '\n\n'
            string += "\t'''\n"
            string += '\tdef get_context_data(self, **kwargs):\n'
            string += '\t\tcontext = super(' + str(model['model']) + 'DetailView, self).get_context_data(**kwargs)\n'
            string += '\t\tcontext["@context_name@"] = @model_name@.objects.all()\n'
            string += '\t\treturn context\n'
            string += "\t'''\n"

        #Generator koda za search
        string += '\n#Generated search for all field in database.\n'
        string += 'def search(request):\n'
        string += '\tif ' + "'" + 'q' + "'" + ' in request.GET and request.GET[' + "'" + 'q' + "'" + ']:\n'
        string += '\t\tq = request.GET[' + "'" + 'q' + "'" + ']\n'
        for model in models:
            string += '\t\t' + str(model['model']).lower() + ' = '
            for i, element in enumerate(model['elements']):
                last = len(model['elements']) - 1
                if element.datatype.foreignkey:
                    string += ''
                else:
                    string += str(model['model']) + '.objects.filter(' + element.name + '__icontains=q)'
                    if i == last:
                        string += '\n'
                    else:
                        string += ' or '
        string += '\n\t\treturn render(request, ' + "'" + 'layout/search.html' + "'" + ', {'
        for model in models:
            string += "'" + str(model['model']).lower() + "'" + ': ' + str(model['model']).lower() + ', '
        string += "'" + 'query' + "'" + ': q})\n\n'


        #Generator koda za login
        string += '#Generated login\n'
        string += 'def login_view(request):\n'
        string += '\ttitle = "Login"\n'
        string += '\tform = UserForm(request.POST or None)\n'
        string += '\tif form.is_valid():\n'
        string += '\t\tusername = form.cleaned_data.get("username")\n'
        string += '\t\tpassword = form.cleaned_data.get("password")\n'
        string += '\t\tuser = authenticate(username=username, password=password)\n'
        string += '\t\tlogin(request, user)\n'
        string += '\t\treturn redirect(' + "'" + 'myapp:index' + "'" + ')\n'
        string += '\treturn render(request, "layout/login.html", {"form": form, "title": title})\n\n'


        #Generator koda za logout
        string += '#Generated logout\n'
        string += 'def logout_view(request):\n'
        string += '\tlogout(request)\n'
        string += '\treturn redirect(' + "'" + 'myapp:login' + "'" + ')\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/views.py', 'w') as f:
        a = test2(models1)
        f.write(a)

    #Generator koda za urls.py u okviru aplikacije
    def test3(models):
        string = 'from django.conf.urls import url\nfrom . import views\n'
        string += '\n' + 'app_name = ' + "'" + 'myapp' + "'"
        string += '\n\nurlpatterns = [' + '\n'
        string += '\t#Generated index/Home page url\n'
        string += '\turl(r'+"'"+'^Home/$'+"'"+', views.index, name='+"'"+'index'+"'"+'),\n\n'
        for model in models:
            string += '\t#Generated ' + str(model['model']) + ' ListView url\n'
            string += '\turl(r' + "'" + '^'
            string += str(model['model']) + '/List/$' + "'" + ', views.'
            string += str(model['model']) + 'ListView.as_view(), name=' + "'"
            string += str(model['model']) + 'ListView' + "'),\n"
        string += '\n'

        for model in models:
            string += '\t#Generated ' + str(model['model']) + ' CreateView url\n'
            string += '\turl(r' + "'" + '^'
            string += str(model['model']) + '/Create/$' + "'" + ', views.'
            string += str(model['model']) + 'CreateView.as_view(), name=' + "'"
            string += str(model['model']) + 'CreateView' + "'),\n"
        string += '\n'

        for model in models:
            string += '\t#Generated ' + str(model['model']) + ' UpdateView url\n'
            string += '\turl(r' + "'" + '^'
            string += str(model['model']) + '/Update/(?P<pk>[0-9]+)/$' + "'" + ', views.'
            string += str(model['model']) + 'UpdateView.as_view(), name=' + "'"
            string += str(model['model']) + 'UpdateView' + "'),\n"
        string += '\n'

        for model in models:
            string += '\t#Generated ' + str(model['model']) + ' DeleteView url\n'
            string += '\turl(r' + "'" + '^'
            string += str(model['model']) + '/Delete/(?P<pk>[0-9]+)/$' + "'" + ', views.'
            string += str(model['model']) + 'DeleteView.as_view(), name=' + "'"
            string += str(model['model']) + 'DeleteView' + "'),\n"
        string += '\n'

        for model in models:
            string += '\t#Generated ' + str(model['model']) + ' DetailView url\n'
            string += '\turl(r' + "'" + '^'
            string += str(model['model']) + '/(?P<pk>[0-9]+)/Detail/$' + "'" + ', views.'
            string += str(model['model']) + 'DetailView.as_view(), name=' + "'"
            string += str(model['model']) + 'DetailView' + "'),\n"
        string += '\n'

        string += '\t#Generated Search url\n'
        string += '\turl(r' + "'" + '^search/$' + "'" + ', views.search, name=' + "'" + 'search' + "'),\n\n"

        string += '\t#Generated LogIn url\n'
        string += '\turl(r' + "'" + '^$' + "'" + ', views.login_view, name=' + "'" + 'login' + "'),\n\n"

        string += '\t#Generated LogOut url\n'
        string += '\turl(r' + "'" + '^logout/$' + "'" + ', views.logout_view, name=' + "'" + 'logout' + "'),\n\n"


        string += ']'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/urls.py', 'w') as f:
        a = test3(models1)
        f.write(a)

    #Generator koda za admin.py
    def test4(models):
        string = 'from django.contrib import admin\nfrom .models import '
        last = len(models) - 1
        for i, model in enumerate(models):
            string += str(model['model'])
            if i == last:
                string += '' + '\n'
            else:
                string += ', '
        for model in models:
            string += '\n'
            string += 'admin.site.register(' + str(model['model']) + ')'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/admin.py', 'w') as f:
        a = test4(models1)
        f.write(a)

    #Generator koda za urls.py u okviru projekta
    def test5(models):
        string = '"""prject URL Configuration\n\n'
        string += 'The `urlpatterns` list routes URLs to views. For more information please see:\n\t'
        string += 'The `urlpatterns` list routes URLs to views. For more information please see:\n'
        string += 'Examples:\n'
        string += 'Function views\n\t'
        string += '1. Add an import:  from my_app import views\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" + '^$' + "'" +', views.home, name=' + "'" + 'home' + "'" + ')\n'
        string += 'Class-based views\n\t'
        string += '1. Add an import:  from other_app.views import Home\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" + '^$' + "'" + ', Home.as_view(), name=' + "'" + 'home' + "'" + ')\n'
        string += 'Including another URLconf\n\t'
        string += '1. Import the include() function: from django.conf.urls import url, include\n\t'
        string += '2. Add a URL to urlpatterns:  url(r' + "'" '^blog/' + "'" + ', include(' + "'" + 'blog.urls' + "'" + '))\n'
        string += '"""\n'
        string += 'from django.conf.urls import include, url\n'
        string += 'from django.contrib import admin\n\n'
        string += 'urlpatterns = [\n\t'
        string += 'url(r' + "'" + '^admin/' + "', " + 'admin.site.urls),\n\t'
        string += 'url(r' + "'" + '^myapp/' + "', " + 'include(' + "'myapp.urls'" + ')),\n'
        string += ']'

        return string


    with open('C:/Users/Johny/Desktop/mrk/mysite/mysite/urls.py', 'w') as f:
        a = test5(models1)
        f.write(a)


    #Kreiranje template i layout deirektorijuma
    newpath = r'C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout'
    if not os.path.exists(newpath):
        os.makedirs(newpath)


    #Generator base.html stranice
    def test6(models):
        string = '<!DOCTYPE html>\n'
        string += '<html lang = "en">\n'
        string += '<head>\n'
        string += '\t<meta charset = "UTF-8">\n'
        string += '\t<title> {% block title %}Application{% endblock %} </title>\n'
        string += '\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">\n'
        string += '\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">\n'
        string += '\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>\n'
        string += '\t<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        string += '\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n'
        string += '\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>\n'
        string += '\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n'
        string += '</head>\n'
        string += '<body background="http://www.designbolts.com/wp-content/uploads/2013/02/Grunge-Seamless-Pattern-For-Website-Background.jpg">\n'
        string += '\t<nav class="navbar navbar-inverse">\n'
        string += '\t\t<div class="container-fluid">\n'
        string += '\t\t{% if user.is_authenticated %}\n'
        string += '\t\t\t<div class="navbar-header">\n'
        string += '\t\t\t\t<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#topNavBar">\n'
        string += '\t\t\t\t\t<span class="icon-bar"></span>\n'
        string += '\t\t\t\t\t<span class="icon-bar"></span>\n'
        string += '\t\t\t\t\t<span class="icon-bar"></span>\n'
        string += '\t\t\t\t</button>\n'
        string += '\t\t\t\t<a class="navbar-brand" href="{% url '+"'"+'myapp:index'+"'"+' %}" style="color:white">Home Page</a>\n'
        string += '\t\t\t</div>\n'
        string += '\t\t\t<div class="collapse navbar-collapse" id="topNavBar">\n'
        string += '\t\t\t\t<form class="navbar-form navbar-left" role="search" method="get" action="{% url ' + "'" + 'myapp:search' + "'" + ' %}">\n'
        string += '\t\t\t\t\t<div class="form-group">\n'
        string += '\t\t\t\t\t\t<input type="text" class="form-control" name="q" value="" size="32">\n'
        string += '\t\t\t\t\t</div>\n'
        string += '\t\t\t\t\t<button type="submit" class="btn btn-default">Search</button>\n'
        string += '\t\t\t\t</form>\n'
        string += '\t\t\t\t<ul class="nav navbar-nav navbar-right">\n'
        string += '\t\t\t\t{% if user.is_superuser %}\n'
        string += '\t\t\t\t\t<li>\n'
        string += '\t\t\t\t\t\t<a href="{% url ' + "'" + 'admin:index' + "'" + ' %}">Admin</a>\n'
        string += '\t\t\t\t\t</li>\n'
        string += '\t\t\t\t{% endif %}\n'
        string += '\t\t\t\t\t<li>\n'
        string += '\t\t\t\t\t\t<a href="{% url ' + "'" + 'myapp:logout' + "'" + ' %}" style="color:white">\n'
        string += '\t\t\t\t\t\t\t<span class="glyphicon glyphicon-off" aria-hidden="true"></span> LogOut\n'
        string += '\t\t\t\t\t\t</a>\n'
        string += '\t\t\t\t\t</li>\n'
        string += '\t\t\t\t</ul>\n'
        string += '\t\t\t</div>\n'
        string += '\t\t{% endif %}\n'
        string += '\t\t</div>\n'
        string += '\t</nav>\n'
        string += '\t<div class="col-md-9">\n'
        string += '\t\t{% block body %}\n\n'
        string += '\t\t{% endblock %}\n'
        string += '\t</div>\n'

        string += '</body>\n'

        return string


    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/base.html', 'w') as f:
        a = test6(models1)
        f.write(a)


    #Generator index.html stranice
    def test7(models):
        string = '{% extends '+"'"+'layout/base.html'+"'" + ' %}' +'\n\n'
        string += '{% block body %}\n\n'
        string += '\t<style>\n'
        string += '\t\tdiv.one {\n'
        string += '\t\t\tbackground-color:#F7F3F3;\n'
        string += '\t\t\tbackground-image:url("http://www.cuded.com/wp-content/uploads/2013/06/30-Black-Background.jpg");\n'
        string += '\t\t\tcolor:black;\n'
        string += '\t\t\twidth:25.33%;\n'
        string += '\t\t\theight:250px;\n'
        string += '\t\t\tfloat:left;\n'
        string += '\t\t\tmargin:4%;\n'
        string += '\t\t\tborder-radius:25%;\n'
        string += '\t\t}\n'
        string += '\t\th1.one {\n'
        string += '\t\t\tposition:relative;\n'
        string += '\t\t\ttop:35%;\n'
        string += '\t\t\ttext-align:center;\n'
        string += '\t\t\tletter-spacing:3px;\n'
        string += '\t\t}\n'
        string += '\t\tfont.one {\n'
        string += '\t\t\tfont-family:Comic sans MS;\n'
        string += '\t\t\tcolor:red;\n'
        string += '\t\t}\n'
        string += '\t</style>\n'
        string += '\t{% if user.is_authenticated %}\n'

        for model in models:
            string += '\t\t<a href="{% url ' + "'" + 'myapp:'
            string += str(model['model']) + 'ListView' + "'" + '%}'
            string += '">\n'
            string += '\t\t\t<div class="one">\n'
            string += '\t\t\t\t<h1 class="one">'
            string += '<font class="one">' + str(model['model']) + '</font></h1>\n'
            string += '\t\t\t</div>\n'
            string += '\t\t</a>\n'

        string += '\t{% endif %}\n'
        string += '\n{% endblock %}\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/index.html', 'w') as f:
        a = test7(models1)
        f.write(a)


    #Generator templejta form.html
    def test8(models):
        string = '{% for field in form %}\n'
        string += '<div class="form-group">\n'
        string += '\t<div class="col-sm-offset-2 col-sm-12">\n'
        string += '\t\t<div class="col-sm-offset-6 col-sm-6">\n'
        string += '\t\t\t<span class="text-danger small">{{ field.error }}</span>\n'
        string += '\t\t</div>\n'
        string += '\t\t<label class="control-label col-sm-2">{{ field.label_tag }}</label>\n'
        string += '\t\t<div class="col-sm-10">{{ field }}</div>\n'
        string += '\t</div>\n'
        string += '</div>\n'
        string += '{% endfor %}\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/form.html', 'w') as f:
        a = test8(models1)
        f.write(a)

    # Generator ListView html za svaki model
    for model in models:
        def test9(models, model):
            string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
            string += '{% block body %}\n'
            string += '\t{% if user.is_authenticated %}\n'
            string += '\t{% if all_' + str(model.name) + ' %}\n'
            string += '\t\t<style>\n'
            string += '\t\t\ttable, th, td {\n'
            string += '\t\t\t\tborder: 2px solid black;\n'
            string += '\t\t\t\tpadding: 10px;\n'
            string += '\t\t\t\tmargin: 10%;\n'
            string += '\t\t\t\tmargin-top: 1%;\n'
            string += '\t\t\t\tmargin-bottom: 1%;\n'
            string += '\t\t\t}\n'
            string += '\t\t</style>\n'
            string += '\t\t<div class="dropdown" style="margin-left:10%">\n'
            string += '\t\t\t<button class="btn btn-default" type="button" data-toggle="dropdown" style="margin-top:0.5%">Models\n'
            string += '\t\t\t\t<span class="caret"></span>\n'
            string += '\t\t\t</button>\n'
            string += '\t\t\t<ul class="dropdown-menu">\n'
            for modelll in models:
                string += '\t\t\t\t<li><a href="{% url ' + "'" + 'myapp:' + str(modelll['model']) + 'ListView' + "'" + ' %}" style="color:black">' + str(modelll['model']) + '</a></li>\n'
            string += '\t\t\t</ul>\n'
            string += '\t\t</div>\n'
            string += '\t\t<table style="width:100%">\n'
            string += '\t\t\t<tr bgcolor="#D3D6FF">\n'
            for element in model.elements:
                if element.datatype.foreignkey is None:
                    string += '\t\t\t\t<th style="text-align:center">???</th>\n'
                    break
                break
            for element in model.elements:
                string += '\t\t\t\t<th style="text-align:center">' + element.name.upper() + ':</th>\n'
            string += '\t\t\t\t<th></th>\n'
            string += '\t\t\t</tr>\n'
            string += '\t\t{% for var in all_' + str(model.name) + ' %}\n'
            string += '\t\t\t<tr>\n'
            for element in model.elements:
                if element.datatype.foreignkey is None:
                    string += '\t\t\t\t<td style="text-align:center"><a href="{% url ' + "'" + 'myapp:' + str(model.name) + 'DetailView' + "'" + ' var.id %}"><button class="btn btn-info">{{ var.naziv }} Detail</button></a></td>\n'
                    break
                break
            for element in model.elements:
                string += '\t\t\t\t<td style="text-align:center">{{ var.' + element.name + ' }}</td>\n'
            string += '\t\t\t\t<td>\n'
            string += '\t\t\t\t\t<a href="{% url ' + "'" + 'myapp:' + str(model.name) + 'UpdateView' + "'" + ' var.id %}">\n'
            string += '\t\t\t\t\t\t<button type="submit" class="btn btn-warning btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Edit">\n'
            string += '\t\t\t\t\t\t\t<span class="glyphicon glyphicon-edit"></span>\n'
            string += '\t\t\t\t\t\t</button>\n'
            string += '\t\t\t\t\t</a>\n'
            string += '\t\t\t\t\t<form action="{% url ' + "'" + 'myapp:' + str(model.name) + 'DeleteView' + "'" + ' var.id %}" method="post" style="display: inline;">\n'
            string += '\t\t\t\t\t\t{% csrf_token %}\n'
            string += '\t\t\t\t\t\t<input type="hidden" name="var_id" value="{{ var.id }}" />\n'
            string += '\t\t\t\t\t\t<button type="submit" class="btn btn-danger btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Delete">\n'
            string += '\t\t\t\t\t\t\t<span class="glyphicon glyphicon-trash"></span>\n'
            string += '\t\t\t\t\t\t</button>\n'
            string += '\t\t\t\t\t</form>\n'
            string += '\t\t\t\t</td>\n'
            string += '\t\t\t</tr>\n'
            string += '\t\t{% endfor %}\n'
            string += '\t\t</table>\n'
            string += '\t{% endif %}\n'
            string += '\t<a href="{% url ' + "'" + 'myapp:' + str(model.name) + 'CreateView' + "'" + ' %}">\n'
            string += '\t\t<button style="margin-left:10%; width:100%" class="btn btn-primary">Add New ' + str(model.name) + '</button>\n'
            string += '\t</a>\n'
            string += '\t{% else %}\n'
            string += '\t\t<h1 align="center">You Are Not Logged In!!!</h1>\n'
            string += '\t\t<h3 align="center">If You Want To See ' + str(model.name) + 's List, You Have To Be '
            string += '<a href="{% url ' + "'" + 'myapp:login' + "'" + ' %}">Logged In!!!</a></h3>\n'
            string += '\t{% endif %}\n'
            string += '{% endblock %}\n'

            return string


        with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/'+str(model.name)+'ListView.html', 'w') as f:
            a = test9(models1, model)
            f.write(a)

    # Generator CreateView html za svaki model
    for model in models:
        def test10(models, model):
            string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
            string += '{% block body %}\n'
            string += '\t{% if user.is_authenticated %}\n'
            string += '\t<div class="container-fluid">\n'
            string += '\t\t<div class="row">\n'
            string += '\t\t\t<div class="col-sm-9 col-md-10">\n'
            string += '\t\t\t\t<div class="panel-body">\n'
            string += '\t\t\t\t\t<form class="form-horizontal" action="" method="post" enctype="multipart/form-data">\n'
            string += '\t\t\t\t\t\t{% csrf_token %}\n'
            string += '\t\t\t\t\t\t{% include ' + "'" + 'layout/form.html' + "'" + ' %}\n'
            string += '\t\t\t\t\t\t<div class="form-group">\n'
            string += '\t\t\t\t\t\t\t<div class="col-sm-offset-2 col-sm-10">\n'
            string += '\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-success">Create ' + str(model.name) + '</button>\n'
            for element in model.elements:
                if element.datatype.foreignkey is not None:
                    string += '\t\t\t\t\t\t\t\t<a href="{% url ' + "'" + 'myapp:' + element.datatype.foreignkey.classs + "CreateView'" + ' %}">\n'
                    string += '\t\t\t\t\t\t\t\t\t<button type="button" class="btn btn-info" data-toggle="tooltip" data-placement="top" title="Add missing ' + element.datatype.foreignkey.classs + '">\n'
                    string += '\t\t\t\t\t\t\t\t\t\t<span class="glyphicon glyphicon-zoom-in"></span>\n'
                    string += '\t\t\t\t\t\t\t\t\t</button>\n'
                    string += '\t\t\t\t\t\t\t\t</a>\n'
            string += '\t\t\t\t\t\t\t</div>\n'
            string += '\t\t\t\t\t\t</div>\n'
            string += '\t\t\t\t\t</form>\n'
            string += '\t\t\t\t</div>\n'
            string += '\t\t\t</div>\n'
            string += '\t\t</div>\n'
            string += '\t</div>\n'
            string += '\t{% else %}\n'
            string += '\t\t<h1 align="center">You Are Not Logged In!!!</h1>\n'
            string += '\t\t<h3 align="center">If You Want To Create/Add New ' + str(model.name) + ', You Have To Be '
            string += '<a href="{% url ' + "'" + 'myapp:login' + "'" + ' %}">Logged In!!!</a></h3>\n'
            string += '\t{% endif %}\n'
            string += '{% endblock %}\n'

            return string

        with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/'+str(model.name)+'CreateView.html', 'w') as f:
            a = test10(models1, model)
            f.write(a)

    # Generator UpdateView html za svaki model
    for model in models:
        def test11(models, model):
            string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
            string += '{% block body %}\n'
            string += '\t{% if user.is_authenticated %}\n'
            string += '\t<div class="container-fluid">\n'
            string += '\t\t<div class="row">\n'
            string += '\t\t\t<div class="col-sm-9 col-md-10">\n'
            string += '\t\t\t\t<div class="panel-body">\n'
            string += '\t\t\t\t\t<form class="form-horizontal" action="" method="post" enctype="multipart/form-data">\n'
            string += '\t\t\t\t\t\t{% csrf_token %}\n'
            string += '\t\t\t\t\t\t{% include ' + "'" + 'layout/form.html' + "'" + ' %}\n'
            string += '\t\t\t\t\t\t<div class="form-group">\n'
            string += '\t\t\t\t\t\t\t<div class="col-sm-offset-2 col-sm-10">\n'
            string += '\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-success">Update ' + str(model.name) + '</button>\n'
            for element in model.elements:
                if element.datatype.foreignkey is not None:
                    string += '\t\t\t\t\t\t\t\t<a href="{% url ' + "'" + 'myapp:' + element.datatype.foreignkey.classs + "CreateView'" + ' %}">\n'
                    string += '\t\t\t\t\t\t\t\t\t<button type="button" class="btn btn-info" data-toggle="tooltip" data-placement="top" title="Add missing ' + element.datatype.foreignkey.classs + '">\n'
                    string += '\t\t\t\t\t\t\t\t\t\t<span class="glyphicon glyphicon-zoom-in"></span>\n'
                    string += '\t\t\t\t\t\t\t\t\t</button>\n'
                    string += '\t\t\t\t\t\t\t\t</a>\n'
            string += '\t\t\t\t\t\t\t</div>\n'
            string += '\t\t\t\t\t\t</div>\n'
            string += '\t\t\t\t\t</form>\n'
            string += '\t\t\t\t</div>\n'
            string += '\t\t\t</div>\n'
            string += '\t\t</div>\n'
            string += '\t</div>\n'
            string += '\t{% else %}\n'
            string += '\t\t<h1 align="center">You Are Not Logged In!!!</h1>\n'
            string += '\t\t<h3 align="center">If You Want To Update ' + str(model.name) + ', You Have To Be '
            string += '<a href="{% url ' + "'" + 'myapp:login' + "'" + ' %}">Logged In!!!</a></h3>\n'
            string += '\t{% endif %}\n'
            string += '{% endblock %}\n'
            return string

        with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/'+str(model.name)+'UpdateView.html', 'w') as f:
            a = test11(models1, model)
            f.write(a)


    # Generator DetailView html za svaki model
    for model in models:
        def test12(models, model):
            a = ''
            string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
            string += '{% block body %}\n'
            string += '\t{% if user.is_authenticated %}\n'
            string += '\t\t<style>\n'
            string += '\t\t\ttable, th, td {\n'
            string += '\t\t\t\tborder: 2px solid black;\n'
            string += '\t\t\t\tpadding: 10px;\n'
            string += '\t\t\t\tmargin: 10%;\n'
            string += '\t\t\t\tmargin-top: 1%;\n'
            string += '\t\t\t\tmargin-bottom: 1%;\n'
            string += '\t\t\t}\n'
            string += '\t\t</style>\n'
            string += '\t\t<div class="dropdown" style="margin-left:10%">\n'
            string += '\t\t\t<button class="btn btn-default" type="button" data-toggle="dropdown" style="margin-top:0.5%">Models\n'
            string += '\t\t\t\t<span class="caret"></span>\n'
            string += '\t\t\t</button>\n'
            string += '\t\t\t<ul class="dropdown-menu">\n'
            for modelll in models:
                string += '\t\t\t\t<li><a href="{% url ' + "'" + 'myapp:' + str(
                    modelll['model']) + 'ListView' + "'" + ' %}" style="color:black">' + str(
                    modelll['model']) + '</a></li>\n'
            string += '\t\t\t</ul>\n'
            string += '\t\t</div>\n'

            for q in models:
                for element in q['elements']:
                    if element.datatype.foreignkey is not None and element.datatype.foreignkey.classs == model.name:
                        string += '\t<table style="width:100%">\n'
                        string += '\t\t<tr bgcolor="#D3D6FF">\n'
                        for element in q['elements']:
                            string += '\t\t\t<th style="text-align:center">' + element.name.upper() + '</th>\n'
                        string += '\t\t\t<th style="text-align:center"></th>\n'
                        string += '\t\t</tr>\n'
                        string += '\t{% for var in ' + model.name.lower() + '.' + str(q['model']).lower() + '_set.all %}\n'
                        string += '\t\t<tr>\n'
                        string += '\t\t\t{% if ' + model.name.lower() + '.id == var.' + model.name.lower() + '.id %}\n'
                        for element1 in q['elements']:
                            string += '\t\t\t\t<td style="text-align:center">{{ var.' + element1.name + ' }}</td>\n'
                        string += '\t\t\t\t<td style="text-align:center">\n'
                        string += '\t\t\t\t\t<a href="{% url ' + "'" + 'myapp:' + str(q['model']) + 'UpdateView' + "'" + ' var.id %}">\n'
                        string += '\t\t\t\t\t\t<button type="submit" class="btn btn-warning btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Edit">\n'
                        string += '\t\t\t\t\t\t\t<span class="glyphicon glyphicon-edit"></span>\n'
                        string += '\t\t\t\t\t\t</button>\n'
                        string += '\t\t\t\t\t</a>\n'
                        string += '\t\t\t\t\t<form action="{% url ' + "'" + 'myapp:' + str(q['model']) + 'DeleteView' + "'" + ' var.id %}" method="post" style="display: inline;">\n'
                        string += '\t\t\t\t\t\t{% csrf_token %}\n'
                        string += '\t\t\t\t\t\t<input type="hidden" name="var_id" value="{{ var.id }}" />\n'
                        string += '\t\t\t\t\t\t<button type="submit" class="btn btn-danger btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Delete">\n'
                        string += '\t\t\t\t\t\t\t<span class="glyphicon glyphicon-trash"></span>\n'
                        string += '\t\t\t\t\t\t</button>\n'
                        string += '\t\t\t\t\t</form>\n'
                        string += '\t\t\t\t</td>\n'
                        string += '\t\t\t{% endif %}\n'
                        string += '\t\t</tr>\n'
                        string += '\t{% endfor %}\n'
                        string += '\t</table>\n'
                        string += '\t<h5 align="center"><i>Table shows <b>'+ str(q['model']) + 's</b> for ' + model.name + '</i></h5><br><br><br>\n\n'


            string += '\t{% else %}\n'
            string += '\t\t<h1 align="center">You Are Not Logged In!!!</h1>\n'
            string += '\t\t<h3 align="center">If You Want To See ' + str(model.name) + 's Detail, You Have To Be '
            string += '<a href="{% url ' + "'" + 'myapp:login' + "'" + ' %}">Logged In!!!</a></h3>\n'
            string += '\t{% endif %}\n'
            string += '{% endblock %}\n'
            return string

        with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/'+str(model.name)+'DetailView.html', 'w') as f:
            a = test12(models1, model)
            f.write(a)


    #Generator za search.html
    def test13(models):
        string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
        string += '{% block body %}\n'
        string += '\t\t<style>\n'
        string += '\t\t\ttable, th, td {\n'
        string += '\t\t\t\tborder: 2px solid black;\n'
        string += '\t\t\t\tpadding: 10px;\n'
        string += '\t\t\t\tmargin: 10%;\n'
        string += '\t\t\t\tmargin-top: 1%;\n'
        string += '\t\t\t\tmargin-bottom: 10%;\n'
        string += '\t\t\t}\n'
        string += '\t\t</style>\n'
        string += '\t\t<div class="dropdown" style="margin-left:10%">\n'
        string += '\t\t\t<button class="btn btn-default" type="button" data-toggle="dropdown" style="margin-top:0.5%">Models\n'
        string += '\t\t\t\t<span class="caret"></span>\n'
        string += '\t\t\t</button>\n'
        string += '\t\t\t<ul class="dropdown-menu">\n'
        for modelll in models:
            string += '\t\t\t\t<li><a href="{% url ' + "'" + 'myapp:' + str(
                modelll['model']) + 'ListView' + "'" + ' %}" style="color:black">' + str(
                modelll['model']) + '</a></li>\n'
        string += '\t\t\t</ul>\n'
        string += '\t\t</div>\n\n'

        for model in models:
            string += '\t\t{% if ' + str(model['model']).lower() + ' %}\n'
            string += '\t\t\t<table style="width:100%">\n'
            string += '\t\t\t\t<tr bgcolor="#D3D6FF">\n'
            for element in model['elements']:
                string += '\t\t\t\t\t<th style="text-align:center">' + element.name.upper() + '</th>\n'
            string += '\t\t\t\t\t<th></th>\n'
            string += '\t\t\t\t</tr>\n'
            string += '\t\t\t\t{% for var in ' + str(model['model']).lower() + ' %}\n'
            string += '\t\t\t\t<tr>\n'
            for element in model['elements']:
                string += '\t\t\t\t\t<td style="text-align:center">{{ var.' + element.name + ' }}</td>\n'
            string += '\t\t\t<td>\n'
            string += '\t\t\t\t<a href="{% url ' + "'" + 'myapp:' + str(model['model']) + 'UpdateView' + "'" + ' var.id %}">\n'
            string += '\t\t\t\t\t<button type="submit" class="btn btn-warning btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Edit">\n'
            string += '\t\t\t\t\t\t<span class="glyphicon glyphicon-edit"></span>\n'
            string += '\t\t\t\t\t</button>\n'
            string += '\t\t\t\t</a>\n'
            string += '\t\t\t\t<form action="{% url ' + "'" + 'myapp:' + str(model['model']) + 'DeleteView' + "'" + ' var.id %}" method="post" style="display: inline;">\n'
            string += '\t\t\t\t\t{% csrf_token %}\n'
            string += '\t\t\t\t\t<input type="hidden" name="var_id" value="{{ var.id }}" />\n'
            string += '\t\t\t\t\t<button type="submit" class="btn btn-danger btn-sm" style="width:47%" data-toggle="tooltip" data-placement="top" title="Delete">\n'
            string += '\t\t\t\t\t\t<span class="glyphicon glyphicon-trash"></span>\n'
            string += '\t\t\t\t\t</button>\n'
            string += '\t\t\t\t</form>\n'
            string += '\t\t\t</td>\n'
            string += '\t\t\t\t</tr>\n'
            string += '\t\t\t\t{% endfor %}\n'
            string += '\t\t\t</table>\n'
            string += '\t\t{% endif %}\n\n'
        string += '{% endblock %}\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/search.html', 'w') as f:
        a = test13(models1)
        f.write(a)

    #Generator login forme -- form.py
    def test14(models):
        string = 'from django.contrib.auth.models import User\n'
        string += 'from django.contrib.auth import authenticate, login, logout\nfrom django import forms\n\n'
        string += 'class UserForm(forms.Form):\n'
        string += '\tusername = forms.CharField()\n'
        string += '\tpassword = forms.CharField(widget=forms.PasswordInput)\n\n'
        string += '\tclass Meta:\n'
        string += '\t\tmodel = User\n'
        string += '\t\tfields = [' + "'" + 'username' + "'" + ', ' + "'" + 'password' + "'" + ']\n\n'
        string += '\tdef clean(self, *args, **kwargs):\n'
        string += '\t\tusername = self.cleaned_data.get("username")\n'
        string += '\t\tpassword = self.cleaned_data.get("password")\n'
        string += '\t\tif username and password:\n'
        string += '\t\t\tuser = authenticate(username=username, password=password)\n'
        string += '\t\t\tif not user:\n'
        string += '\t\t\t\traise forms.ValidationError("This user does not exist")\n'
        string += '\t\t\tif not user.check_password(password):\n'
        string += '\t\t\t\traise forms.ValidationError("Incorrect password")\n'
        string += '\t\t\tif not user.is_active:\n'
        string += '\t\t\t\traise forms.ValidationError("This user is not longer active!")\n'
        string += '\t\treturn super(UserForm, self).clean(*args, **kwargs)\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/forms.py', 'w') as f:
        a = test14(models1)
        f.write(a)


    #Generator login.html stranice
    def test15(models):
        string = '{% extends ' + "'" + 'layout/base.html' + "'" + '%}\n\n'
        string += '{% block body %}\n'
        string += '\t<div class="container-fluid">\n'
        string += '\t\t<div class="row">\n'
        string += '\t\t\t<div class="col-sm-9 col-md-10">\n'
        string += '\t\t\t\t<div class="panel-body">\n'
        string += '\t\t\t\t\t<form class="form-horizontal" action="" method="post" enctype="multipart/form-data">\n'
        string += '\t\t\t\t\t\t{% csrf_token %}\n'
        string += '\t\t\t\t\t\t{% include ' + "'" + 'layout/form.html' + "'" + ' %}\n'
        string += '\t\t\t\t\t\t<div class="form-group">\n'
        string += '\t\t\t\t\t\t\t<div class="col-sm-offset-2 col-sm-10">\n'
        string += '\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-success">Log in</button>\n'
        string += '\t\t\t\t\t\t\t</div>\n'
        string += '\t\t\t\t\t\t</div>\n'
        string += '\t\t\t\t\t</form>\n'
        string += '\t\t\t\t</div>\n'
        string += '\t\t\t</div>\n'
        string += '\t\t</div>\n'
        string += '\t</div>\n'
        string += '{% endblock %}\n'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/login.html', 'w') as f:
        a = test15(models1)
        f.write(a)