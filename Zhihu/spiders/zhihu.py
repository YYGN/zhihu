# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from scrapy import Spider, Request
from Zhihu.items import ZhihuItem



class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 定义起始的知乎大V的url-token
    start_user = 'liangbianyao'
    # 起始的用户详细信息页面
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # include内容，直接从浏览器中抓取
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    # 粉丝人数页面
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    follows_query ='allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 关注的人数页面
    following_url ='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    following_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        """
        重定义起始的请求
        """
        # 发起用户详情请求
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        # 发起粉丝人数请求
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20), callback=self.parse_follower)
        # 发起关注的人数请求
        yield Request(self.following_url.format(user=self.start_user, include=self.following_query, offset=0, limit=20), callback=self.parse_following)

    def parse_user(self, response):
        """
        解析用户详情页面
        """
        items = ZhihuItem()
        user_info = json.loads(response.text)
        if user_info:
            # 遍历items中的Field
            for field in items.fields:
                if field in user_info.keys():
                    items[field] = user_info.get(field)
            yield items
            # 从用户详情页抓取到关注者和关注的页面并发起请求
            yield Request(self.follows_url.format(user=user_info.get('url-token'), include=self.follows_query, offset=0, limit=20), callback=self.parse_follower)
            yield Request(self.following_url.format(user=user_info.get('url-token'), include=self.following_query, offset=0, limit=20), callback=self.parse_following)

    def parse_follower(self, response):
        """
        解析粉丝列表
        """
        follower_list = json.loads(response.text)
        if follower_list:
            if 'data' in follower_list.keys():
                for follower in follower_list.get('data'):
                    # 加上时间限制，避免被网站ban
                    time.sleep(3)
                    yield Request(self.user_url.format(user=follower.get('url_token'), include=self.user_query), callback=self.parse_user)

            # 翻页
            if 'paging' in follower_list.keys():
                if follower_list.get('paging').get('is_end') == False:
                    next_url = follower_list.get('paging').get('next')
                    time.sleep(1)
                    yield Request(next_url, self.parse_follower)

    def parse_following(self, response):
        """
        解析关注列表
        """
        following_list = json.loads(response.text)
        if following_list:
            if 'data' in following_list.keys():
                for following in following_list.get('data'):
                    time.sleep(3)
                    yield Request(self.user_url.format(user=following.get('url_token'), include=self.user_query), callback=self.parse_user)

            if 'paging' in following_list.keys():
                if following_list.get('paging').get('is_end') == False:
                    next_url = following_list.get('paging').get('next')
                    time.sleep(1)
                    yield Request(next_url, self.parse_following)
