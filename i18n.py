"""Internationalization support for the app."""

import gettext
from io import open

def get_lang():
    """Sets the language of the app.
    
    Reads the lang.txt file in locales folder.
    If the file says 'en' it sets the language to English.
    If it says 'es' it sets the language to Spanish.
    """
    file_ = open('./locales/lang.txt','r')
    lang = file_.read()
    file_.close()
    print(lang)
        
    # english
    if lang == 'en':
        en = gettext.translation('base', localedir='locales', languages=['en'])
        en.install()
        return en.gettext
        
    # spanish
    elif lang == 'es':
        es = gettext.translation('base', localedir='locales', languages=['es'])
        es.install()
        return es.gettext