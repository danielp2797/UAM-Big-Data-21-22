# comprobacion del puerto donde esta escuchando HDFS
echo "HDFS listening on..."
hdfs getconf -confKey fs.defaultFS

rm -r data/
# creacion de directorios en HDFS
hdfs dfs -rm -r /bitcoin/input 
hdfs dfs -rm -r /bitcoin/output
mkdir data && mkdir data/elasticData #directorio donde se alamcena el json para elasticSearch

python3 prep.py && python3 proc.py

echo "data stored in hdfs directories..."
hdfs dfs -ls /bitcoin/output && hdfs dfs -ls /bitcoin/input
