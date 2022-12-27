DROP TABLE IF EXISTS resuls_P1_pighive.C3_sailing;
DROP TABLE IF EXISTS resuls_P1_pighive.C3_geograf;

-- tabla auxiliar para contar medallas de oro en sailing
CREATE TEMPORARY TABLE  recuento_sailing AS 
SELECT Name, COUNT(*) AS recuento FROM practicas.atletas 
WHERE Medal = 'Gold' AND Sport = 'Sailing' 
GROUP BY Medal, Name; 

CREATE TABLE resuls_P1_pighive.C3_sailing
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' AS

SELECT Name, recuento FROM recuento_sailing 
WHERE recuento IN (SELECT MAX(recuento) FROM recuento_sailing);

CREATE TABLE resuls_P1_pighive.C3_geograf
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' AS

SELECT DISTINCT Year, City, Season FROM practicas.atletas;

DROP TABLE recuento_sailing; -- borra la auxiliar
