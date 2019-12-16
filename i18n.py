"""Internationalization support for the app.

Currently it supports English and Spanish.
"""

import locale
import gettext
import configparser

def load_cfg():
    """Sets the app language based on config.cfg file.

    If the language is 'en' -> English.
    If the language is 'es' -> Spanish.
    Else, the app is set to the OS default language (it uses English for
    languages other than Spanish.)
    """
    config = configparser.ConfigParser()
    config.read("config.cfg")
    
    l = config.get('language', 'lang')
    
    if l == 'en':
        lang = gettext.translation('base', fallback=True)
    elif l == 'es':
        lang = gettext.translation('base', localedir='locales', languages=['es'])
    else:
        loc = locale.getlocale()
        if loc[0].startswith( ('Spanish', 'es') ):
            lang = gettext.translation('base', localedir='locales', languages=['es'])
        else:
            lang = gettext.translation('base', fallback=True)
    
    return lang.gettext