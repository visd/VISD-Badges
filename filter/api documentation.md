### Filter API

The YAML files in this folder, taken together, describe the resources in our system. They work together to create different versions of the API for users in different groups.

This is experimental. I don't know of a model like this, even one that emits different representations for different types of user. So until I testify that this works, ignore it while I chip away at it.

The `api_core.yaml` catalogs every resource available in its fullest form, along with every possible traversal. It's a whitelist.

The other APIs subtract resources at different levels of granularity.

The work of compiler is to merge the files into native Python objects, one for each API version. They'll need to load fast and stay in memory, because the idea is that every request and response filters through them. So we compile by hand, then pickle the objects and teach Django to hold them in memcache.