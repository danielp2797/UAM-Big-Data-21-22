DROP TABLE IF EXISTS resuls_P1_pighive.C1;

CREATE TABLE resuls_P1_pighive.C1
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' AS
SELECT name, age, year, games, sport, event FROM practicas.atletas WHERE Age IN 
	(
	SELECT MIN(Age) FROM practicas.atletas WHERE Medal = 'Gold'
	) AND Medal = 'Gold';

