# -*- coding: utf-8 -*-
"""
Create a settings_local.py as your local config
When run startup.py, it will try to load the settings_local.py first
Example:
1. for HOME_PATH, if you are running in windows, you can add your home path config in settings_local.py
2. for run mode, you your local, you may want to run in DEBUG=True, also use the settings_local.py
"""
from mylogger import mylogger

log = mylogger.get_instance()

HOME_PATH = "/home/"  

DEBUG = False

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
