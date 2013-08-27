## Badges API
For users in the `group` role.
### Tags
Tags let users mark entries, challenges or other objects with a keyword.

    /tags/:id - GET

Returns: word

    /challenges/:id/tags - GET

Returns: word

    /events/:id/tags - GET

Returns: word
### Challenges
Challenges represent projects or ideas teachers can take on.

    /tags/:id/challenges - GET

Returns: title, short_description, long_description

    /challenges/:id - GET

Returns: title, short_description, long_description

    /skillsets/:id/challenges - GET

Returns: title, short_description, long_description

    /tools/:id/challenges - GET

Returns: title, short_description, long_description
### Skillsets
Skillsets are areas of strength that teachers can build on.

    /skillsets - GET

Returns: title, short_description, long_description

    /tags/:id/skillsets - GET

Returns: title, short_description, long_description

    /skillsets/:id - GET

Returns: title, short_description, long_description

    /tools/:id/skillsets - GET

Returns: title, short_description, long_description
### Entries
A way to submit an example of your work. Entries show you have completed a challenge.

    /challenges/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, user, image

    /entries/:id - GET

Returns: title, created_at, url_link, url_title, caption, user, image

    /resources/:id/entries - POST


    /resources/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, user, image
### Tools
Cameras, software, devices -- anything a teacher uses in an entry.

    /tools - GET

Returns: title, url_link, url_title, icon

    /challenges/:id/tools - GET

Returns: title, url_link, url_title, icon

    /tools/:id - GET

Returns: title, url_link, url_title, icon
### Events
Events mark what is happening in the system. The user sees what is happening in his/her group, or system-wide.

    /events - GET

Returns: user
### Resources
More information about a challenge, usually as a link to a website.

    /tags/:id/resources - GET

Returns: description, title, url-link, url-title, thumb

    /challenges/:id/resources - GET

Returns: description, title, url-link, url-title, thumb

    /tools/:id/resources - GET

Returns: description, title, url-link, url-title, thumb

    /resources/:id - GET

Returns: description, title, url-link, url-title, thumb