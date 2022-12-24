ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
CREATE DATABASE IF NOT EXISTS uambd11;
USE uambd11;
DROP TABLE pcaps;
CREATE EXTERNAL TABLE pcaps(ts bigint,protocol string,src string,src_port string,dst string, dst_port string,len
int,ttl int)
ROW FORMAT SERDE 'net.ripe.hadoop.pcap.serde.PcapDeserializer'
STORED AS INPUTFORMAT 'net.ripe.hadoop.pcap.mr1.io.PcapInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 'hdfs:/user/uambd11/pcaps/';
