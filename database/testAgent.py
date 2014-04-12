#!/usr/bin/python
# -*- coding: utf-8 -*-

from classifierSVM import *
from data_storage import *
from twitter import *

db = DataStorage('localhost','root','','twitter')
twitter = Twitter(db,24744541)
classifier = ClassifierSVM('rbf',0.2,5,twitter)
classifier.buildModel()