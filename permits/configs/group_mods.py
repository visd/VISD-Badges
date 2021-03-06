MODS = {'admin': {'inherits': 'visd-staff',
                  'values': {'users': {'fields': {'group': '+w'},
                                       'methods': {'DELETE': '+rx'}}}},
        'visd-staff': {'values': {'skillsets': {'fields': {'title': '+w',
                                                           'short_description': '+w',
                                                           'long_description': '+w',
                                                           'slug': '+rw',
                                                           'challenges': '+w'},
                                                'methods': {'PUT': '+rwx',
                                                            'DELETE': '+rx'}},
                                  'challenges': {
                                      'fields': {
                                          'title': '+w',
                                          'short_description': '+w',
                                          'long_description': '+w',
                                          'slug': '+rw',
                                          'created_at': '+r',
                                          'skillset': '+rw',
                                          'skillset_id': '+rw',
                                          'entries': '+w',
                                          'resources': '+w',
                                          'tags': '+w',
                                          'tools': '+w',
                                          'user_id': '+rw',
                                          'user': '+w',
                                          'group_id': '+rw',
                                          'group': '+rw'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  },
                                  'resources': {
                                      'fields': {
                                          'title': '+w',
                                          'url-link': '+w',
                                          'url-title': '+w',
                                          'description': '+w',
                                          'challenge': '+w',
                                          'thumb': '+w',
                                          'created_at': '+r',
                                          'challenge': '+rw'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  },
                                  'entries': {
                                      'fields': {
                                          'user': '+w',
                                          'title': '+w',
                                          'caption': '+w',
                                          'image': '+w',
                                          'url_link': '+w',
                                          'url_title': '+w',
                                          'created_at': '+r',
                                          'challenge': '+rw'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  },
                                  'tags': {
                                      'fields': {
                                          'word': '+w',
                                          'slug': '+rw',
                                          'created_at': '+r'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  },
                                  'tools': {
                                      'fields': {
                                          'title': '+w',
                                          'slug': '+r',
                                          'url_link': '+w',
                                          'url_title': '+w',
                                          'icon': '+w',
                                          'created_at': '+r'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  },
                                  'users': {
                                      'fields': {
                                          'first_name': '+w',
                                          'last_name': '+w',
                                          'email': '+w',
                                          'username': '+w'
                                      },
                                      'methods': {
                                          'PUT': '+rwx',
                                          'DELETE': '+rx'
                                      }
                                  }
                                  }
                       }
        }
