import os

path_to_json = 'dataset/influencer-json-2020'
json_files_name = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for i in range(len(json_files_name)):
    if json_files_name[i] == "marimaria.json":
        print(i)
# print(json_files_name[331:])

# nba_youngboy no post
# apasnayaryka private