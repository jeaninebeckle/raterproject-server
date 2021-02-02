SELECT 
  c.label,
  COUNT(g.title)
FROM raterprojectapi_categories c
JOIN 
  raterprojectapi_game_categories gc on gc.categories_id = c.id
JOIN 
  raterprojectapi_game g on gc.game_id = g.id
GROUP BY c.label
