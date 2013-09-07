""" http://djangosnippets.org/snippets/174/

This middleware allows developers to "fake" browser support for HTTP methods. 
Even though most modern browsers only support GET and POST, the HTTP standard 
defines others. In the context of REST, PUT and DELETE are used for client 
interaction with the server.

For forms with a PUT or DELETE method, this middleware will change them to go 
through POST, and will include an invisible field called "method_middleware_transform" 
that carries the originally intended method.

So, <form method="PUT" ...>...</form> More or less becomes <form method="POST" ...>
<input type=hidden name="method_middleware_transform" value="PUT"></form> (with a few 
other minor HTML modifications)

The process is completely transparent to the developer... you never have to deal with
the fact that browsers don't support the standard methods.

One caveat is that server interaction via XMLHttpRequest (AJAX) requires special 
attention... this middleware won't properly setup your XMLHttpRequest to take advantage 
of this functionality.

This is a combination of the work of Jesse Lovelace and the Django CSRF middleware.
"""

import re
import itertools

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

_SUPPORTED_TRANSFORMS = ['PUT', 'DELETE']

_FORM_RE = re.compile(
    r'((<form\W[^>]*\bmethod=(\'|"|))(%s)((\'|"|)\b[^>]*>))' %
    '|'.join(_SUPPORTED_TRANSFORMS), re.IGNORECASE)

_MIDDLEWARE_KEY = 'method_middleware_transform'


class HttpMethodsMiddleware(object):

    def process_request(self, request):
        if request.POST and request.POST.has_key(_MIDDLEWARE_KEY):
            if request.POST[_MIDDLEWARE_KEY].upper() in _SUPPORTED_TRANSFORMS:
                request.method = request.POST[_MIDDLEWARE_KEY]
        return None

    def process_response(self, request, response):
        if response['Content-Type'].split(';')[0] in _HTML_TYPES:
            # ensure we don't add the 'id' attribute twice (HTML validity)
            idattributes = itertools.chain(("id='" + _MIDDLEWARE_KEY + "'",),
                                           itertools.repeat(''))

            def add_transform_field(match):
                """Returns the matched <form> tag with a modified method and
                the added <input> element"""
                return match.group(2) + "POST" + match.group(5) + \
                    "<div style='display:none;'>" + \
                    "<input type='hidden' " + idattributes.next() + \
                    " name='" + _MIDDLEWARE_KEY + "' value='" + \
                    match.group(4).upper() + "' /></div>"

            # Modify any POST forms
            response.content = _FORM_RE.sub(
                add_transform_field, response.content)
        return response
