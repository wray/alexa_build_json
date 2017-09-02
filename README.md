# alexa_build_json
This is an alexa skill python template that prepares an uploads a json file to S3 to be used by the lambda to implement the skill.

The way it works:
* Using a JSON convention where the keys match to intents and slots match to intent_slot.
* The actual python lambda function simply parses the JSON file at runtime.
* Therefore, during a TravisCI build, you can do whatever necessary to populate your skill data (e.g. call an API, call your database).
* This prevents the lambda from having to call the API/db for every invocation -- good for multiple or excessive API calls required to get your data.
* However, you must rebuild to ensure your data is "fresh".

## Build (Heavy lifting done here) -> Deploy -> Run
### Build-time
1) Push to master will initiate a Travis Build.
2) Travis runs the build script that calls your custom python code in pre/build_json.py to create a json file.
3) Your build_json.py will output to the json file in the response directory.
4) When that succeeds, Travis will place the lambda function in place AND the JSON file in S3.
### Run-time
5) The lambda merely opens and reads the json from S3 to respond to the skill intents.

## Make sure to update:
1) The Travis.yml with your values.
2) The src/alexa_py to ensure you use the correct S3 bucket.
3) Build your skill -- design your intent schema so you know what should go in your JSON file.
4) The pre/build_json.py file to generate the json for your specific skill.

Do 1 and 2 first and create a skill using the speechAssets. With the existing speechAssets and the default build_json.py file you should have a working skill whose intents are all "not implemented". You can see that some intents are "required" for all skills, so simply update the response for those with information relevant to your skill.
