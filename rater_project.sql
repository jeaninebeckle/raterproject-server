SELECT COUNT(u.username), u.username
FROM raterprojectapi_review r
JOIN raterprojectapi_game g ON r.game_id = g.id
JOIN raterprojectapi_player p ON r.player_id = p.id
JOIN auth_user u ON p.user_id = u.id
GROUP BY player_id
ORDER BY COUNT(u.username) DESC
