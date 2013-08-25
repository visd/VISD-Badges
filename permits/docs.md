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

Incidentally, traversals are *only figured for children*. There is no such thing as blocking traversal to a parent! If it's in the URL, by definition you can traverse to it. So we also offer access to the parent resource (that is, resource+id), if there is one. (Read below about The Invisible Index for more on this point.)

### Instance level:

An instance has no permissions of its own; it takes on the permissions of its class, and its attributes take on the permissions define for them at the class level.

We change the permissions of an instance by changing its ownership or group membership.

### Cheat sheet

For fields:

- 7: Instances: read and write, Listing: GET and POST
- 6: Instances: read and write
- 5: Instances: read, Listing: GET
- 4: Instances: read
- 3: Instances: write, Listing: POST (perhaps invisible posting, as for logging or events)
- 2: Instances: write
- 1: Listing: GET (only metadata about a collection)

For methods:

- 7: Can get a form, modify the field values, execute the method
- 6: Can get a form, modify the field values, but not do anything
- 5: Can get a form, read-only field values, execute the method
- 4: Can get a form, read-only field values, but not do anything
- 3: Gets no form, modify the field values, execute the method
- 2: Gets no form, modify the field values, but not do anything
- 1: Gets no form, read-only field values, execute the method.

Let's use some examples per method:

GET:

- 5: User sees a link to GET this and can follow that link.
- 1: User doesn't get a link to this, but can GET it anyway.

In this way, whether an instance is read-only for a particular user is: permission&1
Whether we can get a link to that instance is: permission&4

In the case of GET, the write bit is of undetermined use.

PUT:

- 7: User sees a link to modify this instance, get form with editable fields (based on +/-w per field), and can submit the form.
- 5: User sees a button to PUT this resource somewhere predetermined (e.g., 'add to my favorites')
- 1: Some action the user takes silently PUTs this resource somewhere. Also the user could do a manual PUT without the link.

DELETE:

- 4: User gets a button to delete this thing.
- 1: An invisible delete, again permissible from carefully constructed http calls. Beware. But we may need this sort of call to be triggered silently.

Just as in POSIX, we may have to extend the bit system so we have special setuid or setgid bits. Not if we can help it, though. 

## Sites, or the invisible index

In visible terms, there is a difference between a URL like:

/entries

and one like:

/challenges/46/entries

The first is not scoped, and the second is. But this needs to be an illusion. Why?

We're using permissions to configure which traversals are possible from which scope. But we can't do this if the scope does not exist. So we make an invisible one, 'index'. Now we can define which resources we can traverse to directly from the index.

Actually, we need to be careful. Because we *can* go to:

/challenges/46

but not to:

/challenges

So from the scope of index, we use the permisson 4 (r--), which lets us access what's in the directory but not list it directly. Of course if we want to be able to write to files we can +w.



