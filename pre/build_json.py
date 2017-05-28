import urllib2
import json

responses = {}

for intent in ['toprepos','toplanguages','toporgs','topusers','mostactiveusersbylang','launch']:
    responses[intent] = "<speak>Not yet implemented.</speak>"

# Top Repos

# Top Languages

# Top Orgs

# Top Users

# Most Active Users by language
    

responses['launch'] = "<speack>Welcome to Virginia Coders. This skill uses the GitHub API to find the top respos, languages, organizations and users in Virginia. Try it out by asking, what are the top orgs.</speak> "
responses['help'] = "<speak>Use Virginia Coders to check out the top repos, programming languages, organizations and users in Virginia according to GitHub. Try asking for the top programming languages used in Virginia; simply say, what are the top languages.</speak>"
responses['end'] = "<speak>Thanks for checking out V A Coders. Talk to you soon.</speak>"
    
with open('responses/github.json', 'w') as outfile:
    json.dump(responses, outfile)
