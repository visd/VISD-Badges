## Badges API
For users in the `group` role.
Also with extra permissions for the `visd-staff` group.
### Tags
Tags let users mark entries, challenges or other objects with a keyword.

    /tags/:id - PUT

Required fields: word, slug

    /tags/:id - DELETE


    /tags/:id - GET

Returns: word, created_at, slug

    /challenges/:id/tags - POST

Required fields: word, slug

    /challenges/:id/tags - GET

Returns: word, created_at, slug

    /events/:id/tags - GET

Returns: word, created_at, slug
### Challenges
Challenges represent projects or ideas teachers can take on.

    /tags/:id/challenges - GET

Returns: title, created_at, long_description, skillset, short_description

    /challenges/:id - PUT

Required fields: title, long_description, skillset, short_description, slug

    /challenges/:id - DELETE


    /challenges/:id - GET

Returns: title, created_at, long_description, skillset, short_description

    /skillsets/:id/challenges - POST

Required fields: title, long_description, skillset, short_description, slug

    /skillsets/:id/challenges - GET

Returns: title, created_at, long_description, skillset, short_description

    /tools/:id/challenges - GET

Returns: title, created_at, long_description, skillset, short_description
### Skillsets
Skillsets are areas of strength that teachers can build on.

    /skillsets - GET

Returns: title, short_description, slug, long_description

    /tags/:id/skillsets - GET

Returns: title, short_description, slug, long_description

    /skillsets/:id - PUT

Required fields: title, short_description, slug, long_description

    /skillsets/:id - DELETE


    /skillsets/:id - GET

Returns: title, short_description, slug, long_description

    /tools/:id/skillsets - GET

Returns: title, short_description, slug, long_description
### Entries
A way to submit an example of your work. Entries show you have completed a challenge.

    /challenges/:id/entries - POST

Required fields: title, challenge, url_link, caption, user, image, url_title

    /challenges/:id/entries - GET

Returns: created_at, title, challenge, url_link, caption, user, image, url_title

    /entries/:id - PUT

Required fields: title, challenge, url_link, caption, user, image, url_title

    /entries/:id - DELETE


    /entries/:id - GET

Returns: created_at, title, challenge, url_link, caption, user, image, url_title

    /resources/:id/entries - POST

Required fields: title, challenge, url_link, caption, user, image, url_title

    /resources/:id/entries - GET

Returns: created_at, title, challenge, url_link, caption, user, image, url_title
### Tools
Cameras, software, devices -- anything a teacher uses in an entry.

    /tools - GET

Returns: title, created_at, url_link, slug, url_title, icon

    /challenges/:id/tools - POST

Required fields: title, url_link, url_title, icon

    /challenges/:id/tools - GET

Returns: title, created_at, url_link, slug, url_title, icon

    /tools/:id - PUT

Required fields: title, url_link, url_title, icon

    /tools/:id - DELETE


    /tools/:id - GET

Returns: title, created_at, url_link, slug, url_title, icon
### Events
Events mark what is happening in the system. The user sees what is happening in his/her group, or system-wide.

    /events - GET

Returns: user
### Resources
More information about a challenge, usually as a link to a website.

    /tags/:id/resources - GET

Returns: description, title, challenge, thumb, url-link, created_at, url-title

    /challenges/:id/resources - POST

Required fields: description, title, challenge, thumb, url-link, url-title

    /challenges/:id/resources - GET

Returns: description, title, challenge, thumb, url-link, created_at, url-title

    /tools/:id/resources - GET

Returns: description, title, challenge, thumb, url-link, created_at, url-title

    /resources/:id - PUT

Required fields: description, title, challenge, thumb, url-link, url-title

    /resources/:id - DELETE


    /resources/:id - GET

Returns: description, title, challenge, thumb, url-link, created_at, url-title