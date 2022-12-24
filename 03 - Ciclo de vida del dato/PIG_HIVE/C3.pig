--%DECLARE input 'file:////home/daniel/Downloads/athleteEvents.csv';
--%DECLARE output 'file:///home/daniel/Desktop/UAM_Msc_BigData/ciclo_vida/practica1_ciclo_vida/resultados_local/C3_local';
--%DECLARE outputbis 'file:///home/daniel/Desktop/UAM_Msc_BigData/ciclo_vida/practica1_ciclo_vida/resultados_local/C3_local_bis';
--fs -rm -f -r -R $output; --Elimina el directorio salida si existe. 
--fs -rm -f -r -R $outputbis; --Elimina el directorio salida si existe. 

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

deportistas = FOREACH (FILTER atletas BY Sport == 'Sailing' and Medal=='Gold') GENERATE Name;
group_deportistas = GROUP deportistas BY Name;
deportistas_count = FOREACH group_deportistas GENERATE group AS Name, COUNT(deportistas) AS Medallas;

max_medallas = FOREACH (GROUP deportistas_count ALL)
        GENERATE MAX(deportistas_count.Medallas) AS valor:int;

mejores = FOREACH (
                FILTER deportistas_count BY Medallas == max_medallas.valor)
                        GENERATE Name, Medallas;
DUMP mejores;

--STORE mejores INTO '$output' USING PigStorage (',');

--------- olimpiadas por continente--------------------------------------

olimp_agrup = GROUP atletas BY (Year, Season, City);
olimpiadas = FOREACH olimp_agrup GENERATE group.Year, group.City, group.Season;

DUMP olimpiadas;

--STORE olimpiadas INTO '$outputbis' USING PigStorage (',');
