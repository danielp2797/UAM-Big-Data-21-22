ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
SET net.ripe.hadoop.pcap.io.reader.class=net.ripe.hadoop.pcap.HttpPcapReader;
USE uambd11;
SELECT count(distinct `header_user-agent`) as user_agents_count, count(*) as tr_count FROM http;
