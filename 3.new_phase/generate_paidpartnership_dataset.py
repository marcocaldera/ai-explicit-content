import json
import pandas as pd
import string
import urllib.request
from urllib.error import HTTPError
import os

start = pd.Timestamp.now()
# code

if not os.path.exists('dataset/images-2.0'):
    os.makedirs('dataset/images-2.0')


def __clean_caption(comment):
    _hashtag = [word for word in comment.split() if word.startswith('#')]  #  prendo hashtag
    _tag = [word for word in comment.split() if word.startswith('@')]  # prendo tag

    comment = " ".join([word for word in comment.split() if word not in _hashtag])  # rimuovo hashtag
    comment = " ".join([word for word in comment.split() if word not in _tag])  # rimuovo tag
    comment = comment.translate(str.maketrans('', '', string.punctuation))  # rimuovo punteggiatura

    return _hashtag, _tag, comment


# this finds our json files
path_to_json = 'dataset/non-influencer-json-2020'
json_files_name = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#json_files_name = json_files_name[971:]  # riparto da dove mi ero fermato

# Colonne del nuovo dataset che voglio creare
json_df = pd.DataFrame(
    columns=['username', 'photo_id', 'followed_by', 'hashtag', 'tag', 'caption', 'is_video', 'timestamp',  'n_comment',
             'n_likes', 'target'])

# we need both the json and an index number so use enumerate()
for index, js in enumerate(json_files_name):
    with open(os.path.join(path_to_json, js)) as json_file:
        print(js)
        json_text = json.load(json_file)
        main_data_position = json_text['entry_data']['ProfilePage'][0]['graphql']['user']
        username = main_data_position['username']  # nome utente instagram

        if len(main_data_position['edge_owner_to_timeline_media']['edges']) != 0:

            url_first_image = main_data_position['edge_owner_to_timeline_media']['edges'][0]['node']['display_url']
            # df = pd.read_csv("dataset/influencer_dataset.csv", sep=',', encoding="utf-8")
            for i_post, post in enumerate(main_data_position['edge_owner_to_timeline_media']['edges']):

                hashtag, tag, caption = [], [], ''
                if len(post['node']['edge_media_to_caption']['edges']) != 0:  # verifico se è presente un commento
                    caption = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    hashtag, tag, caption = __clean_caption(caption)

                # Se posso, scarico la foto e la salvo sul filesystem
                photo_id = None
                try:
                    urllib.request.urlretrieve(
                        post['node']['display_url'],
                        "dataset/images-2.0/{}.jpg".format(username + str(i_post))
                    )
                    photo_id = username + str(i_post)
                except HTTPError as e:
                    pass

                json_df.loc[i_post] = [
                    username,
                    photo_id,
                    main_data_position['edge_followed_by']['count'],
                    hashtag,
                    tag,
                    caption,
                    post['node']['is_video'],
                    post['node']['taken_at_timestamp'],
                    post['node']['edge_media_to_comment']['count'],
                    post['node']['edge_liked_by']['count'],
                    'standard'
                ]

            json_df.to_csv('dataset/non-influencer_dataset.csv', mode='a', header=False)

        #     break
    # break
        # if index % 30 == 0:
        # print("Salvataggio primi {} elementi".format(index))
        # json_df.to_csv('dataset/influencer_dataset.csv', mode='a', header=False)

# print(json_df)
#json_df.to_csv('dataset/influencer_dataset.csv')

print(pd.Timestamp.now() - start)  # end time
# info 0 days 00:16:18.869679
