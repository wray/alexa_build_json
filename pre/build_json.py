import urllib2
import json

responses = {}

for intent in ['toprepos','toplanguages','toporgs','topusers','mostactiveusersbylang','launch','help','end']:
    responses[intent] = "<speak>Not yet implemented.</speak>"

with open('responses/github.json', 'w') as outfile:
    json.dump(responses, outfile)
