## What do the permission modes mean?

Remember: This is not a perfect, one-to-one correspondence with Unix-style permissions. 


### Table-level permissions

#### Overall permissions:

- read: Can get meta-information about the resource. Its url, count, date modified, etc.
- write: Can create, modify, delete files in the directory.
- execute: Gains access to the instance-level methods in the directory. This means getting a meaningful listing of the directory.

#### Methods:

- read: Get a link to this method.
- write: Not used.
- execute: Perform this method.

This might need some explaining. Consider the POST method. With a permission of 5 (r-x), the user will get a link to the POST method for this resource (usually opening a form), and the system accepts the POST. With a permission of 1, the user might take actions which POST a new resource without knowing it. An example would be creating Events or logging.

#### Aggregates:

What can we find out about this table? We may, at some point, set permissions for aggregate properties of a table (or subtable) such as its count.

### Column-level permissions

#### Per attribute:

This generally means per field, but not in every case. Some attributes can be derived from others.

- read: Self-explanatory.
- write: As it says.
- execute: An executable field is a traversal. We use it to get to related resources. 

This last bit says a lot, so let's take a moment.

The user's permissions over a directory are determined by this relationship. There is no bare, unconditioned permission over a resource. Even if we are accessing it on its own we are silently accessing it through the base resource of the index.

If a user has no route that grants read access to that resource, then the resource does not exist to that user. On the other hand, it the user finds one route with read-only access, then that user can read that resource in that context (and no other).

Let us say that the user gains access level 5 to the *bar* resource via *foo*. That will automatically give us these traversals:

foo/:pk/bar GET

If we escalate to level 7, now we have these traversals:

foo/:pk/bar GET
foo/:pk/bar POST

Notice that changing this bit changed nothing whatsoever about:

/bar GET
/bar POST

both of which would be set in the permissions from index.

This is a way of saying that permission to GET or POST to a directory of a resource is not an inherent property of the resource. In fact, the directory of a resource is not an inherent property of the resource.

Do not be fooled, then, when we find permissions to GET a resource set at the level of the resource. That speaks to the user's ability to GET a single instance (or PUT it, or DELETE it).

There's also a strange and counterintuitive -- but powerful -- setting for a directory: --x. This means that we can traverse through the collection *but not see it*. Why does this matter?

This URL is not helpful:

/entries

It gets us every entry in the system. What are they entries for? We don't know because their usual context (a challenge) is removed. But this *is* helpful:

/entries/473

and without the permissions bit set to execute, we couldn't reach this entry to look at it.

Also note that, as permissions are concerned, the nature of the relationship (parent, child, many) is unimportant.

### Instance level:

An instance has no permissions of its own; it takes on the permissions of its class, and its attributes take on the permissions define for them at the class level.

We change the permissions of an instance by changing its ownership or group membership.