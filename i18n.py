import gettext
from io import open

def get_lang():
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