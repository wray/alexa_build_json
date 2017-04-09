"""
Simple Python Lambda service providing information on meetups in Central Virginia.

Intents supported:
  Upcoming
  GetEventsByTopic


"""

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import settings
import urllib2
import json
import time
import datetime
import pytz

# Assume tz on lambda is UTC
day = datetime.datetime.now().timetuple() # probably should move into function
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')
key = settings.MEETUP_API_KEY


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': 'RVA Meetups',
            'content': 'The RVA Meetups provides information on upcoming meetups in Richmond and the Central Virginia area. Go to meetup.com for details on upcoming meetings and groups in your area that share your interests.'
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Helpers -----------------
def strip_specials(s):
    return s.replace('&','and').replace('/',',')

def say_time(t):
    utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(t))
    loc_dt = utc_dt.astimezone(eastern)
    if loc_dt.minute == 0:
        return loc_dt.strftime('%A %B %-d, %-I %p')
    else:
        return loc_dt.strftime("%A %B %-d, <say-as interpret-as='cardinal'>%-I</say-as> %M %p")

def speak_events(events,lookahead):
    speech = ''
    num_events = len(events)
    for i in range(num_events if num_events <= 20 else 20):
        t = events[i]['time']
        t = t/1000
        if t <= int(time.mktime((day[0],day[1],day[2] + lookahead, 23, 59, 0, 0, 0, 0))):
            speech += '%s by %s on %s. ' % (strip_specials(events[i]['name']),
                                            strip_specials(events[i]['group']['name']),
                                            say_time(t))
            speech += "<break time='500ms' />"
    return speech



# --------------- Your functions to implement your intents ------------------
def upcoming(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = ""
    should_end_session = True

    speech_output = "<speak> The following meetup events are happening in Central Virginia very soon. "

    resp = urllib2.urlopen('https://api.meetup.com/find/events?radius=50&order=time&sign=true&key='+key)

    speech_output += speak_events(json.loads(resp.read()),1)

    speech_output += " </speak>"

    return build_response(session_attributes, build_speechlet_response
                          (intent['name'], speech_output, reprompt_text, should_end_session))



def get_events_by_topic(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    
    topic = intent['slots']['topic']['value']

    speech_output = "<speak> The following meetup events related to " + topic + " are happening soon in Central Virginia. "

    cat = urllib2.urlopen('https://api.meetup.com/find/topic_categories?&sign=true&photo-host=public&key=%s' % (key))

    j = json.loads(cat.read())
    top_id = 1
    for i in range(len(j)):
        if topic in j[i]['shortname']:
            top_id = j[i]['id']
    
    resp = urllib2.urlopen('https://api.meetup.com/recommended/events?radius=50&order=times&sign=true&topic_category=%d&key=%s' % (top_id,key))

    speech_output += speak_events(json.loads(resp.read()),7)

    speech_output += " </speak>"

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "<speak>Thank you for checking out meetups in Central Virginia. " \
      "The Silicon Valley of the South </speak>"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))




# --------------- Primary Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    logger.info("on_session_started requestId=" + session_started_request['requestId'] +
                ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    logger.info("requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return build_response({},build_speechlet_response(
        "RVA Meetups", "<speak>Welcome to the 4 1 1 for RVA Meetups. This skill provides information about upcoming Meetups in RVA. Learn about your meetups and all the others in Central Virginia as we work to create the Silicon Valley of the South. Ask for upcoming events to hear about meetings coming up immediately.</speak>","",False))


def get_help():
    """ Called when the user asks for help
    """

    return build_response({},build_speechlet_response(
        "RVA Meetups","""<speak>This skill provides upcoming Meetup information. Try asking for upcming events.</speak>""","",False)) 


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "Upcoming":
        return upcoming(intent,session)
    elif intent_name == "GetEventsByTopic":
        return get_events_by_topic(intent,session)    
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return on_session_ended(event['request'], event['session'])
