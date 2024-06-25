from flask import Flask, request, redirect, url_for, render_template, request
from chat import start_chat
import requests
import json
import subprocess as sp
app = Flask(__name__)




@app.route('/')
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

    
    #   sp.run(['python','train.py'], shell=True)
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

if __name__  == "__main__":
    app.run(host ='0.0.0.0',port = '6868')
    