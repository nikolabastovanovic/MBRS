'''
Created on 06.12.2015.

@author: xx
'''

from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
import pydot, os


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
                    string += 'CharField' + "("

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

                else:
                    string += 'IntegerField' + "("

                    if len(element.datatype.integerfield.parameters) == 0:
                        string += ")"

                    if len(element.datatype.integerfield.parameters) == 1:
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

            string += '\n\n\t'
            string += "'''"
            string += '\n\tYou can chose one of these atributes to be returned instead of type object!'
            string += '\n\tdef __str__(self):'
            for element in model['elements']:
                string += '\n\t\treturn self.' + element.name
            string += '\n\t' + "'''"
        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/models.py', 'w') as f:
        a = test1(models1)
        f.write(a)

    #Generator koda za views.py
    def test2(models):
        string = 'from django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.core.urlresolvers import reverse_lazy, reverse\n'
        for model in models:
            string += '\n'
            string += 'from .models import ' + str(model['model'])
        for model in models:
            #CreateView generator
            string += '\n\n'
            string += '#Create view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'CreateView' + '(CreateView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tfields=['
            last = len(model['elements']) - 1
            for i, element in enumerate(model['elements']):
                string += "'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n\tsuccess_url=reverse_lazy(' + "'" + "'" + ")"

            # UpdateView generator
            string += '\n\n'
            string += '#Update view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'UpdateView' + '(UpdateView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tfields=['
            last = len(model['elements']) - 1
            for i, element in enumerate(model['elements']):
                string += "'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '

            # DeleteView generator
            string += '\n\n'
            string += '#Delete view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'DeleteView' + '(DeleteView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tmodel=' + str(model['model'])
            string += '\n\tsuccess_url=reverse_lazy(' + "'" + "'" + ")"

            # ListView generator
            string += '\n\n'
            string += '#List view for ' + str(model['model']) + ' model.\n'
            string += 'class ' + str(model['model']) + 'ListView' + '(generic.ListView):'
            string += '\n\ttemplate_name=' + "'" + '.html' + "'"
            string += '\n\tcontext_object_name=' + "'" + 'all_' + str(model['model']) + "'"
            string += '\n\tdef get_queryset(self):'
            string += '\n\t\treturn ' + str(model['model']) + '.object.all'

        return string

    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/views.py', 'w') as f:
        a = test2(models1)
        f.write(a)

    #Generator koda za urls.py u okviru aplikacije
    def test3(models):
        string = 'from django.conf.urls import url\nfrom . import views\n'
        string += '\n' + 'app_name = ' + "'" + 'myapp' + "'"
        string += '\n\nurlspaterns = [' + '\n\n' + ']'

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


    #Kreiranje template i layout deirektorojuma
    newpath = r'C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout'
    if not os.path.exists(newpath):
        os.makedirs(newpath)


    #Generator index.html stranice
    def test6(models):
        string = '<!DOCTYPE html>\n'
        string += '<html lang = "en">\n'
        string += '<head>\n'
        string += '\t<meta charset = "UTF-8">\n'
        string += '\t<title> {% block title %}MyApp{% endblock %} </title>\n'
        string += '\t{% load staticfiles %}\n'
        string += '\t<script src = "https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n'
        string += '\t<script src = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n'
        string += '</head>\n'
        string += '<body>\n'
        string += '</body>\n'


        return string


    with open('C:/Users/Johny/Desktop/mrk/mysite/myapp/templates/layout/index.html', 'w') as f:
        a = test6(models)
        f.write(a)