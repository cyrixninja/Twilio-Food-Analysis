from datetime import time
import re
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)
apikey = "73cf80a8ed3c4a46a964cfeb165bb681"
app = Flask(__name__)
def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')
    response = requests.get(media_url)
    if  response.status_code == 200:
        webquery= ("https://api.spoonacular.com/food/images/analyze?apiKey="+apikey+"&"+"imageUrl="+media_url)   
        response1 = requests.get(webquery)
        respjson=  response1.json()
        name = str(respjson["category"]["name"])
        calories= str(respjson["nutrition"]['calories']['value'])
        fat= (respjson["nutrition"]['fat']['value'])
        protein=(respjson["nutrition"]['protein']['value'])
        carbs=(respjson["nutrition"]['carbs']['value'])
        recipeurl=(respjson["recipes"][0]['url'])
        data="""
Name: {}
Calories : {} calories
Fat : {} g
Protien : {} g
Carbs: {} g
Recipe: {}
        """.format(name,calories,fat,protein,carbs,recipeurl)
        print(data)
        msg.body(data)

    return str(resp)    

if __name__ == '__main__':
    app.run()