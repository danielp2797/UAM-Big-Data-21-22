ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
SET mapreduce.map.memory.mb=4096;
USE uambd11;
SET net.ripe.hadoop.pcap.io.reader.class=net.ripe.hadoop.pcap.HttpPcapReader;
SELECT header_host, count(*) as counter FROM http group by header_host order by counter desc limit 10;
