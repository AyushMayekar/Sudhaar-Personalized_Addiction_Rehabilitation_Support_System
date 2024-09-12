from twilio.rest import Client

def Contact():

    account_sid = 'AC5384fff47d5c7fb261da661ad2ac5f82'
    auth_token = '3b10bbc9a827a7360bb0fe0af73e67f3'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Urgent: Please contact [Emergency Services Number] immediately. [Patient's Name] is in a critical situation at [Location], experiencing [brief description of the emergency, e.g., severe withdrawal symptoms/unconsciousness]. Your immediate presence and assistance are needed. For more details, please call [Your Phone Number].",
        from_='+15108764218',
        to='+919867511579'
    )

    print(message.sid)

if __name__ == '__main__':
    Contact()