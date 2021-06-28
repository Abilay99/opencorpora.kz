from django.conf import settings
from .urls import urlpatterns
def switch_lang_code(path, language):
    # get the supported language codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    # validate the inputs
    if path == '':
        raise Exception('Url path for language switch is empty')
    elif path[0] != '/':
        raise Exception('Url path for language does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)
    # split the parts of the path
    parts = path.split('/')
    # add or substitute the new language prefix
    if parts[1] in lang_codes:
        if not urlpatterns[0].pattern.prefix_default_language:
            if language != settings.LANGUAGE_CODE:
                parts[1] = language
            else:
                parts.pop(1)
        else:
            parts[1] = language
    else:
        if not urlpatterns[0].pattern.prefix_default_language and language != settings.LANGUAGE_CODE:
            parts[0] = '/' + language
    # return the full new path
    return '/'.join(parts)