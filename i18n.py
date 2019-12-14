"""Internationalization support for the app."""

import locale
import gettext
from io import open

def set_lang():
    """Sets the language of the app based in the current locale.
    
    If the OS is in Spanish, the app uses the Spanish language files.
    Else, it uses the English string provided in the source code.
    """
    loc = locale.getlocale()
    if loc[0].startswith( ('Spanish', 'es') ):
        lang = gettext.translation('base', localedir='locales', languages=['es'])
    else:
        lang = gettext.translation('base', fallback=True)
    return lang.gettext