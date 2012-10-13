#! /usr/bin/env python
#coding=utf-8
import os
dir = 'D:\GitHub\datapanel'
for root, dirs, filename in os.walk(dir):
    for file in filename:
        thefilename = os.path.join(root, file)
        print  thefilename
        #thefilename = os.path.join(root, file).lower()
        if thefilename.endswith('.pyc'):
            os.remove(thefilename)
        if thefilename.endswith('.pyo'):
            os.remove(thefilename)
print "del all the pyc & pyo"