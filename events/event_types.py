EVENT_TYPES = {

    "entry-submitted" : {
        "description" : "An admin okayed a challenge. The crucial object is an entry.",
        "object" : "entries",
        "eventstring" : "<a href='{{user.url}}'>{{user.fullname}}</a> <a href='{{object.url}}'>completed</a> the challenge: <a href='{{challenge.url}}'>{{challenge.title}}</a>.",
        "tags" : ["entry-approved","acheivement"],
        "level" : "user"
    },
    # "new-user" : {
    #     "description" : "A new user joins the system.",
    #     "object" : "profile",
    #     "eventstring" : "<a href='{{object.url}}'>{{user.fullname}}</a> joined the system.",
    #     "tags" : ["system","new-user"],
    #     "level" : "user"
    # },
    "new-challenge" : {
        "description": "A new challenge in the system.",
        "object" : "challenges",
        "eventstring" : "A new challenge in <a href='{{object.skillset.url}}'>{{object.skillset.title}}</a>: <a href='{{object.url}}'>{{object.title}}</a>!",
        "tags" : ["system","add","newchallenge"],
        "level" : "guest"
    },
    "new-skillset" :{
        "description": "A new skillset in the system.",
        "object": "skillsets",
        "eventstring" : "A new skillset to master: <a href='{{object.url}}'>{{object.title}}</a>",
        "tags" : ["system","new-skillset"],
        "level" : "guest"
    },
    "test-template" : {
        "description" : "Used for testing.",
        "object" : "challenges",
        "eventstring" : "{{user}} completed the challenge: {{object.title}}.",
        "tags" : ["test-template"],
        "level" : "public"
    }

}