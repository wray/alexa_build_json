import urllib2
import json

responses = {}

for intent in ['toprepos','toplanguages','toporgs','topusers','topusersbylang','launch']:
    responses[intent] = "<speak>Not yet implemented.</speak>"

# { repo_name : ( isOrg, owner_name, lang ), ... }
# [ (repo_name, star_fork_cnt), ... ]
    
# Top Repos
# repos stars + forks
# ordered list

# Top Languages
# repos stars + forks, unique by lang
# 

# Top Orgs
# repos star + fork by org

# Top Users
# repos star + fork by user

# Top Users by language
# repos star + fork by lang
    

responses['launch'] = "<speack>Welcome to Virginia Coders. This skill uses the GitHub API to find the top repos, languages, organizations and users in Virginia. Try it out by asking, what are the top orgs.</speak> "
responses['help'] = "<speak>Use Virginia Coders to check out the top repos, programming languages, organizations and users in Virginia according to GitHub. Try asking for the top programming languages used in Virginia; simply say, what are the top languages.</speak>"
responses['end'] = "<speak>Thanks for checking out V A Coders. Talk to you soon.</speak>"
    
with open('responses/github.json', 'w') as outfile:
    json.dump(responses, outfile)
