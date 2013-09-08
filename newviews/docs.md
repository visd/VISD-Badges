### The context

The first principle: The context will supply the template with everything it needs to know.

The template does not touch the database. The template doesn't perform any real logic besides
testing if something exists or looping over a iterator.

The context for an *instance* gives the templating engine everything it needs to build an
instance on the page. Think of a single panel on the screen, with controls and text and images.
This is all in the scope of the instance.

The scope of the *collection* should include the controls to GET, or POST to, the collection;
the url and methods on the parent context (if any), and meta-information (at first version,
just the count).

#### Instance:

- 'meta':
    - 'url': *String. The URL of this instance.*
    - 'methods': *A list of methods available to perform on this instance.*
    - 'tagged_with': *Likely to be helpful in, say, CSS markup. Any tag can go in here.*
    - 'resource': *A necessary redundancy. The name of the type of resource. In some special occasions (such as showing a parent resource) we will get the resource without the collection.*
- 'fields':
    - key: value -- *The fields in the instance.*
    - By the time fields reach the template, they can be nested for calls to the parent. So, for instance, an entry can have:
        `{'challenge':{'title':'blah', 'url':'/challenge/13', 'skillset':{'title':'blah', 'url':'/skillsets/56'}}}`
    Here we have our one case in which we count on the templating engine to figure out what to do with a url. But this is acceptable, in this case, because we know it will only ever be a GET, and by definition it is permissible.
-  'relations':
    - A dictionary containing, in turn a dictionary for every related resource. This will have, at bare minimum, a 'meta' entry with a url and available methods for that URL. If there's more nesting to do, the collection for that relation is nested in here (see below).

#### Collection:
    
- 'meta':
    - 'resource': *The name of the resource.*
    - 'url': *String. The URL of this collection.*
    - 'methods': [] *A list of methods available to this collection ('GET' or 'POST')*
    - 'count': # *The number of instances in this collection.
- 'traversals':
    - [{'url': url, 'method': 'GET'}] *for the parent id, if it exists. No parent collection because we don't know if that collection is directly traversable as-is.
- resource: [instances] *If we are recursing. A depthless retrieval skips this step.

### Parents

Instances and collections find their own parents in different ways.

A property on each model defines its parent instance. Another property defines the parent_model of this model. (This is unrelated to class inheritance.) So the parent instance of /entries/43 might be /challenges/110. The parent_model of entries is challenges; it's inherent to the structure. So the URL doesn't have to maintain this information. This lets us say that, for instance, whenever we show of an entry we want to include what challenge it's an entry for.

Collections, on the other hand, show how we scoped them in this request. Consider:

/tags/:id/challenges

and

/skillsets/:id/challenges

We're looking at a bunch of challenges. What bunch? To know which bunch, we have to look in the request. If we walk back up, we can find siblings or cousins. For instance, "also tagged with..." or "events in this skillset."