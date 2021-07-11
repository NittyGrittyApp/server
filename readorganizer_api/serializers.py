from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer
from taggit_serializer.serializers import TagListSerializerField

from .models import Channel
from .models import Entry
from .models import EntryContent


class EntryContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryContent
        fields = ["source", "content", "mimetype", "language", "updated_time"]


class ListEntrySerializer(serializers.ModelSerializer):
    published_time = serializers.DateTimeField()

    class Meta:
        model = Entry
        fields = [
            "id",
            "channel",
            "gid",
            "archived",
            "link",
            "title",
            "author",
            "added_time",
            "updated_time",
            "published_time_upstream",
            "updated_time_upstream",
            "published_time",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class EntrySerializer(TaggitSerializer, serializers.ModelSerializer):
    published_time = serializers.DateTimeField()
    contents = EntryContentSerializer(source="content_set", required=False, many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Entry
        fields = [
            "id",
            "channel",
            "gid",
            "archived",
            "link",
            "title",
            "author",
            "added_time",
            "updated_time",
            "published_time_upstream",
            "updated_time_upstream",
            "published_time",
            "contents",
            "tags",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "channel": {"read_only": True},
            "gid": {"read_only": True},
            "link": {"read_only": True},
            "title": {"read_only": True},
            "author": {"read_only": True},
            "added_time": {"read_only": True},
            "updated_time": {"read_only": True},
            "published_time_upstream": {"read_only": True},
            "updated_time_upstream": {"read_only": True},
            "published_time": {"read_only": True},
        }


class ChannelSerializer(TaggitSerializer, serializers.ModelSerializer):
    unarchived_entries = serializers.IntegerField()
    tags = TagListSerializerField()

    class Meta:
        model = Channel
        fields = [
            "id",
            "url",
            "title",
            "active",
            "update_frequency",
            "title_upstream",
            "displayed_title",
            "link",
            "last_check_time",
            "last_successful_check_time",
            "added_time",
            "is_stale",
            "unarchived_entries",
            "tags",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "title_upstream": {"read_only": True},
            "displayed_title": {"read_only": True},
            "link": {"read_only": True},
            "last_check_time": {"read_only": True},
            "last_successful_check_time": {"read_only": True},
            "added": {"read_only": True},
            "is_stale": {"read_only": True},
            "unarchived_entries": {"read_only": True},
        }


class ChannelDetailSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)
    unarchived_entries = serializers.IntegerField()

    class Meta:
        model = Channel
        fields = [
            "id",
            "url",
            "title",
            "title_upstream",
            "displayed_title",
            "link",
            "last_check_time",
            "last_successful_check_time",
            "added_time",
            "active",
            "update_frequency",
            "is_stale",
            "entries",
            "unarchived_entries",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "title_upstream": {"read_only": True},
            "displayed_title": {"read_only": True},
            "link": {"read_only": True},
            "last_check_time": {"read_only": True},
            "last_successful_check_time": {"read_only": True},
            "added": {"read_only": True},
            "is_stale": {"read_only": True},
            "unarchived_entries": {"read_only": True},
        }
