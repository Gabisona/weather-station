import json
import sqlite3

import paho.mqtt.client as mqtt
from flask import Flask, render_template

app = Flask(__name__)

temperatura = ''
umidade = ''

@app.route("/")
def index():
  user = 'senai'
  password = '050825'
  endereco = 'mqtt.eclipseprojects.io'
  port = 1883
  topico = 'senaiamigues'

  def on_message(client, userdata, msg):
    dados = json.loads(msg.payload)
    global temperatura
    global umidade 
    temperatura = dados['Temperatura']
    umidade = dados['Umidade']
    print(f"Temperatura: {temperatura} °C | Umidade: {umidade}")
    #print(msg.payload)
                                     
  client = mqtt.Client()
  client.username_pw_set(user, password)
  client.connect (endereco, port)
  client.subscribe(topico)
  client.on_message = on_message
  client.loop_start()
  
  #BANCO DE DADOS
  connection = sqlite3.connect("arduininho")
      
  connection.execute("CREATE TABLE IF NOT EXISTS metereologiaDB (id INTEGER PRIMARY KEY, temperatura STRING, umidade STRING);")
        
  connection.execute("INSERT INTO metereologiaDB (temperatura, umidade) VALUES (?, ?)", (temperatura, umidade))
        
  dados_temp = connection.execute("SELECT * FROM metereologiaDB")
  print(dados_temp.fetchall())
  connection.commit()
  connection.close()

  return render_template('index.html', temperatura=temperatura, umidade=umidade)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
