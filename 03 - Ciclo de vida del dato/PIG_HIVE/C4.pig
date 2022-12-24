--%DECLARE input 'file:////home/daniel/Downloads/athleteEvents.csv';
--%DECLARE output 'file:///home/daniel/Desktop/UAM_Msc_BigData/ciclo_vida/practica1_ciclo_vida/resultados_local/C4_local';
--%DECLARE outputoro 'file:///home/daniel/Desktop/UAM_Msc_BigData/ciclo_vida/practica1_ciclo_vida/resultados_local/C4_local_oro';

--fs -rm -f -r -R $output; --Elimina el directorio salida si existe. 
--fs -rm -f -r -R $outputoro; --Elimina el directorio salida si existe. 

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

dummies = FOREACH atletas GENERATE Name,
		(CASE WHEN Medal == 'Gold' THEN 1 ELSE 0 END) AS Gold:int,
		(CASE WHEN Medal == 'Silver' THEN 1 ELSE 0 END) AS Silver:int,
		(CASE WHEN Medal == 'Bronze' THEN 1 ELSE 0 END) AS Bronze:int;
		--(CASE WHEN Medal == 'NA' THEN 1 ELSE 0 END) AS NA:int;

dummies_group = GROUP dummies BY Name;
dummies_count = FOREACH dummies_group GENERATE group as Name,
			SUM(dummies.Gold) AS Medallas_oro:int,
			SUM(dummies.Silver) AS Medallas_plata:int,
			SUM(dummies.Bronze) AS Medallas_bronce:int;
			--SUM(dummies.NA) AS Medallas_NA:int;
			
total_medallas = FOREACH dummies_count GENERATE Name, Medallas_oro, Medallas_plata, Medallas_bronce, --Medallas_NA,
	(Medallas_oro+Medallas_plata+Medallas_bronce) AS Total;
	--(Medallas_oro+Medallas_plata+Medallas_bronce+Medallas_NA) AS Total_NA;

max_medallas = FOREACH (GROUP total_medallas ALL)
        GENERATE MAX(total_medallas.Total) AS valor:int;

max_medallas_oro = FOREACH (GROUP total_medallas ALL)
        GENERATE MAX(total_medallas.Medallas_oro) AS valor:int;
        
mejores = FOREACH (
                FILTER total_medallas BY Total == max_medallas.valor)
                        GENERATE Name, Medallas_oro, Medallas_plata, Medallas_bronce;
mejores_oro = FOREACH (
                FILTER total_medallas BY Medallas_oro == max_medallas_oro.valor)
                        GENERATE Name, Medallas_oro, Medallas_plata, Medallas_bronce;
DUMP mejores;
DUMP mejores_oro;	

--STORE mejores INTO '$output' USING PigStorage (',');
--STORE mejores_oro INTO '$outputoro' USING PigStorage (',');		

-----------------------------------------------------------------------
-- MAS MEDALLAS DE ORO EN LA HISOTRIA DE LOS JUEGOS OLIMPICOS







