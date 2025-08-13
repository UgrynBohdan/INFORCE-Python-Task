Auth

POST /api/auth/login/ — отримання JWT токена

POST /api/auth/register/ — створення користувача

token/refresh/

Restaurants

POST /api/restaurants/ — створення ресторану

POST /api/restaurants/{id}/menu/ — додавання меню на день

GET /api/restaurants/menu/today/ — отримати меню на сьогодні

Votes

POST /api/votes/ — голосування за меню

GET /api/votes/results/today/ — результати голосування на сьогодні

docker tag inforce_python_task4-web:latest ugrynbogdan/inforce_task-web:latest
