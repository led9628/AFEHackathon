# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

# @authors Leah Dibble, Sophia Szady, Maggie Wong, Ashley Martin, Bella Ciagne 

import logging
import ask_sdk_core.utils as ask_utils

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_model.interfaces.audioplayer import AudioItem, Stream, PlayDirective, PlayBehavior
from utils import create_presigned_url

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

counter=0
numberCounter = 0
itemCounter = 0
yesNoCounter = 0

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "<speak><prosody rate='fast'>Welcome to Code Chronicles! Let's go on a journey to face the Bugmaster, who's been destroying programs across the land and it's your job to stop him. What's your name hero?</prosody></speak>"
        reprompt_text = "My name is Alexa, what yours?"
        
        global counter
        global numberCounter
        global itemCounter
        global yesNoCounter
        counter=0
        numberCounter = 0
        itemCounter = 0
        yesNoCounter = 0
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class CaptureHeroIntentHandler(AbstractRequestHandler):
    """Handler for Capture Hero Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CaptureHeroIntent")(handler_input)

    def handle(self, handler_input):
         # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        Name = slots["Name"].value
        speak_output = "<speak><prosody rate='fast'> Okay {Name}, lets head towards Bugmaster’s castle! Up ahead, you see some friendly faces. Look's like it's time to meet your team, the Data Type Squad! Hi, I'm Int the Inch-worm and I’m every number you can think of, so talk to me whenever you want to use numbers! Hi I'm boolean the butterfly! When I'm not flying around, I can either be true or false, like a light switch is either on or off. Hi I'm string the spider! from one word to an entire sentence, I'm everything you can say or write! And together we make up Team Data Types! Up ahead there’s a big web covered with letters blocking the path. Who on your team should join you?</prosody></speak>".format(Name=Name)
        reprompt_text = "Not quite. Remember, who lives in a web and works with words?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
         )

class DataChallengeIntentHandler(AbstractRequestHandler):
    """Handler for all data Challenge prompts in level 1"""
    def can_handle(self, handler_input):
        #type: (handler_input) -> bool 
        return ask_utils.is_intent_name("DataChallengeIntent")(handler_input)
    
    def handle(self, handler_input):
        #type (handler_input) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        answer = slots["answer"].value.lower()
        
        global counter
        speak_output = 'you shouldnt be here, speak' + str(counter)
        reprompt_text = 'you shoudnt be here either, reprompt'
        
        if counter == 0:
            correctList = ["spider","string","string the spider"]
            if answer in correctList:
                counter += 1
                speak_output = "<speak><prosody rate='fast'> Correct! String the spider goes up to the web and collects all the letters that spell good job! You're now 200 steps from Bugmaster’s castle! Who do you think should keep track of the number of steps?</prosody></speak>"
                reprompt_text = 'That is incorrect. Please try again. Remember: Who on your teams deals with numbers?'
            else:
                speak_output = "Sorry, that's incorrect. Remember: Who lives in a web and works with words?"
                reprompt_text = "Which team member should you call on?"
        elif counter == 1:
            correctList = ['int','inchworm','inch worm','int the inchworm']
            if answer in correctList:
                counter +=1 
                speak_output = "<speak><prosody rate='fast'> Yes! Int the Inch Worm will track how far you are from the castle moving forward. You see a bridge up in the distance with rapid water underneath. You can either cross the bridge or swim across. Who should we call on to make this decision?</prosody></speak>"
                reprompt_text = "Here's a clue: Who on your team deals with two choice decisions like a lightswitch or true or false?"
            else:
                speak_output = "That is incorrect. Remember: who deals with numbers on the team?"
                reprompt_text = "Remember, which of your teammates deals with two choice decisions like a lightswitch or true or false"
        elif counter == 2:
            correctList = ['bool', 'boolean', 'butterfly', 'boolean the butterfly']
            if answer in correctList:
                counter+=1
                speak_output = "<speak>Yes! Boolean the butterfly chooses to cross the bridge to avoid the water underneath. However, a troll is guarding it. The troll says to you: <voice name = 'Matthew'> answer this question to cross my bridge: how many data types have you learned about so far?</voice></speak>"
                reprompt_text = "Here's a hint: how many team members do you have?"
            else:
                speak_output = "Remember who deals with 2 choice decisions?"
                reprompt_text = "Try again, which team member should you call on?"
        elif counter == 3:
            correctList = ['int','inchworm','inch worm','int the inchworm']
            checker = answer in correctList
            if checker:
                speak_output = "<speak><voice name = 'Matthew'>You've completed my riddle! Here, you'll need this tool belt for your journey.</voice> You've completed level 1, now it's time to learn movement abilities. Int the inchworm tells you that you're now 150 steps away from Bugmaster’s castle and points out something blowing in the wind. You and the Data Squad run ahead and realize it's a map! You’ve learned the movement skill. Try it out by saying move left or move right.</speak>"
                reprompt_text= "Who works and stores numbers?"
            else:
                speak_output = "Think about who deals with numbers"
                reprompt_text = "Try again, you got this!"
        else:
            speak_output = "count var too high"
            reprompt_text = "Count var too high (reprompt_text)"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class NumberHandler(AbstractRequestHandler):
    """Handler for Number Usage"""
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NumberIntent")(handler_input)  
    def handle(self, handler_input):
        #type (handler_input) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        answer = slots["number"].value.lower()
        global numberCounter
        
        if numberCounter == 0:
            if answer == '3':
                numberCounter += 1
                speak_output = "<speak><voice name='Matthew'>Okay you got me... For a bonus point what data type was the answer to that question?</voice></speak>"
                reprompt_text = "Who on your team deals with numbers"
            else:
                speak_output = "Think about who's on your team"
                reprompt_text = "Try again, remember who is on your team"
        elif numberCounter == 1:
            numberCounter += 1
            speak_output = "<speak><prosody rate='fast'>Woohoo let’s loop it all day! You finally arrive at Bugmaster’s castle and put everything back in your tool belt. Once the door opens, you see Bugmaster waiting. Your speaker suddenly starts buzzing and a new song titled “Bugmaster” appears. Should you play the song?</prosody></speak>"
            reprompt_text = 'oh no try a number'
        else:
            speak_output = 'you shouldnt be here'
            reprompt_text = 'you shoudnt be here either'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )
class ItemIntentHandler(AbstractRequestHandler):
    """Handler for Item Usage"""
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ItemIntent")(handler_input)
    def handle(self, handler_input):
        #type (handler_input) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        item = slots["item"].value.lower()
        global itemCounter
        
        if itemCounter == 0:
            if item == 'umbrella':
                itemCounter += 1
                speak_output = "<speak><prosody rate='fast'>Nice Job! You ask boolean the butterfly how far you are from the castle, but then int chimes in to say that you're only 50 steps away and that the journey could use some music! You receive a speaker and continue on your way. Once you get out of the town all you want is to listen to your favorite song over and over. How many times do you want to listen?</prosody></speak>"
                reprompt_text = "umbrella reprompt"
            elif item == 'map':
                speak_output = "Are you sure? If you don’t take out the umbrella you will be rained on"
                reprompt_text = "map reprompt"
        elif itemCounter == 1:
            itemCounter += 1
            if item == 'umbrella':
                speak_output= "<speak><prosody rate='fast'>As you get out your umbrella the Bugmaster sound comes to an end. Should you press the repeat button to loop the song?</prosody></speak>"
                reprompt_text= "Are you sure? It seemed to be working"
            elif item == 'map':
                speak_output= "Maybe try another item"
                reprompt_text= "second map reprompt"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class LevelTwoIntentHandler(AbstractRequestHandler):
    """Handler for Level Two"""
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LevelTwoIntent")(handler_input)  
    def handle(self, handler_input):
        #type (handler_input) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        answer = slots["direction"].value.lower()
        
        if answer == 'left':
            speak_output= "Oh no! There's a big boulder blocking the path, try moving right"
            reprompt_text = 'say move right'
        elif answer == 'right':
            speak_output = "<speak><prosody rate='fast'>Great Job! You're approaching a busy town marking 100 steps away from the castle, but there are storm clouds ahead. Luckily a kind townsfolk gives you their extra umbrella. He tells you that if it is raining, use an umbrella. You put the umbrella in your tool belt next to the map. As you walk through town, you feel some raindrops. Looking down at your tool belt, what should you take out?</prosody></speak>"
            reprompt_text = "insert here"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
            )
class LevelBossHandler(AbstractRequestHandler):
    """Handler for Level Boss"""
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LevelBossIntent")(handler_input)
    def handle(self, handler_input):
        global yesNoCounter
        #type (handler_input) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        answer = slots["YesorNo"].value.lower()
        slots = handler_input.request_envelope.request.intent.slots
        if yesNoCounter == 0:
            if answer == 'yes':
                yesNoCounter+=1
                speak_output= "<speak><audio src='soundbank://soundlibrary/electrical/feedback_mics/feedback_mics_06'/>Bugmaster covers his ears, maybe this is a solution! But then Bugmaster starts to spray water and you know that if the speaker gets wet, it will break. What use from your toolbelt?</speak>"
                reprompt_text= "Are you sure? It may help save the land"
            elif answer == 'no':
                speak_output= "Hmmmm... it might help"
                reprompt_text= "boss no reprompt"
        elif yesNoCounter == 1:
            yesNoCounter+=1
            if answer == 'yes':
                speak_output= "<speak><audio src='soundbank://soundlibrary/electrical/feedback_mics/feedback_mics_06'/>The sound starts again and makes Bugmaster dizzy! He spins around really fast and sprays water everywhere! He suddenly vanishes and the whole team cheers. Do you want to go home?</speak>"
                reprompt_text= "final loop reprompt"
            elif answer == 'no':
                speak_output= "hmmm are you sure?"
                reprompt_text= "second to last no reprompt"
        elif yesNoCounter == 2:
            yesNoCounter+=1
            if answer == 'yes':
                speak_output= "<speak> You take out the map and as soon as you do you are swept up and you are dropped back at home with the whole data squad. <audio src='soundbank://soundlibrary/musical/amzn_sfx_trumpet_bugle_03'/>''Congratulations you have completed code chronicles and saved all programmers from the bugmaster!</speak>"
                reprompt_text= "This has been a long journey are you sure?"
            elif answer == 'no':
                speak_output= "The team looks at you and you can tell they are tired, should you go home?"
                reprompt_text= "final no reprompt"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureHeroIntentHandler())
sb.add_request_handler(DataChallengeIntentHandler())
sb.add_request_handler(NumberHandler())
sb.add_request_handler(ItemIntentHandler())
sb.add_request_handler(LevelTwoIntentHandler())
sb.add_request_handler(LevelBossHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
