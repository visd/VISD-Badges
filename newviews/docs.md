### The context

The first principle: The context will supply the template with everything it needs to know.

The template does not touch the database. The template doesn't perform any real logic besides
testing if something exists or looping over a iterator.

The context for an *instance* gives the templating engine everything it needs to build an
instance on the page. Think of a single panel on the screen, with controls and text and images.
This is all in the scope of the instance.

The scope of the collection should include the controls to GET, or POST to, the collection;
the url and methods on the parent context (if any), and meta-information (at first version,
just the count).

#### Instance:

- meta:
    - 'url': *String. The URL of this instance.*
    - 'methods': *A list of methods available to perform on this instance.*
- fields:
    - key: value -- *The fields in the instance.*
- traversals:
    - [{url: *String. The url of this traversal.*
          - 'methods': [] *A list of available methods on this url. ('GET','PUT','DELETE')*
          - 'preload': {'meta': {'url':' ', 'methods':[], 'count': #}}
            *The nested results of the collection returned from a GET on this url.*
    - }]

#### Collection:
    
- meta:
    - url: *String. The URL of this collection.*
    - methods: [] *A list of methods available to this collection ('GET' or 'POST')*
    - count: # *The number of instances in this collection.
