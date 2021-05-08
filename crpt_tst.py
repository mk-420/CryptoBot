from BOTTEL import telegram_chatbot
import json
import requests
from datetime import datetime
from urllib.request import urlopen
# loads subscriber data
st=48;sth=57.5

bot = telegram_chatbot("config.cfg")
# this adds subscriber
def checker(st,sth):
    response = requests.get("https://api.wazirx.com/api/v2/tickers")
    obj = response.json()
    pr = float(obj["dogeinr"]["last"])
    if(pr<st or pr>sth):
        print(st)
        print(sth)
        bot.send_message(pr,650222726)
def SubTimer(msg, id):
    if informer(msg) != "Please enter correct district. You may check spelling on Google :)":
        ub[id] = msg
        with open("SubData.txt", "r+") as withRp:
            withRp.truncate()
            withRp.write(str(ub))
        return "You Are Now Subscribed.\nYou will recieve daily Corona Updates at 9 am everyday." + "\n\n" + informer(
            msg)
    else:
        return "Press /daily again and re-Enter Correct District spelling"
# this is schedule message sender
def sender():
    print("Schedule Message Sent")
    for ids, dists in ub.items():
        bot.send_message("Good Morning\n\n"+str(informer(dists)), ids)


# this is main function which uses json data from covid 19 api and searches it "
def informer(dist):
    response = requests.get("https://api.wazirx.com/api/v2/tickers")
    obj = response.json()
    pr=(obj["dogeinr"]["last"])
    ts= (obj["dogeinr"]["at"])
    time = datetime.fromtimestamp(ts)
    print(time.time())
    return "Price "+pr

schedule.every().day.at("03:30").do(sender)

print("Bot server is ON")
# this processes the input
def make_reply(msg):
    reply = None
    if msg is not None:
        reply = informer(msg)
        print(msg)
        return reply
# id for knowing if subbscribe request
stid = False
update_id = None
# this lop fetch updates and passes it
while True:
    message=checker(st,sth)
    schedule.run_pending()
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]  # this stors all user id text etc

    # below lines checks if updates have came or timeout is done(came is +1 update id)
    # if came it fetch message text and user id . it sends meesage INPUT to the make reply function ,the OUTPUT
    # from this make reply is returned to send message function with user id that this fetched from updates
    # takes input and SUBSCRIBER ID and sends ,this message reciever
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]  # id
            try:
                print(item["message"]["from"]["username"])
            except:
                print(str(item["message"]["from"]["first_name"])+" "+str(item["message"]["from"]["last_name"]))
            if message == "/daily":
                print(message)
                bot.send_message("Enter District for which you would like daily updates", from_)
                stid = True
            elif stid is True:
                stid = False
                reply = SubTimer(message, from_)  # sent to process input
                print(message + " >>" + "sucess subs")
                bot.send_message(reply, from_)  # returns output with  id
            if "Setl" in message:
                print(message)
                st=float(message[4:])
            elif "Seth" in message:
                print(message)
                sth = float(message[4:])
            else:
                reply = make_reply(message)
                bot.send_message(reply, from_)
