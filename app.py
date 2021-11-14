from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from flask import request
import json
from flask import *
import time
app= Flask(__name__)
contador=0
@app.route('/', methods=['GET'])
def aplicacion():

    
    return render_template('index.html')

@app.route('/pagina', methods=['POST'])
#http://127.0.0.1:5000/login?username=usuario&password=clave

def pagina():
    
    #return(f"<h3>hola mundo { request.form.get('correo') } </h3>")
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=['localhost:9092'])
    producer.send('event', json.dumps(request.form))
    producer.flush()
    
    return render_template("pagina.html")
@app.route('/resumen', methods=['GET'])
def resumen():
    global contador
    print(contador)
    consumer = KafkaConsumer('event',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         auto_offset_reset='earliest', enable_auto_commit=False)
    partitions=  [TopicPartition('event', p) for p in consumer.partitions_for_topic('event')]
    last_offset_per_partition = consumer.end_offsets(partitions)
    numero=list(last_offset_per_partition.values())[0]
    for message in consumer:
            if contador==numero:
                break
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
            contador+=1
            if contador==numero:
                contador+=1
                break
    
    return render_template("resumen.html")
    time.sleep(5)
    #return render_template('index.html')
if __name__=="__main__":
    app.run()
