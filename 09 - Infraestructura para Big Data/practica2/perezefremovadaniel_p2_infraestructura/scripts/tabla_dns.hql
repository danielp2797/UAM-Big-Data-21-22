ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
CREATE DATABASE IF NOT EXISTS uambd11;
USE uambd11;
SET net.ripe.hadoop.pcap.io.reader.class=net.ripe.hadoop.pcap.DnsPcapReader;
DROP TABLE dns;
CREATE EXTERNAL TABLE dns(ts bigint, src string,dst string,dns_queryid int,dns_qr boolean,dns_opcode
string,dns_rcode string,dns_question string,dns_answer array<string>)
ROW FORMAT SERDE 'net.ripe.hadoop.pcap.serde.PcapDeserializer'
STORED AS INPUTFORMAT 'net.ripe.hadoop.pcap.mr1.io.PcapInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 'hdfs:/user/uambd11/pcaps/';
