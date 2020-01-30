"""Internationalization support for the app.

Currently it supports English and Spanish.
"""

import locale
import gettext
import configparser
import sys, os

def load_cfg():
    """Loads the language configuration from config.cfg file.
    
    If the config file does not exist or it does not have a language
    option, it creates a new cfg with default values.
    """
    config = configparser.ConfigParser()
    
    if (config.read('config.cfg') is False or
    config.has_option('language', 'lang') is False):
        #  create cfg with default values
        config['language'] = {'lang':'os'}
        with open('config.cfg', 'w') as configfile:
            config.write(configfile)
    
    return config.get('language', 'lang')
    
def set_lang():
    """Sets the app language based on config.cfg file.

    If the language is 'en' -> English.
    If the language is 'es' -> Spanish.
    Else, the app is set to the OS default language (it uses English for
    languages other than Spanish.)
    """
    l = load_cfg()
    if l == 'en':
        lang = gettext.translation('base', fallback=True)
    elif l == 'es':
        lang = gettext.translation('base', localedir='locales',
               languages=['es'])
    else:
        locale.setlocale(locale.LC_ALL, '')
        if locale.getlocale()[0].startswith( ('Spanish', 'es') ):
            lang = gettext.translation('base', localedir='locales',
                   languages=['es'])
        else:
            lang = gettext.translation('base', fallback=True)
    
    return lang.gettext

def save_cfg(val):
    """Saves the current user configuration in the config.cfg file."""
    config = configparser.ConfigParser()
    config.read('config.cfg')
    config.set('language', 'lang', val)

    with open('config.cfg', 'w') as configfile:
        config.write(configfile)

    # restart the app
    os.execv(sys.executable, ['python'] + sys.argv)