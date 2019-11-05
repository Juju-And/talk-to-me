import time
from time import gmtime, strftime
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='pl-PL')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# COMMANDS = ['Hello', 'What is the time?', 'banana']

# format the instructions string
instructions = (
    "Przywitaj się z aplikacją, a następnie możesz zapytać ją o godzinę lub pogodę w mieście X")

# show instructions and wait 3 seconds before starting the game
print(instructions)
time.sleep(3)
print("Powiedz coś!")

first_speech = recognize_speech_from_mic(recognizer, microphone)
if first_speech["transcription"]:
    if first_speech["transcription"] == "cześć":
        print("Siemanko!")

if not first_speech["success"]:
    print("success")
# print("Nie zrozumiałem. Co powiedziałeś/aś?\n")

second_speech = recognize_speech_from_mic(recognizer, microphone)
if second_speech["transcription"] == "która godzina":
    curr_time = strftime("%H:%M:%S", gmtime())
    print(curr_time)
