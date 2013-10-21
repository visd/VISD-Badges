# VISD Badges

This project may have two areas of interest to it.

On the developer's side, there's another stab at rapid and secure developement of web apps, in this case within the Django framework.

On the content side, the end result is a system for teachers to use to track their own uses of technology in their teaching. It's a planner, in idea book, and a site for sharing their own progress.

## Rapid development

Because we don't know how teachers might use a site such as this, we want to be able to experiment. To encourage rapid development, there's a Build feature to generate phony instances that are related. We can tear down and rebuild fixtures to our liking with one command.

With a lot of deference to the contrainst of RESTful architecture, the backend conveys everything about application state to the template via hypertext. No decisions about what will appear on each page gets made in teh template design; only how it will appear.

The data and options served up in the hypertext follow from a comprehensive permissions system modeled on the UNIX filesystem. In short, users see what they are allowed to see and can go where they are allowed to go. Although some of these choices can be hidden, the whitelist comes ouf of the combination of permissions defined at the class level and the user's group.

The permissions system will work without the views, but not vice versa.