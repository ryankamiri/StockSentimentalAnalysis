import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv()


account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
client = Client(account_sid, auth_token)

message = client.messages.create(body="Join Earth's mightiest heroes. Like Kevin Bacon.", from_=os.getenv("TWILIO_NUMBER"), to='')

print(message)
print()
print(message.sid)