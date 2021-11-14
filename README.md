# SD-T2

Configuracion topico de ordenes y resumen (fijarse que KAFKA_HOME.sh apunte a la ruta de la carpeta de kafka):

$KAFKA_HOME/bin/kafka-topics.sh --create\
 --bootstrap-server localhost:9092 \
 --replication-factor 1 \
 --partitions 1 \
 --config retention.ms=1080000 \
 --topic ordenes
 
$KAFKA_HOME/bin/kafka-topics.sh --create\
 --bootstrap-server localhost:9092 \
 --replication-factor 1 \
 --partitions 1 \
 --config retention.ms=1080000 \
 --topic resumen
 
 
 Pasos a seguir para correr el software:
  1. Correr zookeeper_run.sh
  2. Correr kafka_run.sh
  3. Correr create_topic.sh
  4. Correr aplicación flask
  5. Ingresar a localhost:5000

 
