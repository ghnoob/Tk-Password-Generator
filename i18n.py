"""Internationalization support for the app."""

import locale
import gettext
from io import open

def set_lang():
    """Sets the language of the app based in the current locale.
    
    If the OS is in Spanish, the app uses the Spanish language files.
    Else, it uses the English ones (default)
    """
    # spanish
    loc = locale.getlocale()
    if loc[0].startswith( ('es', 'Spanish') ):
        es = gettext.translation('base', localedir='locales', languages=['es'])
        es.install()
        return es.gettext
        
    # english
    else:
        en = gettext.translation('base', localedir='locales', languages=['en'])
        en.install()
        return en.gettext