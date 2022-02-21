ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
SET net.ripe.hadoop.pcap.io.reader.class=net.ripe.hadoop.pcap.DnsPcapReader;
--SET hive.vectorized.execution.enabled=true; 
USE uambd11;

CREATE TABLE IF NOT EXISTS dns_domains_vorc
STORED AS ORC -- FORMATO NECESARIO PARA EL EJ 10
AS select split(substring(dns_question, 0, instr(dns_question, ' ')),'\\.')[
SIZE(split(substring(dns_question, 0, instr(dns_question, ' ')),'\\.'))-3] 
AS site_name_splitted FROM dns;

EXPLAIN SELECT site_name_splitted,
count(*) AS counter 
FROM dns_domains_vorc 
GROUP BY site_name_splitted 
ORDER BY counter DESC;
