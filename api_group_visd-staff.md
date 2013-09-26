## Badges API
For users in the `group` role.
Also with extra permissions for the `visd-staff` group.
### Challenges
Challenges represent projects or ideas teachers can take on.

    /tags/:id/challenges - GET

Returns: title, created_at, short_description, long_description

    /skillsets/:id/challenges - POST

Required fields: group, title, slug, skillset_id, short_description, user_id, group_id, long_description

    /skillsets/:id/challenges - GET

Returns: title, created_at, short_description, long_description

    /challenges/:id - PUT

Required fields: group, title, slug, skillset_id, short_description, user_id, group_id, long_description

    /challenges/:id - GET

Returns: title, created_at, short_description, long_description

    /challenges/:id - DELETE
  

    /tools/:id/challenges - GET

Returns: title, created_at, short_description, long_description
### Users
A user in the system. You must be logged in to show up as a user.

    /index/:id/users - GET

Returns: first_name, last_name, email

    /users/:id - PUT

Required fields: first_name, last_name, email

    /users/:id - GET

Returns: first_name, last_name, email

    /users/:id - DELETE

### Tags
Tags let users mark entries, challenges or other objects with a keyword.

    /tags/:id - PUT

Required fields: word, slug

    /tags/:id - GET

Returns: word, created_at, slug

    /tags/:id - DELETE


    /challenges/:id/tags - POST

Required fields: word, slug

    /challenges/:id/tags - GET

Returns: word, created_at, slug

    /events/:id/tags - GET

Returns: word, created_at, slug
### Memberships
Groups gain different kinds of access to objects that belong to their group.

    /users/:id/memberships - GET

### Skillsets
Skillsets are areas of strength that teachers can build on.

    /index/:id/skillsets - GET

Returns: title, slug, short_description, long_description

    /tags/:id/skillsets - GET

Returns: title, slug, short_description, long_description

    /skillsets/:id - PUT

Required fields: title, slug, short_description, long_description

    /skillsets/:id - GET

Returns: title, slug, short_description, long_description

    /skillsets/:id - DELETE

### Entries
A way to submit an example of your work. Entries show you have completed a challenge.

    /users/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, image

    /tags/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, image

    /entries/:id - PUT

Required fields: title, url_link, url_title, caption, image

    /entries/:id - GET

Returns: title, created_at, url_link, url_title, caption, image

    /entries/:id - DELETE


    /challenges/:id/entries - POST

Required fields: title, url_link, url_title, caption, image

    /challenges/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, image

    /tools/:id/entries - GET

Returns: title, created_at, url_link, url_title, caption, image
### Tools
Cameras, software, devices -- anything a teacher uses in an entry.

    /index/:id/tools - GET

Returns: title, created_at, url_link, url_title, slug, icon

    /challenges/:id/tools - POST

Required fields: title, url_link, url_title, icon

    /challenges/:id/tools - GET

Returns: title, created_at, url_link, url_title, slug, icon

    /tools/:id - PUT

Required fields: title, url_link, url_title, icon

    /tools/:id - GET

Returns: title, created_at, url_link, url_title, slug, icon

    /tools/:id - DELETE

### Events
Events mark what is happening in the system. The user sees what is happening in his/her group, or system-wide.

    /index/:id/events - GET

Returns: user
### Resources
More information about a challenge, usually as a link to a website.

    /challenges/:id/resources - POST

Required fields: thumb, title, challenge, description

    /challenges/:id/resources - GET

Returns: thumb, title, created_at, url_link, url_title, challenge, description

    /resources/:id - PUT

Required fields: thumb, title, challenge, description

    /resources/:id - GET

Returns: thumb, title, created_at, url_link, url_title, challenge, description

    /resources/:id - DELETE
