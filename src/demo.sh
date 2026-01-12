#!/bin/bash


echo 'curl -d "model_name=Qwen3-Coder-480B-A35B-Instruct&user_question=how many file does Guiness Penelope acted?" http://localhost:5000/text2sql/sql'
echo ''
curl -d "model_name=Qwen3-Coder-480B-A35B-Instruct&user_question=how many file does Guiness Penelope acted?" http://localhost:5000/text2sql/sql
# ---------------------

echo '-------------------------------------------------'
# echo ''
echo 'curl -d "sql=SELECT COUNT(f.film_id) FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE a.last_name = 'Guiness' AND a.first_name = 'Penelope';" http://localhost:5000/text2sql/exec'
echo ''
curl -d "sql=SELECT COUNT(f.film_id) FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE a.last_name = 'Guiness' AND a.first_name = 'Penelope';" http://localhost:5000/text2sql/exec
# -----------------

echo '-------------------------------------------------'
# echo ''
echo 'curl -d "model_name=Qwen3-Coder-480B-A35B-Instruct&user_question=how many file does Guiness Penelope acted?&sql=SELECT COUNT(f.film_id) FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE a.last_name = 'Guiness' AND a.first
_name = 'Penelope';&query_result=[[19]]" http://localhost:5000/text2sql/insight'
echo ''
curl -d "model_name=Qwen3-Coder-480B-A35B-Instruct&user_question=how many file does Guiness Penelope acted?&sql=SELECT COUNT(f.film_id) FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE a.last_name = 'Guiness' AND a.first
_name = 'Penelope';&query_result=[[19]]" http://localhost:5000/text2sql/insight