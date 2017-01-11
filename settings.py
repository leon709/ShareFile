# -*- coding: utf-8 -*-
"""
Create a settings_local.py as your local config
When run startup.py, it will try to load the settings_local.py first
"""
from mylogger import mylogger

log = mylogger.get_instance()

HOME_PATH = "/home/"  # linux style path, should change this path value if in windows

DEBUG = False

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
