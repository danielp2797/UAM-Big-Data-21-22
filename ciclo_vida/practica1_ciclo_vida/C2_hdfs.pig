%DECLARE input 'hdfs:///hadoop/dataset/athleteEvents.csv';
%DECLARE output 'hdfs:///hadoop/out/C2';

fs -rm -f -r -R $output; --Elimina el directorio salida si existe. 

atletas = LOAD '$input'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'YES_MULTILINE',
'NOCHANGE', 'SKIP_INPUT_HEADER') AS (
ID:chararray,
Name:chararray,
Sex:chararray,
Age:int,
Height:int,
Weight:int,
Team:chararray,
NOC:chararray,
Games:chararray,
Year:int,
Season:chararray,
City:chararray,
Sport:chararray,
Event:chararray,
Medal:chararray);

espanoles = FILTER atletas BY Team == 'Spain';
espanoles_ord = ORDER espanoles BY Name;
DUMP espanoles_ord;

STORE espanoles_ord INTO '$output' USING PigStorage (',');
