ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;
--SET mapreduce.map.cpu.vcores=3;

USE uambd11;

SELECT src, dst, protocol, sum(len) AS bytes, count(*) AS packages 
    FROM pcaps
    WHERE protocol IN ('UDP', 'TCP')
    GROUP BY src, dst, protocol
    ORDER BY packages DESC;
