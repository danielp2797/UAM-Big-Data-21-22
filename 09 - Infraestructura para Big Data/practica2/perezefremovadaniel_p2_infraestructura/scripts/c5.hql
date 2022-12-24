ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
SET net.ripe.hadoop.pcap.io.reader.class=net.ripe.hadoop.pcap.HttpPcapReader;
USE uambd11;
SELECT http_response, count(*) as res_count FROM http GROUP BY http_response;
