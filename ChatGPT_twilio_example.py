"""
Definitions:
    send_sms: Compose and send an sms to a number
    sms_reply: process an incoming sms

"""
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    to_phone_number = data['to']
    message_body = data['message']

    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=to_phone_number
    )

    return jsonify({'sid': message.sid})

import requests

def download_media(media_urls):
    for url in media_urls:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the media file locally
            filename = url.split('/')[-1]
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filename}")
    return 0  # TODO return actual information matching success of this process

# In your sms_reply function, call download_media(media_urls) where appropriate


@app.route('/sms', methods=['POST'])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    incoming_msg = request.values.get('Body', '').lower()
    num_media = int(request.values.get('NumMedia', 0))

    resp = MessagingResponse()
    msg = resp.message()

    # Check if there is any media content
    if num_media > 0:  # Process MMS files
        media_urls = [request.values.get(f'MediaUrl{i}') for i in range(num_media)]
        media_content_types = [request.values.get(f'MediaContentType{i}') for i in range(num_media)]
        # Respond with the number of media files received
        msg.body(f"Received {num_media} media file(s).")
        # Optionally, you can also download and process these files here
        progress_status = download_media(media_urls)

    # TODO this seems to suggest that there is no text associated with MMS but is that true?
    else:
        # generate correct flow based on text message
        if 'hello' in incoming_msg:
            msg.body("Hi there! How can I help you today?")
        elif 'bye' in incoming_msg:
            msg.body("Goodbye! Have a great day!")
        else:
            msg.body("Sorry, I didn't understand that. Can you please rephrase?")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
