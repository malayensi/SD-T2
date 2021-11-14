from logging import error
import smtplib, ssl
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from flask import request
import json
from flask import *
import time
app= Flask(__name__)
contador=0
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "correomailnewnuevo@gmail.com"  # Enter your address
password = "clavecorreo1235"

context = ssl.create_default_context()





@app.route('/', methods=['GET'])
def aplicacion():

    
    return render_template('index.html')






@app.route('/pagina', methods=['POST'])
#http://127.0.0.1:5000/login?username=usuario&password=clave

def pagina():
    
    #return(f"<h3>hola mundo { request.form.get('correo') } </h3>")
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers=['localhost:9092'])
    producer.send('orders', {"Nombre cocinero":request.form['Nombre cocinero'],"Nombre vendedor":request.form['Nombre vendedor'],"Cantidad sopaipillas vendidas":request.form["Cantidad sopaipillas vendidas"],"Correo vendedor":request.form["Correo vendedor"],"Correo cocinero":request.form["Correo cocinero"]})
    producer.flush()
    
    return render_template("pagina.html")
@app.route('/resumen', methods=['GET'])



def resumen():
    diccionario={}
    global contador
    print(contador)
    consumer = KafkaConsumer('orders',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset='earliest', enable_auto_commit=False)
    partitions=  [TopicPartition('orders', p) for p in consumer.partitions_for_topic('orders')]
    last_offset_per_partition = consumer.end_offsets(partitions)
    numero=list(last_offset_per_partition.values())[0]
    print(numero)
    #print((mensaje))
    if contador==0:
            for message in consumer:
                print(message.value)
                if message.value["Nombre cocinero"] not in diccionario.keys():
                        diccionario[message.value["Nombre cocinero"]]={"Nombre cocinero":message.value["Nombre cocinero"],"Nombre vendedor":message.value['Nombre vendedor'],"Cantidad sopaipillas vendidas":int(message.value["Cantidad sopaipillas vendidas"]),"Correo vendedor":message.value["Correo vendedor"],"Correo cocinero":message.value["Correo cocinero"]}
                else:
                        diccionario[message.value["Nombre cocinero"]]["Cantidad sopaipillas vendidas"]+=int(message.value["Cantidad sopaipillas vendidas"])
                contador+=1
                print(contador)
                if contador==numero:
                        break
    else:
        if numero>contador:
            for message in consumer:
                if message.value["Nombre cocinero"] not in diccionario.keys():
                    diccionario[message.value["Nombre cocinero"]]={"Nombre cocinero":message.value["Nombre cocinero"],"Nombre vendedor":message.value['Nombre vendedor'],"Cantidad sopaipillas vendidas":message.value["Cantidad sopaipillas vendidas"],"Correo vendedor":message.value["Correo vendedor"],"Correo cocinero":message.value["Correo cocinero"]}
                else:
                    diccionario[message.value["Nombre cocinero"]]["Cantidad sopaipillas vendidas"]+=message.value["Cantidad sopaipillas vendidas"]
                contador+=1
                if contador==numero:
                        break
    for cocinero in diccionario.keys():
        message = f"""\
        Subject: resumen diario

        Nombre cocinero:{cocinero},Nombre vendedor:{diccionario[cocinero]["Nombre vendedor"]},Cantidad sopaipillas vendidas:{diccionario[cocinero]['Cantidad sopaipillas vendidas']}."""
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, diccionario[cocinero]["Correo cocinero"], message)
            server.sendmail(sender_email, diccionario[cocinero]["Correo vendedor"], message)
    print(diccionario)
    return render_template("resumen.html")
    time.sleep(5)
    #return render_template('index.html')
if __name__=="__main__":
    app.run()