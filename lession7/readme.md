# **Домашнее задание №4. Apache Airflow**

## Подзадача №1. Запрос данных из API при помощи инструментов Airflow

Выполненная подзадача №1 Находится в папке /homework1/  https://github.com/qwerty29544/robot_dreams_data_engineering/tree/main/lession7/homework1

Файл dshop_api_dag.py - даг файл для задачи. Внутри имеется две таски:
 1. t1 - http operator для таски по запросу api token. 
В данном методе происходит post json, и ответ ключом, который пушится в xcom
 2. t2 - python operator - для таски по загрузке партиционированных по дате ответов сервера с запрашиваемыми данными. 
Файлы сохраняются в формате .json по пути, который указан в /homework1/common/config.yaml
Вся логика находится в /homework1/common/get_json_data.py

## Подзадача №2. Дамп данных из бд при помощи инструментов Airflow

Выполненная подзадача №2 Находится в папке /homework2/  https://github.com/qwerty29544/robot_dreams_data_engineering/tree/main/lession7/homework2

Файл dump_postgres_dag.py - даг файл для задачи. Внутри список тасок для каждой из таблиц в базе dshop:
 1. postgres_tasks - python operator который принимает путь к файлу и sql запрос на копирование. 
**Можно было сделать запрос и его генерацию внутри функции**.
Каждая таска отвечает за дамп своей таблицы.

Были попытки сделать всё через PostgresOperator, но я столкнулся с такой ошибкой:

psycopg2.errors.InvalidName: relative path not allowed for COPY to file

Видимо, пока я не сильно преисполнился переопределением логики операторов Airflow

Таска через питон оператор делает пулл хука по коннекшну из airflow и при помощи этого коннекшна 
дампит по COPY to STDOUT данные в файл
