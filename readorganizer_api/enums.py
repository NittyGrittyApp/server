from django.db import models


class ChannelTypesEnum(models.TextChoices):
    MANUAL = "manual", "Manual"
    FEED = "feed", "RSS/Atom feed"


class EntryContentSourceTypesEnum(models.TextChoices):
    FEED_SUMMARY = "summary", "Feed - summary field"
    FEED_CONTENT = "content", "Feed - content field"
    READABILITY = "readability", "Readability (Python implementation)"
    NODE_READABILITY = "nodereadability", "Readability (Node.js implementation)"


class InternalTasksEnum(models.TextChoices):
    FETCH_FEED_CHANNEL_CONTENT = "readorganizer_api.internal.fetch_feed_channel_content"
