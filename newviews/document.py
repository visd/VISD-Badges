""" Here are a set of functions to auto-generate API documentations, with variations per user type.

Preferred text format is Markdown.
"""
from permits.configs.modifiers import base_config
from permits import methods as permit
from newviews import methods as vmethods

from badges import resource_configs

from settings import PROJECT_ROOT
from os import path

def api_for(user_role, group=None):
    config = permit.reduce_permissions_dictionary_to(user_role, base_config(group))
    return {user_role: api_dict(config=config)}

def meta_for(resource):
    description = resource_configs.config_from_verbose(resource).get('description')
    return {'description':description or ''}

def markdown_api(user_role, group=None, filename='api'):
    filename = '_'.join([filename,user_role])
    if group:
        filename = '_'.join([filename,group])
    filename += '.md'
    api_dict = api_for(user_role, group)
    md = ['## Badges API']
    md.append('For users in the `%s` role.' % user_role)
    if group:
        md.append('Also with extra permissions for the `%s` group.' % group)
    for res, di in api_dict[user_role].items():
        md.append('### %s' % res.title())
        md.append(di['meta']['description'])
        for url in di['urls']:
            md.append('\n    %s - %s\n' % (url['url'], url['method']))
            if url.get('fields'):
                fields_string = ', '.join(url['fields'])
                if url['method'] == 'GET':
                    md.append('Returns: %s' % fields_string)
                if url['method'] == 'POST' or url['method'] == 'PUT':
                    md.append('Required fields: %s' % fields_string)
                if url['method'] == 'DELETE':
                    md.append('\n\t')
    final_text = '\n'.join(md)
    f = open(path.join(PROJECT_ROOT,filename),'w')
    f.write(final_text)
    f.close()
    return final_text

def convert_to_viewmaps(config):
    """ Accepts a config file, pre-narrowed to user_role.
    Returns a dictionary in which each resource has beeen expanded into a viewmap.
    """
    return {k:vmethods.viewmap_of(v) for k,v in config.items()}

def api_dict(config):
    """Accepts a config file, pre-narrowed to user_role. Returns a dictionary that can be expanded
    into a readable api.
    """
    result = {res:{'meta':meta_for(res),'urls':[]} for res in config.keys() if res is not 'index'}
    viewmaps = convert_to_viewmaps(config)
    for resource, res_config in viewmaps.items():
        prefix = (resource is not 'index') and ("/%s/:id" % resource) or ''   
        traversals = res_config.get('traversals')
        # First of all, the forward links from here. We're going to make an entry for each in
        # the forward resource's 'urls' key.
        if traversals:
            # Each t will be a dictionary such as {'url';'foo','methods':['GET','PUT']}
            for t in traversals:
                # finesse point. We're actually appending these urls to the result for the resource
                # they link to. That is, using the above example, we're appending these urls to
                # result {'foo'['urls']}
                target = t['url']
                for method in t['methods']:
                    url_dict = {'url': '%s/%s' % (prefix, target), 'method': method}
                    target_fields = viewmaps[target]['fields']
                    if method == 'GET':
                        url_dict['fields']=target_fields['read']
                    elif method == 'POST':
                        url_dict['fields']=target_fields['write']
                    result[target]['urls'].append(url_dict)
        methods = res_config.get('methods')
        if methods and resource is not "index":
            available_methods = vmethods.allowed_methods_of(methods)
            for m in available_methods['allowed']:
                url_dict = {'url': '/%s/:id' % resource, 'method': m}
                if m == 'GET':
                    url_dict['fields']=res_config['fields']['read']
                if m == 'PUT':
                    url_dict['fields']=res_config['fields']['write']
                result[resource]['urls'].append(url_dict)
    return result

