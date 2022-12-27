SET input='hdfs:///hadoop/dataset/athleteEvents.csv';

CREATE DATABASE IF NOT EXISTS practicas;
CREATE DATABASE IF NOT EXISTS resuls_P1_pighive;

CREATE TABLE IF NOT EXISTS practicas.atletas (
ID int, 
Name string,
Sex string,
Age int,
Height int,
Weight int, 
Team string, 
NOC string,
Games string, 
Year int,
Season string,
City string,
Sport string,
Event string, 
Medal string 
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA INPATH ${hiveconf:input}
OVERWRITE INTO TABLE practicas.atletas;

-- Comprobacion creacion DB
SHOW DATABASES;

-- Comprobacion de la carga bde datos
SELECT * FROM practicas.atletas LIMIT 10; 
