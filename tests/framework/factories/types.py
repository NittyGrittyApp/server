from dataclasses import dataclass
from typing import Mapping

import factory.fuzzy
from django.utils.timezone import now

from kustosz import types as ro_types
from kustosz.constants import DEFAULT_UPDATE_FREQUENCY
from kustosz.enums import ChannelTypesEnum
from kustosz.enums import EntryContentSourceTypesEnum


@dataclass(frozen=True)
class FakeRequestType:
    url: str
    headers: Mapping[str, str]
    text: str


class ChannelDataInputFactory(factory.Factory):
    class Meta:
        model = ro_types.ChannelDataInput

    url = factory.Faker("uri")
    channel_type = ChannelTypesEnum.FEED
    title = factory.Faker("text")
    active = True
    update_frequency = DEFAULT_UPDATE_FREQUENCY
    tags = factory.Faker("words", unique=True)


class FakeRequestFactory(factory.Factory):
    class Meta:
        model = FakeRequestType

    url = factory.Faker("uri")
    headers = factory.LazyFunction(lambda: {})
    text = ""


class FetchedFeedEntryContentFactory(factory.Factory):
    class Meta:
        model = ro_types.FetchedFeedEntryContent

    source = factory.fuzzy.FuzzyChoice(EntryContentSourceTypesEnum.values)
    content = factory.Faker("text")
    mimetype = factory.Faker("mime_type", category="text")
    language = factory.Faker("locale")


class FetchedFeedEntryFactory(factory.Factory):
    class Meta:
        model = ro_types.FetchedFeedEntry

    feed_url = factory.Faker("uri")
    gid = factory.Faker("uri")
    link = factory.Faker("uri")
    title = factory.Faker("text")
    author = factory.Faker("name")
    published_time = factory.LazyFunction(now)
    updated_time = factory.LazyFunction(now)
    content = factory.List([FetchedFeedEntryContentFactory()])


class FetchedFeedFactory(factory.Factory):
    class Meta:
        model = ro_types.FetchedFeed

    url = factory.Faker("uri")
    fetch_failed = False
    title = factory.Faker("text")
    link = factory.Faker("uri")


class ReadabilityContentListFactory(factory.Factory):
    class Meta:
        model = ro_types.ReadabilityContentList

    content = factory.List([FetchedFeedEntryContentFactory()])


class SingleEntryExtractedMetadataFactory(factory.Factory):
    class Meta:
        model = ro_types.SingleEntryExtractedMetadata

    title = factory.Faker("text")
    author = factory.Faker("name")
    published_time_upstream = factory.LazyFunction(now)
    updated_time_upstream = factory.LazyFunction(now)
