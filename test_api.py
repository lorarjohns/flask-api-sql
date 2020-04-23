from pprint import pprint
import requests
import json

url= "http://0.0.0.0:5000/"

print('testing healthcheck endpoint...')
r = requests.get(url + 'healthcheck')

if r.status_code != 200:
  print("Error:", r.status_code)

print(r.json())
print('done with healthcheck check!')

print('\n\n')

print('testing stats/section endpoint...')
print('testing user_id for "u:0eccf48d721e" and "u:e6f4cc3ba334"')
print('\n')
user_ids = ["u:0eccf48d721e", "u:e6f4cc3ba334"]
for id in user_ids:
  r = requests.get(url + 'stats/section', json={"user_id": id})

  if r.status_code != 200:
    print("Error:", r.status_code)
  print(f'Output for {id}:')
  pprint(r.json())
print('done with stats/section check!')

print('\n\n')

print('testing rank/section endpoint...')
print('testing on user_id "u:0eccf48d721e" and')
print('''content_ids: "c2806f15-9b98-4bbc-b66a-13d131f63aac",
              "9728ca66-54a3-4229-adf2-70dbbfed5049",
              "675da7be-ac22-49f1-b4ba-b967abdd819e",
              "ed8d04f8-d103-4c02-ab35-55902fdf9f6d",
              "af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b",
              "1bce63f2-f3c4-4f9e-9491-45d1c4aaec02",
              "9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30"''')
print('\n')
r = requests.post(url + "rank/section", json={
"user_id": "u:0eccf48d721e", 
"content_ids": 

        ["c2806f15-9b98-4bbc-b66a-13d131f63aac",
        "9728ca66-54a3-4229-adf2-70dbbfed5049",
        "675da7be-ac22-49f1-b4ba-b967abdd819e",
        "ed8d04f8-d103-4c02-ab35-55902fdf9f6d",
        "af56c5dd-fddc-4fe5-b0b7-2b74d951ec0b",
        "1bce63f2-f3c4-4f9e-9491-45d1c4aaec02",
        "9a1f8fb9-19ec-4451-aee8-d3a0e9dcfb30"]
}, headers={'Content-Type':'application/json'}
)
print('Output:')
pprint(r.json())
print('done with rank/section check!')
