def globalvar(request):
    SETTINGS = {
        'site_title': 'SIGPAE',
        'site_description': '160 characters description for search engines.',
        'site_logo_url': ''
    }
    return { 'SETTINGS': SETTINGS}