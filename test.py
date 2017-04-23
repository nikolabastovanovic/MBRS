'''
Created on 06.12.2015.

@author: xx
'''


from execute import execute
import os

execute(os.path.split(__file__)[0], 'grammer.tx', 'test.test', True, True)