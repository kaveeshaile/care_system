# main.py

import speech_recognition as sr
from transformers import pipeline
from twilio.rest import Client
from llm import detect_command
from twillo import send_sms
from voice import recognize_speech



# Recognize speech using the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, the service is down.")
        return None

# Load a pre-trained model and detect the command
def detect_command(command):
    classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')
    result = classifier(command)
    print(result)
    if 'call for an ambulance quickly' in command.lower():
        return True
    return False

# Send SMS using Twilio
def send_sms(to_number, from_number, message, account_sid, auth_token):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    print(f"Message sent: {message.sid}")

# Main function to combine everything
def main():
    # Twilio credentials (replace with your actual credentials)
    account_sid = 'AC25e38d6ad17614fb2ff2640aa38a7bd0'
    auth_token = '9c9b06daaff295e4d117424087c83d5a'
    from_number = '+15735273897'
    to_number = '+12252542523'
    home_address = '81/D Honnanthra South Piliyandala'

    command = recognize_speech()
    if command and detect_command(command):
        message = f"Emergency! Please send an ambulance to {home_address}."
        print(message)
        send_sms(to_number, from_number, message, account_sid, auth_token)
    # message = f"Emergency! Please send an ambulance to {home_address}."
    # print(message)
#call for an ambulance quickly
if __name__ == "__main__":
    main()
