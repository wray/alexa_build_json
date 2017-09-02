import json

responses = {}

for intent in ['yourfirstintent','yoursecondintent']:
    responses[intent] = "<speak>Not yet implemented.</speak>"

#
# Put your custom code here. Call your APIs, scrape a website, ingest an RSS Feed, use your database.
# Arrange your data to match the JSON convention:
# responses = { 'yourfirstintent' : '<Your Response SSML>', 'yoursecondintent' : { 'custom_slot_1' : '<Your response SSML>',
#                                                                                   'custom_slot_2' : '<Your response SSML'> }}
# 
#
  
# Keep the required responses below to ensure you skill reacts to launch/open, help, and end (as required by ASK).

responses['launch'] = "<speak>Welcome to my real cool skill. It gets data from cool places.</speak> "
responses['help'] = "<speak>Use my cool skill that simplifies data retrieval for you. Suggest some intents to try.</speak>"
responses['end'] = "<speak>Thanks for my cool skill. Talk to you soon.</speak>"
   
# Don't Forget, if you update your json filename, update it here too!
with open('responses/response.json', 'w') as outfile:
    json.dump(responses, outfile)
