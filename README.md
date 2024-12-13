## **Эмулятор атак на веб-приложение**



## **Описание проекта**

Эмулятор атак на веб-приложения, включая DDoS, SQL Injection и XSS, c демонстрацией методов защиты. Позволяет пользователям изучить принципы атак и их предотвращения через интерактивный интерфейс.


        **Эмуляция популярных атак**:
    
    •    DDoS: Перегрузка сервера запросами.
    •    SQL Injection: Внедрение вредоносных SQL-запросов.
    •    XSS: Исполнение JavaScript-кода через пользовательский ввод.
    
       ** Методы защиты**:
    
    •    Ограничение запросов (Rate Limiting).
    •    Подготовленные SQL-выражения (Prepared Statements).
    •    Экранирование данных для предотвращения XSS.
    •    Генерация отчётов об атаках и методах защиты.
    •    Тестирование знаний через интерактивный опрос.

## **Установка**

    1. **Склонируйте репозиторий**:
       git clone https://github.com/Ye2312/attack-emulator.git
       cd attack-emulator

    2. **Установите зависимости**:
       pip install -r requirements.txt

## **Запуск приложения**

    1. **Запустите приложение через консоль Python**.

    2. **Откройте ссылку http://127.0.0.1:5001 **.

## **Запуск тестов**

    1. Запустите тесты через pytest в корневой папке проекта:
          pytest



## **Структура проекта**

    •    src/: 
              app.py: основной файл приложения.
              templates/: HTML-шаблоны для маршрутов.
                            index.html: главная страница.
                            attack_report.html: отчёт об атаке.
                            defense_report.html: отчёт о защите.
                            ddos_demo.html: демонстрация DDoS.
                            sql_demo.html: демонстрация SQL Injection.
                            xss_demo.html: демонстрация XSS.
                            test.html: тестирование знаний.
    •    tests/: тесты маршрутов.
    •    docs/:
              build: части документации
              source: части документации
              requirements.txt: список зависимостей.
              README.md: руководство пользователя.
              
## **Пример использования**
    1. Запустите приложение.
    2.    Выберите атаку на главной странице:
           •    DDoS: отправьте несколько запросов, чтобы перегрузить сервер.
           •    SQL Injection: протестируйте уязвимости базы данных через SQL-запросы.
           •    XSS: внедрите скрипт через пользовательский ввод.
    3.    Включите защиту, подходящую для выбранной атаки.
    4.    Повторите атаку, чтобы увидеть, как защита её блокирует.
    5.    Ознакомьтесь с отчётами об атаке и методах защиты.
    6.    Пройдите тест для проверки понимания атак и защит.

