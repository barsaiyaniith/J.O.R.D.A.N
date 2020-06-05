import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import playsound

#ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return it as string

def recordAudio():

    # record audio
    r = sr.Recognizer() # Creating a recognizer object

    #open mic and start recording
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


        #Use Google speech recognition to recognize whatwe say
        data = ''
        try:
            data = r.recognize_google(audio)
            print('You said :' + data)
        except sr.UnknownValueError: # check for unknown errors
             print('Google Speech Rec not able to understand the audio')
        except sr.RequestError as e:
            print('request result from Google speech reg error')

        return data

# A function to get the vr resonse

def assistantResponse(text):

    print(text)

    #Convert the text to speech

    text_speech = gTTS(text=text, lang ='en', slow=False)

    # Save the converted audio to a file
    text_speech.save('assistant_response.mp3')


    #play the converted file
    os.system('mpg123 assistant_response.mp3')
    #playsound.playsound('assistant_response.mp3')

# Function for wake work
def wakeWord(text):
    WAKE_WORDS = ['hey jordan']

    text = text.lower() ## to convert to lower cases


    # check to see if the user command or text have wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    # if the wake word isnt found
    return False

# funct for current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today() 
    week_day = calendar.day_name[my_date.weekday()] # e.g. monday
    monthNum = now.month
    dayNum = now.day

    # a list of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]

    # a list of ordinal numbers
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    return 'Today is ' +week_day+ ', '+ month_names[monthNum-1]+ ' the '+ ordinalNumbers[dayNum-1]+'.'

# function to return a random greeting response
def greeting(text):

    # greeting inputs
    GREETINGS_INPUTS = ['hi','hey','wassup','hello']

    #greeting responses
    GREETING_RESPONSES = ['Hello Sir', 'hey there']


    # if the users input is a greeting then return raamdomly resp
    for word in text.split():
        if word.lower() in GREETINGS_INPUTS:
            return random.choice(GREETING_RESPONSES)+'.'
        # if not detected then return empty string
    return ''

# funct for person firstand last name from text
def getPerson(text):

    wordList = text.split()  # splitting the text into a list of words
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) -1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' '+ wordList[i+3]

while True:

    # record the audio
    text = recordAudio()
    response = ''

    # check for the wake words /phrase
    if(wakeWord(text) == True):

        # check for greeting by user
        response = response + greeting(text)

        # check to see user say regards date
        if('date' in text):
            get_date = getDate()
            response = response + ' '+get_date
        
        # check with time
        if('time' in text):
            now = datetime.datetime.now()
            meridiem =''
            if now.hour >= 12:
                meridiem ='p.m' # post meridiem (pm) after midday
                hour = now.hour - 12
            else:
                meridiem = 'a.m' #anti meridiem (am) before midday
                hour = now.hour

            #convert minute into a propoer string
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)
            
            response = response +' '+'It is '+str(hour)+':'+minute+' '+meridiem+' .'

        
        # if who is name
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response+ ' '+ wiki

        #have the assistant to response back using audio
        assistantResponse(response)
