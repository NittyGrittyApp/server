from dataclasses import asdict
from sys import maxsize as time_always_update
from typing import Iterable

from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models.query import QuerySet
from django.utils.timezone import now as django_now

from .enums import ChannelTypesEnum
from .enums import InternalTasksEnum
from .exceptions import NoNewChannelsAddedException
from .types import AsyncTaskResult
from .types import ChannelDataInput
from .utils import dispatch_task_by_name


class ChannelManager(models.Manager):
    def add_channels(
        self, channels_list: Iterable[ChannelDataInput], fetch_content: bool = True
    ) -> tuple[tuple[int, ...], tuple[AsyncTaskResult, ...]]:
        queryset = self.get_queryset()

        all_urls = [channel.url for channel in channels_list]
        existing_urls = queryset.filter(url__in=all_urls).values_list("url", flat=True)
        new_urls = set(all_urls) - set(existing_urls)

        if not new_urls:
            raise NoNewChannelsAddedException()

        channels_to_insert = [
            self.model(**asdict(channel_data))
            for channel_data in channels_list
            if channel_data.url in new_urls
        ]

        inserted_channels = queryset.bulk_create(channels_to_insert)

        if not inserted_channels[0].id:
            inserted_channels = queryset.filter(url__in=new_urls)

        fetch_content_tasks = []
        if fetch_content:
            fetch_content_tasks = self.fetch_channels_content(inserted_channels)

        inserted_channels_ids = [channel.id for channel in inserted_channels]

        return (inserted_channels_ids, fetch_content_tasks)

    def fetch_channels_content(
        self, channels: QuerySet, force_fetch: bool = False
    ) -> tuple[AsyncTaskResult, ...]:
        active_channels = channels.filter(active=True).order_by("pk")

        feed_channels = active_channels.filter(channel_type=ChannelTypesEnum.FEED)

        feed_channels_paged = Paginator(
            feed_channels, settings.READORGANIZER_CHANNELS_CHUNK_SIZE
        )

        fetch_feeds_tasks = []
        for chunk_number in feed_channels_paged.page_range:
            task = self._request_feed_channels_content_fetch(
                feed_channels_paged.get_page(chunk_number), force_fetch
            )
            fetch_feeds_tasks.append(task)

        return fetch_feeds_tasks

    def _request_feed_channels_content_fetch(
        self, channels: QuerySet, force_fetch: bool
    ) -> AsyncTaskResult:
        channel_ids = [channel.id for channel in channels if channel.id]
        task = dispatch_task_by_name(
            InternalTasksEnum.FETCH_FEED_CHANNEL_CONTENT,
            kwargs={"channel_ids": channel_ids, "force_fetch": force_fetch},
        )
        return task

    def __discard_channels_updated_recently(self, queryset: QuerySet):
        now = django_now()
        channels = []
        for channel in queryset:
            try:
                time_since_last_update = (now - channel.last_checked).total_seconds()
            except TypeError:
                time_since_last_update = time_always_update

            if time_since_last_update > channel.update_frequency:
                channels.append(channel)
        return channels

    def _fetch_feed_channels_content(
        self, channel_ids: Iterable[int], force_fetch: bool
    ):  # return ids of entries that were fetched?
        queryset = self.get_queryset().filter(pk__in=channel_ids)

        if not force_fetch:
            requested_feeds = self.__discard_channels_updated_recently(queryset)
            requested_feed_urls = [feed.url for feed in requested_feeds]
        else:
            requested_feed_urls = queryset.values_list("url", flat=True)
            requested_feed_urls = list(requested_feed_urls)

        # pass feed urls to dedicated fetcher
