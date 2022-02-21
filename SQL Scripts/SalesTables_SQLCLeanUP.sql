DROP DATABASE IF EXISTS VGSales;
CREATE DATABASE VGSales;
USE VGSales;

CREATE TABLE ConsoleSales (
    Console_Rank INT NOT NULL AUTO_INCREMENT,
    Platform VARCHAR(255) NOT NULL,
    Console_Type VARCHAR(255) NOT NULL,
    Firm VARCHAR(255) NOT NULL,
    Release_Year INT NOT NULL,
    Units_Sold_in_Millions DECIMAL(10,2)
,
    PRIMARY KEY (Console_Rank)
);

LOAD DATA INFILE '[FILE LOCATION]' 
INTO TABLE ConsoleSales
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

    
DROP TABLE IF EXISTS GameSales;
CREATE TABLE GameSales (
    Game_Rank INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Platform VARCHAR(255) NOT NULL,
    Publisher VARCHAR(255) NOT NULL,
    Developer VARCHAR(255) NOT NULL,
    Critic_Score DECIMAL(10 , 1 ),
    Global_Sales DECIMAL(10 , 3 ),
    NA_Sales DECIMAL(10 , 3 ) ,
    EU_Sales DECIMAL(10 , 3 ) ,
    JP_Sales DECIMAL(10 , 3 ) ,
    Other_Sales DECIMAL(10 , 3 ),
    Release_Date VARCHAR(255) NOT NULL,
    PRIMARY KEY (Game_Rank)
);

LOAD DATA INFILE '[FILE LOCATION]' 
IGNORE INTO TABLE GameSales
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

UPDATE consolesales # Console Sales table is updated so that it has matching values to the Game Sales table for the Platform column
SET 
    Platform = REPLACE(Platform, 'PlayStation ', 'PS'),
    Platform = REPLACE(Platform,'Nintendo DS family', 'DS'),
    Platform = REPLACE(Platform, 'Game Boy Advance family', 'GBA'),
    Platform = REPLACE(Platform, 'Game Boy', 'GB'),
    Platform = REPLACE(Platform, 'PSPortable', 'PSP'),
    Platform = REPLACE(Platform, 'Nintendo 3DS family', '3DS'),
    Platform = REPLACE(Platform, 'Xbox 360', 'X360'),
    Platform = REPLACE(Platform, 'Xbox One', 'XOne'),
    Platform = REPLACE(Platform, 'Nintendo Switch', 'NS'),
    Platform = REPLACE(Platform, '(console)', ''),
    Platform = REPLACE(Platform, 'Xbox', 'XB'),
	Platform = REPLACE(Platform, 'Super Nintendo Entertainment System', 'SNES'),
	Platform = REPLACE(Platform, 'Nintendo Entertainment System', 'NES'),
    Platform = REPLACE(Platform, 'GameCube', 'GC'),
    Platform = REPLACE(Platform, 'Wii U', 'WiiU'),
    Platform = REPLACE(Platform, 'Dreamcast', 'DC'),
    Platform = REPLACE(Platform, 'Nintendo 64', 'N64');
    
UPDATE gamesales # Game Sales table is updated so the Release Date column is properly displayed as a date.
SET 
    Release_Date = REPLACE(Release_Date, 'th', ''),
    Release_Date = REPLACE(Release_Date, 'rd', ''),
    Release_Date = REPLACE(Release_Date, 'st', ''),
    Release_Date = REPLACE(Release_Date, 'nd', ''),
    Release_Date = REPLACE(Release_Date, ' ', '-'),
    Release_Date = str_to_date( Release_Date, '%d-%M-%y' );

alter table gamesales modify column Release_Date DATE;



    
