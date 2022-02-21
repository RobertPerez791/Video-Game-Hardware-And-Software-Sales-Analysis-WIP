SELECT # Generates updated Game Sales chart, with properly formatted dates
    *
FROM
    gamesales;
    
SELECT # Generates updated Console Sales chart, with Platform column values matched to Game Sales table.
    *
FROM
    consolesales;

SELECT # Generates a table displaying best selling game on each platform
    gs.Name,
    gs.Platform,
    MAX(Global_Sales),
    Units_Sold_in_Millions AS Platform_Sales_in_Millions
FROM
    gamesales gs
        JOIN
    consolesales cs ON cs.Platform = gs.Platform
GROUP BY Platform
ORDER BY Units_sold_in_Millions DESC;