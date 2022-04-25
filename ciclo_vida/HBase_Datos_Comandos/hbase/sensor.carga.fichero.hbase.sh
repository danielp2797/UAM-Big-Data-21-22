hbase org.apache.hadoop.hbase.mapreduce.ImportTsv -Dimporttsv.separator=',' -Dimporttsv.columns='HBASE_ROW_KEY,info:temp_in,info:temp_out,info:vibration,info:pressure_in,info:pressure_out' sensor /tmp/sensor.hbase.csv

