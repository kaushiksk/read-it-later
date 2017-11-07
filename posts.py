#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : posts.py
# Author            : Kaushik S Kalmady
# Date              : 07.11.2017
# Last Modified Date: 07.11.2017
# Last Modified By  : Kaushik S Kalmady

from newspaper import Article
# from wordcloud import WordCloud

# keyword_freq = {}

def extract_article(story_url):
    """extract_article

    :param story_url: URL to the article to be parsed
    """
    #
    article = Article(story_url)
    # if not article.is_valid_url():
    #     return "Error"

    article.download()
    article.parse()
    #article.nlp()

    title = article.title
    img = article.top_image
    publish_date = article.publish_date
    text = article.text.split('\n\n')[1] + " " +  article.text.split('\n\n')[2] if article.text else ""

	# for keyword in article.keywords:
	# 	keyword_freq[keyword] = keyword_freq.get(keyword,0) + 1

    return {
        'title':title,
        'img':img,
        'publish_date':publish_date,
        'text':text.encode('ascii','ignore'),
    }

# def gen_worldcloud():

# 	wordcloud = WordCloud().generate_from_frequencies(keyword_freq)
# 	image = wordcloud.to_image()
# 	image.save("wodcloud.png")


