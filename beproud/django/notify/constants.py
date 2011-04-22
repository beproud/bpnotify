#:coding=utf8:

"""
NOTIFY_TYPES = (
    ('new_user', 'Welcome!'),
    ('follow', 'User Follow'),
    ('private_msg', 'Private Message'),
    ...
)
"""
"""
NOTIFY_MEDIA = {
    "news": {
        "verbose": "News",
        "backend": "model",
    },
    "private_msg": {
        "verbose": "Private Message",
        "backend": ["model", "mail"],
    },
    ...
}
"""

"""
NOTIFY_MEDIA_DEFAULTS = {
    "new_user": {
        "news": True,
    },
    "follow": {
        "news": True,
    },
    "private_msg": {
        "news": True,
        "private_msg": True,
    },
}
"""
