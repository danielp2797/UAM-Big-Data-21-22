ADD JAR hdfs:///user/uambd11/libs/hadoop-pcap-serde-1.2-SNAPSHOT-jar-with-dependencies.jar;

USE uambd11;

SELECT ts, sum(len)*8 as bits
    from pcaps 
    group by ts 
    order by ts;
