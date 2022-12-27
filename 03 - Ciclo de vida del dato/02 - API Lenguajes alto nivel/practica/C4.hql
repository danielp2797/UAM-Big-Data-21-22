DROP TABLE IF EXISTS resuls_P1_pighive.C4_mejores;
DROP TABLE IF EXISTS resuls_P1_pighive.C4_mejores_oro;

-- tabla auxiliar para contar las medallas de cada atleta
CREATE TEMPORARY TABLE recuento_medallas AS
SELECT Name,
SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END)  AS Gold,
SUM(CASE WHEN Medal = 'Silver' THEN 1 ELSE 0 END) AS Silver,
SUM(CASE WHEN Medal = 'Bronze' THEN 1 ELSE 0 END) AS Bronze
FROM practicas.atletas
GROUP BY Name;

-- tabla auxiliar para contar el total de medallas por atleta
CREATE TEMPORARY TABLE recuento_medallas_total AS
SELECT *, Gold+Silver+Bronze AS Total FROM recuento_medallas;

-- Mejores segun medallas de Oro
CREATE TABLE resuls_P1_pighive.C4_mejores_oro
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' AS

SELECT Name, Gold FROM recuento_medallas WHERE Gold IN (SELECT MAX(Gold) FROM recuento_medallas);

-- Mejores segun total de medallas
CREATE TABLE resuls_P1_pighive.C4_mejores
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' AS
SELECT Name, Total FROM recuento_medallas_total WHERE Total IN (SELECT MAX(Total) FROM recuento_medallas_total);

-- se borran las auxiliares
DROP TABLE recuento_medallas;
DROP TABLE recuento_medallas_total;
