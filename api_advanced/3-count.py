#!/usr/bin/python3
""""3-count.py"""
import requests


def count_words(subreddit, word_list, after="", words_count={}):
    """"count words"""
    url = "https://www.reddit.com/r/{}/hot.json?limit=100" \
        .format(subreddit)
    header = {'User-Agent': 'Mozilla/5.0'}
    param = {'after': after}
    response = requests.get(url, headers=header, params=param)

    if response.status_code != 200:
        return

    json_res = response.json()
    after = json_res.get('data').get('after')
    has_next = after is not None
    hot_titles = []
    words = [word.lower() for word in word_list]

    if len(words_count) == 0:
        words_count = {word: 0 for word in words}

    hot_articles = json_res.get('data').get('children')
    [hot_titles.append(article.get('data').get('title'))
     for article in hot_articles]

    # loop through all titles
    for i in range(len(hot_titles)):
        for title_word in hot_titles[i].lower().split():
            for word in words:
                if word.lower() == title_word:
                    words_count[word] = words_count.get(word) + 1

    if has_next:
        return count_words(subreddit, word_list, after, words_count)
    else:

        words_count = dict(filter(lambda item: item[1] != 0,
                                  words_count.items()))

        words_count = sorted(words_count.items(),
                             key=lambda item: item[1],
                             reverse=True)

        for i in range(len(words_count)):
            print("{}: {}".format(words_count[i][0],
                                  words_count[i][1]))
