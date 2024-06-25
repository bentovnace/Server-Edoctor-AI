from flask import Flask, request,request_tearing_down,jsonify,render_template, request
from chat import start_chat
import requests
import json
from  pymessenger.bot import Bot
import subprocess as sp
app = Flask(__name__)
ACCESS_TOKEN  ="EAANu788WJRcBAEsaODXm805XMrnEsiLUZBpeDaF8EZAIJ6Vw3ZBValTL7D7fdRpDEiLiE4N16OrBp6kAYIPEKqXsjpQfT0ZB9PVaroIzj2MnZBuIYtCs2aLsqdxJ8n48ABoV2xfpZA4EHpWOunwV2JWeDAbvuk0KZBd7gfv1cxJYv78aa2k8toVATx88cV3UY8ZD"
VERIFY_TOKEN ="bentovnace"

bot = Bot(ACCESS_TOKEN)




@app.route('/home')
def hello_world():
    return render_template("login.html")


@app.route('/data',methods=['POST','GET'])  
def login():
    tag=request.form['tag']
    patterns=request.form['patterns']
    responses=request.form['responses']
    
    readFile = open("intents.json",encoding = "UTF-8") 
    lines = readFile.readlines() 
    readFile.close() 
    w = open("intents.json",mode='w',encoding = "UTF-8") 
    w.writelines([item for item in lines[:-2]])
    w.close()
    
    file_object_2 = open('intents.json', mode ='a')
    
    file_object_2.write(',\n{\n"tag": '+'"'+tag+'"'+',\n"patterns": [\n   '+'"'+patterns+'"'+'\n],\n"responses": [\n  '+'"'+responses+'"'+'\n]\n  }'+'\n]\n'+'}')
    file_object_2.close()

    
    sp.run(['python','train.py'], shell=True)
    return render_template('home.html',name=tag, name2=patterns, name3=responses)

@app.route('/edoctor', methods=['GET','POST'])


def chatbot():
    chatInput = request.args.get('input')
    r = requests.get('http://coronavirus-19-api.herokuapp.com/countries/Vietnam')
    data =r.json()
    covid = f'Ca nhiễm:{data["cases"]}\nChết: {data["deaths"]} \nKhỏi:{data["recovered"]} \nSố ca nhiễm trong ngày: {data["todayCases"]}'
    if chatInput == "Diễn biến covid 19" or chatInput =="Tình hình covid 19" or chatInput == "Diễn biến covid 19 ở Việt Nam" or chatInput =="Tình hình covid 19 ở Việt Nam" or chatInput == "Số ca nhiễm" or chatInput =="Chết" :
        return covid
    else:
        return str(start_chat(chatInput))



@app.route('/', methods=['GET','POST'])
def chatbotFacebook():
    if request.method =="GET":
        if request.args.get('hub.verify_token')==VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return "token fail"
    
    
    
    if request.method =="POST":
        
        output = request.get_json()
        for event in output['entry']:
            message = event['messaging']
            for data in message:
                recipient_id = data['sender']['id']
                if data ['message'].get('text'):
                    msg = data['message']['text']
                    r = requests.get('http://coronavirus-19-api.herokuapp.com/countries/Vietnam')
                    data =r.json()
                    covid = f'Ca nhiễm:{data["cases"]}\nChết: {data["deaths"]} \nKhỏi:{data["recovered"]} \nSố ca nhiễm trong ngày: {data["todayCases"]}'
                    if msg == "Diễn biến covid 19" or msg =="Tình hình covid 19" or msg == "Diễn biến covid 19 ở Việt Nam" or msg =="Tình hình covid 19 ở Việt Nam" or msg == "Số ca nhiễm" or msg =="Chết" :
                        response = covid
                    else:
                        response = str(start_chat(msg))
                    
                    bot.send_text_message(recipient_id,str(response))
                else:
                    pass
        return "ok"


if __name__  == "__main__":
    app.run(host ='0.0.0.0',port = '5000')
    