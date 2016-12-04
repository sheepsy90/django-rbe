import inspect
import sys
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern

from django.core.management.base import BaseCommand
from django.shortcuts import render_to_response


class Command(BaseCommand):
    help = 'produces the documentation file for all available APIs'

    def handle(self, *args, **options):
        root_urlconf = __import__(settings.ROOT_URLCONF) # import root_urlconf module
        all_urlpatterns = root_urlconf.urls.urlpatterns # project's urlpatterns
        VIEW_NAMES = [] # maintain a global list

        def get_all_view_names(urlpatterns):
            for pattern in urlpatterns:
                if isinstance(pattern, RegexURLResolver):
                    get_all_view_names(pattern.url_patterns)
                elif isinstance(pattern, RegexURLPattern):
                    if 'api/' in pattern.regex.pattern:
                        assert pattern.callback.__doc__ is not None, "View function with /api/* found but __doc__ was None"
                        doc = pattern.callback.__doc__
                        doc = '\n'.join([e.lstrip() for e in doc.split('\n')])
                        VIEW_NAMES.append([pattern.regex.pattern.replace('$', ''), doc]) # add the view to the global list
        get_all_view_names(all_urlpatterns)

        content = render_to_response('api/api_doc_template.html', {'endpoints': VIEW_NAMES,
                                                               'base_url': 'https://rbe-network.org/'}).content
        with open('templates/api/api_doc_include.html', 'w') as f:
            f.write(content)

