SELECT 
  g.title,
  g.age_recommendation
FROM raterprojectapi_game g
WHERE g.age_recommendation < 8
