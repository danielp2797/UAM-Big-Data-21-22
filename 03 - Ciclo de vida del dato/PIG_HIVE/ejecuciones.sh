#!usr/bin/bash

hdfs dfs -put $1 'hdfs:///hadoop/dataset/athleteEvents.csv'

rm -rf metastore_db #elimina metastore actual
schematool -dbType derby -initSchema #levanta el servicio Derby

#----------------------------------------------
#------ Consultas Pig local -------------------
#----------------------------------------------
pig -x local -f C1.pig -param input=$1
pig -x local -f C2.pig -param input=$1
pig -x local -f C3.pig -param input=$1
pig -x local -f C4.pig -param input=$1

#---------------------------------------------
#------ Consultas Pig mapreduce----------------
#----------------------------------------------

pig C1_hdfs.pig
pig C2_hdfs.pig
pig C3_hdfs.pig
pig C4_hdfs.pig
#----------------------------------------------

#----------------------------------------------
#------ Consultas Hive -------------------
#----------------------------------------------

hdfs dfs -put $1 'hdfs:///hadoop/dataset/athleteEvents.csv'

hive -f BD_practicas.hql
hive -f C1.hql
hive -f C2.hql
hive -f C3.hql
hive -f C4.hql
