# welbex_testcase
 
Это решение тестового задания от компании Welbex. Выполнил Николай Петрищев. 
Решение содержит документацию в формате redoc и swagger.

Решение содержит все уровни сложности, ключая:
 - Фильтр списка грузов (вес, мили ближайших машин до грузов);
 - Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).
 - 
Работа с фильтрами(примеры):
1. Получение списка грузов по весу:
   http://127.0.0.1:8000/welbex_api/cargos/?min_weight=10&max_weight=1000
   Параметры запроса:
    - min_weight(минимальный вес);
    - max_weight(максимальный вес).
3. Получение расстояния в милях ближайших машин до грузов:
   http://127.0.0.1:8000/welbex_api/cargos/?location_zip_code=00656&max_distance=5000
   Параметры запроса:
    - location_zip_code(zip_code локации груза);
    - max_distance(максимальное расстояние от груза до машин).

Для запуска проекта необходимо выполнить следующие команды:
1. git pull https://github.com/Nikolaj-dev/welbex_testcase.git
2. python manage.py makemigrations
3. python manage.py migrate
4. python delivery_app.init_db.py
5. python manage.py runserver
6. celery -A welbex.celery worker -l info -P threads
7. celery -A welbex beat -l info
   
