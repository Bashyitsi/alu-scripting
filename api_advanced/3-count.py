#!/usr/bin/python3

import requests


def count_words(subreddit, word_list, after='', hot_list=None):
    if hot_list is None:
        hot_list = [0] * len(word_list)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "My User Agent 1.0"}
    params = {'after': after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()

        for topic in data['data']['children']:
            title_words = topic['data']['title'].split()
            for i, word in enumerate(word_list):
                for title_word in title_words:
                    if title_word.lower() == word.lower():
                        hot_list[i] += 1

        after = data['data']['after']
        if after is not None:
            return count_words(subreddit, word_list, after, hot_list)

    results = []
    save = []
    for i in range(len(word_list)):
        for j in range(i + 1, len(word_list)):
            if word_list[i].lower() == word_list[j].lower():
                save.append(j)
                hot_list[i] += hot_list[j]

    for i in range(len(word_list)):
        for j in range(i, len(word_list)):
            if (hot_list[j] > hot_list[i] or
                    (word_list[i] > word_list[j] and hot_list[j] == hot_list[i])):
                hot_list[i], hot_list[j] = hot_list[j], hot_list[i]
                word_list[i], word_list[j] = word_list[j], word_list[i]

        if hot_list[i] > 0 and i not in save:
            results.append("{}: {}".format(word_list[i].lower(), hot_list[i]))

    return results


# Example usage
subreddit = "unpopular"
word_list = ['you', 'unpopular', 'vote', 'down', 'downvote', 'her', 'politics']
results = count_words(subreddit, word_list)

# Print the sorted count of keywords
for result in results:
    print(result)
