import requests 
import base64
import json
import os
import csv


# Load keys
client_key = 'XXXX'
client_secret = 'XXXX'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')


# Post request to auth endpoint to obtain Bearer Token
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = auth_resp.json()['access_token']


# Make queries
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

search_params = {
    'query': 'Tesla',
    'fromDate': '202004010000',
    'toDate': '202005010000',
    'bucket': 'day'
}

search_url = '{}1.1/tweets/search/fullarchive/full/counts.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_params)
tweet_data = search_resp.json()

#print(json.dumps(tweet_data, indent = 4))


# Save results to json file
path = os.path.join(os.path.dirname(__file__),'twitter_request_tsla.json')
with open(path, 'a') as g:
	json.dump(tweet_data,g, indent=4)


# Extract only relevant items for CSV
relevant_data = []

for x in tweet_data['results']:
    relevant_data.append({'time_period':x['timePeriod'], 'count':x['count']})

path = os.path.join(os.path.dirname(__file__),'twitter_request_tsla.json')
with open(path, 'w') as g:
	json.dump(tweet_data,g, indent=4)


# Save relevant_data list to CSV
path_csv = os.path.join(os.path.dirname(__file__),'twitter_request_tsla.csv')
twitter_request = open(path_csv, 'w')
csv_writer = csv.writer(twitter_request)

count = 0
for i in relevant_data:
    if count == 0:
        header = i.keys()
        csv_writer.writerow(header)
        count +=1

    csv_writer.writerow(i.values())

twitter_request.close()

