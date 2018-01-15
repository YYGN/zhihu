# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class ZhihuItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    添加存储字段
    """
    name = Field()
    gender = Field()
    type = Field()
    url_token = Field()
    headline = Field()
    answer_count = Field()
    follower_count = Field()
    articles_count = Field()
    badge = Field()
    locations = Field()
    educations = Field()
    description = Field()
    following_count = Field()
    voteup_count = Field()
    collection_count = Field()
    favorited_count = Field()
    emloyments = Field()
    thanked_count = Field()