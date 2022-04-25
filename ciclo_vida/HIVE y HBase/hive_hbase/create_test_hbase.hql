create database hbase;
use hbase;
create external table hbase_t1(key int, col_1 int, col_2 int)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key, cf1:col_1, cf1:col_2")
TBLPROPERTIES ("hbase.table.name" = "t1", "hbase.mapred.output.outputable" = "t1");
exit;
