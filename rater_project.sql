SELECT
    g.id,
    g.title,
    AVG(r.value) AS average_rating
FROM
    raterprojectapi_game g
JOIN
    raterprojectapi_rating r ON r.game_id = g.id
GROUP BY g.title
ORDER BY average_rating DESC
LIMIT 5
