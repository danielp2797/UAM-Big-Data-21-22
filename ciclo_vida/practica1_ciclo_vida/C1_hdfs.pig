%DECLARE input 'hdfs:///hadoop/dataset/athleteEvents.csv';
%DECLARE output 'hdfs:///hadoop/out/C1';

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

medallas_oro = FILTER atletas BY Medal == 'Gold';

edad_minima = FOREACH (GROUP medallas_oro ALL)
        GENERATE MIN(medallas_oro.Age) AS valor:int;

medallistas = FOREACH (
                FILTER medallas_oro BY (int)Age == edad_minima.valor)
                        GENERATE Name, Games, Year, Sport, Event;
DUMP medallistas;

STORE medallistas INTO '$output' USING PigStorage (',');

