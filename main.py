from _ast import Sub
from datetime import datetime
import pytz
from flask import Flask , request
import json
import os,sys
from pprint import pprint
from pymessenger import Bot
from wit import Wit

VERIFICATION_TOKEN = "hello"
PAGE_ACCESS_TOKEN = "#"
wit_access_token ="#"
client = Wit(wit_access_token)
app = Flask(__name__)

bot = Bot(PAGE_ACCESS_TOKEN)



@app.route('/', methods =['GET'])
def verify() :
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch" , 403
        return request.args["hub.challenge"] , 200
    return "Hello-world" , 200






@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    printmsg(data)
    process_data(data)
    return "okk",200



def get_wit_response(message_text):
    wit_response = client.message((message_text))
    pprint(wit_response)
    entity = None
    value = None
    intent = None
    try:

        intent = wit_response['intents'][0]['name']

        entities = list(wit_response['entities'].keys())

        entity = wit_response['entities']['location:location'][0]['name']
        value = wit_response['entities']['location:location'][0]['value']
    except:
        pass
    return (intent,entity,value)


def generate_user_response(messaging_text,TimeZones):
    intent,entity,value = get_wit_response(messaging_text)
    response = None
    if intent == 'greeting':
        response = "Hello, how are you."

    elif intent == 'GetTimee' and entity == 'location':

        response = 'The time now in '+value +' is : '+ TimeZones[value]
    else:
        response = "Sorry, i did not understand your message!!"
    return response


#print(get_wit_response("what is time in egypt"))



def process_data(data):

    if data["object"]=="page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                if messaging_event.get("message"):
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    else:

                        messaging_text = "no text"
                    printmsg(messaging_text)
                    response = generate_user_response(messaging_text,timeZones)
                    bot.send_text_message(sender_id,response)



def printmsg(msg):
    pprint(msg)

    sys.stdout.flush()

tz_Egypt=pytz.timezone('Africa/Cairo')
datetime_Egypt = datetime.now(tz_Egypt)
Egypt_T = datetime_Egypt.strftime("%H:%M:%S")

tz_Morocco=pytz.timezone('Africa/Casablanca')
datetime_Morocco = datetime.now(tz_Morocco)
Morocco_T = datetime_Morocco.strftime("%H:%M:%S")

tz_SaudiArabia=pytz.timezone('Asia/Riyadh')
datetime_SaudiArabia = datetime.now(tz_SaudiArabia)
SaudiArabia_T = datetime_SaudiArabia.strftime("%H:%M:%S")

tz_Algeria=pytz.timezone('Africa/Algiers')
datetime_Algeria = datetime.now(tz_Algeria)
Algeria_T = datetime_Algeria.strftime("%H:%M:%S")

tz_Tunisia=pytz.timezone('Africa/Tunis')
datetime_Tunisia= datetime.now(tz_Tunisia)
Tunisia_T = datetime_Tunisia.strftime("%H:%M:%S")


tz_Sudan=pytz.timezone('Africa/Khartoum')
datetime_Sudan= datetime.now(tz_Sudan)
Sudan_T = datetime_Sudan.strftime("%H:%M:%S")

tz_Palestine=pytz.timezone('Asia/Gaza')
datetime_Palestine= datetime.now(tz_Palestine)
Palestine_T = datetime_Palestine.strftime("%H:%M:%S")

tz_Libya=pytz.timezone('Libya')
datetime_Libya= datetime.now(tz_Libya)
Libya_T = datetime_Libya.strftime("%H:%M:%S")

tz_Emirates=pytz.timezone('Asia/Dubai')
datetime_Emirates= datetime.now(tz_Emirates)
Emirates_T = datetime_Emirates.strftime("%H:%M:%S")

tz_Qatar=pytz.timezone('Asia/Qatar')
datetime_Qatar= datetime.now(tz_Qatar)
Qatar_T = datetime_Qatar.strftime("%H:%M:%S")

tz_Kuwait=pytz.timezone('Asia/Kuwait')
datetime_Kuwait= datetime.now(tz_Kuwait)
Kuwait_T = datetime_Kuwait.strftime("%H:%M:%S")

tz_Bahrain=pytz.timezone('Asia/Bahrain')
datetime_Bahrain= datetime.now(tz_Bahrain)
Bahrain_T = datetime_Bahrain.strftime("%H:%M:%S")


timeZones ={
    "egypt" : Egypt_T,
    "algeria" : Algeria_T,
    "palestine" : Palestine_T,
    "emirates" : Emirates_T,
    "kuwait" : Kuwait_T,
    "qatar" : Qatar_T,
    "tunisia" : Tunisia_T,
    "libya" : Libya_T,
    "sudan" : Sudan_T,
    "morocco" : Morocco_T,
    "bahrain" : Bahrain_T,
    "saudi arabia" : SaudiArabia_T

}
#print(generate_user_response("what is time in qatar",timeZones))





if __name__ == '__main__':
    app.run(debug=True, port=80)





























