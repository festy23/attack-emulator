
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key23'
active_defense = None 
request_count = None
app.jinja_env.globals.update(enumerate=enumerate)
app.config['TEMPLATES_AUTO_RELOAD'] = True



@app.route('/')
def home(): 
    """
    Главная страница.

    Сбрасывает счётчик запросов для DDoS атаки.

    Глобальные переменные:
        request_count (int): Счётчик запросов для симуляции DDoS.

    Returns:
        str: Рендерит шаблон index.html.
    """
    global request_count
    request_count=0 
    return render_template('index.html')


@app.route('/attack', methods=['POST'])
def attack():
    """
    Страница для выбора типа атаки.

    Перенаправляет на страницы с демонстрациями различных атак.

    Аргументы формы:
        attack_type (str): Тип выбранной атаки. Возможные значения:
            - "SQL Injection"
            - "XSS"
            - "DDoS"

    Returns:
        redirect: Перенаправление на страницы с демонстрацией атак.
    """
    attack_type = request.form.get('attack_type')

  
    if attack_type == "SQL Injection":
        return redirect(url_for('sql_demo'))
    elif attack_type == "XSS":
        return redirect(url_for('xss_demo'))
    elif attack_type == "DDoS":
        return redirect(url_for('ddos_demo'))
    else:
        flash("Выберите корректную атаку.")
        return redirect(url_for('home'))

   


@app.route('/defense', methods=['POST'])
def defense():
    """
    Управление защитой.

    Обрабатывает включение или отключение выбранного типа защиты.

    Аргументы формы:
        action (str): Действие, которое необходимо выполнить. Возможные значения:
            - "enable"
            - "disable"
        defense_type (str): Тип включаемой защиты. Возможные значения:
            - "Rate limiting"
            - "Prepared Statements"
            - "Input Data Filtering"

    Глобальные переменные:
        active_defense (str): Текущий активный метод защиты.

    Returns:
        redirect: Перенаправление на главную страницу.
    """
    action = request.form.get('action') 
    defense_type = request.form.get('defense_type') 

    if action == "enable":
        session['active_defense'] = defense_type
        flash(f"Защита '{defense_type}' включена!", "success")
        
        if defense_type == "Rate limiting":
            return redirect('/')
        elif defense_type == "Prepared Statements":
            return redirect('/')
        elif defense_type == "Input Data Filtering":
            return redirect('/')
    elif action == "disable":
        session['active_defense'] = None
        flash("Защита отключена.", "danger")
        return redirect('/')

    return redirect('/')



@app.route('/sql_demo', methods=['GET', 'POST'])
def sql_demo():
    """
    Демонстрация SQL-инъекций.

    Симулирует SQL-инъекцию с использованием фейковой базы данных и 
    защищённых/не защищённых методов выполнения запросов.

    Аргументы формы (POST):
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Глобальные переменные:
        active_defense (str): Текущий активный метод защиты.

    Returns:
        str: Рендерит шаблон sql_demo.html с результатами.
    """
   
    fake_db = [
             {"username": "admin", "password": "P@ssw0rd123", "role": "Administrator", "email": "admin@example.com"},
             {"username": "user1", "password": "mypassword1", "role": "User", "email": "user1@example.com"},
             {"username": "hacker", "password": "hacktheplanet", "role": "User", "email": "hacker@anonymous.com"},
             {"username": "alice", "password": "alice_in_wonderland", "role": "User", "email": "alice@example.com"},
             {"username": "bob", "password": "bob_secure_pass", "role": "Moderator", "email": "bob@example.com"},
             {"username": "root", "password": "toor", "role": "Superuser", "email": "root@localhost"},
             {"username": "guest", "password": "guest123", "role": "Guest", "email": "guest@example.com"},
             {"username": "test_user", "password": "test1234", "role": "Tester", "email": "test_user@example.com"},
             {"username": "admin2", "password": "Adm1n$$2023", "role": "Administrator", "email": "admin2@example.com"},
             {"username": "john", "password": "johns_password", "role": "User", "email": "john@example.com"},
             {"username": "eve", "password": "eve_12345", "role": "Guest", "email": "eve@secure.com"},
             {"username": "developer", "password": "dev@123", "role": "Developer", "email": "dev@example.com"},
]

    
    result = ""
    query = ""
    stolen_data = []
    show_attack_report = False
    show_defense_report = False
    active_defense = session.get('active_defense', None)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if active_defense == "Prepared Statements":
           
            for row in fake_db:
                if row["username"] == username and row["password"] == password:
                    result = f"Добро пожаловать, {username}!"
                    break
            else:
                result = "Доступ запрещён!"
                query = "SELECT * FROM users WHERE username=? AND password=?"
            show_defense_report = True 
            
        else:
           
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            if "'--" in username or "OR" in username:
                result = "Вы украли данные из базы!"
                stolen_data = fake_db
                show_attack_report = True  
                
            else:
                for row in fake_db:
                    if row["username"] == username and row["password"] == password:
                        result = f"Добро пожаловать, {username}!"
                        break
                else:
                    result = "Доступ запрещён!"

    
    return render_template(
        'sql_demo.html',
        result=result,
        query=query,
        active_defense=active_defense,
        stolen_data=stolen_data,
        
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report
    )

@app.route("/attack_report", methods=["GET"])
def attack_report():
    """
    Отчёт об атаке.

    Выводит отчёт об атаке, основанный на типе атаки, переданном в URL.

    Returns:
        str: Рендерит шаблон attack_report.html с отчётом об атаке.
    """
    attack_type = request.args.get("attack_type", "Unknown")
    report = {
        "title": f"Отчёт об атаке: {attack_type}",
        "description": f"Атака типа {attack_type} имеет уникальный характер воздействия на систему.",
        "example": {
            "DDoS": "Перегрузка сервера за счёт большого числа запросов.",
            "SQL Injection": "Вредоносные SQL-запросы через пользовательский ввод.",
            "XSS": "Внедрение JavaScript-кода, выполняемого в браузере пользователя.",
        }.get(attack_type, "Пример не предоставлен."),
        "impact": {
            "DDoS": "Сервер становится недоступным из-за перегрузки.",
            "SQL Injection": "Компрометация базы данных.",
            "XSS": "Кража данных или подмена интерфейса.",
        }.get(attack_type, "Описание последствий отсутствует."),
        "how_it_works": {
            "DDoS": [
                "Массовая отправка запросов для перегрузки сервера.",
                "Исчерпание серверных ресурсов.",
            ],
            "SQL Injection": [
                "Вставка SQL-команд через уязвимый ввод.",
                "Выполнение несанкционированных операций с базой данных.",
            ],
            "XSS": [
                "Использование уязвимого пользовательского ввода.",
                "Выполнение вредоносного JavaScript-кода.",
            ],
        }.get(attack_type, ["Описание отсутствует."]),
    }
    return render_template("attack_report.html", report=report)
@app.route("/defense_report", methods=["GET"])
def defense_report():
    """
    Отчёт о защите.

    Выводит отчёт о защите, основанный на выбранном типе защиты.

    Returns:
        str: Рендерит шаблон defense_report.html с отчётом о защите.
    """
    defense_type = request.args.get("defense_type", "Unknown")
    report = {
        "title": f"Отчёт о защите: {defense_type}",
        "description": f"Механизм защиты {defense_type} обеспечивает предотвращение определённых атак.",
        "example": {
            "Rate Limiting": "Ограничение количества запросов от одного клиента.",
            "Prepared Statements": "Использование параметризованных запросов вместо прямых строк.",
            "Input Data Filtering": "Экранирование пользовательского ввода.",
        }.get(defense_type, "Пример не предоставлен."),
        "impact": f"Активная защита {defense_type} может существенно снизить риск успешной атаки.",
        "how_it_works": {
            "Rate Limiting": [
                "Анализ и ограничение количества запросов.",
                "Блокировка IP-адресов с подозрительной активностью.",
            ],
            "Prepared Statements": [
                "Замена вводимых данных параметрами запроса.",
                "Предотвращение выполнения вредоносных SQL-команд.",
            ],
            "Input Data Filtering": [
                "Экранирование входных данных.",
                "Применение Content Security Policy (CSP).",
            ],
        }.get(defense_type, ["Описание отсутствует."]),
    }
    return render_template("defense_report.html", report=report)


@app.route('/xss_demo', methods=['GET', 'POST'])
def xss_demo():
    """
    Демонстрация защиты от XSS-атак.

    Симулирует атаку XSS с фильтрацией пользовательского ввода.

    Аргументы формы (POST):
        user_input (str): Пользовательский ввод, который будет отрендерен в шаблоне.

    Глобальные переменные:
        active_defense (str): Текущий активный метод защиты.

    Возвращаемые значения:
        str: HTML-шаблон с результатами демонстрации.
    """
    result = ""
    active_defense = session.get('active_defense', None) 
    show_attack_report = False
    show_defense_report = False
    executed_query=""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        executed_query = f"Отображённый скрипт: {user_input}"
        
        if active_defense == "Input Data Filtering":

            safe_input =  (user_input.replace("<", "&lt;")  .replace(">", "&gt;") .replace('"', "&quot;") .replace("'", "&#39;"))
            result = f"Ваш ввод был обработан: {safe_input}"
            show_defense_report = True
        else:
            
            result = f"Ваш ввод: {user_input}"
            if '<script>' in user_input:
                show_attack_report = True

    return render_template(
        'xss_demo.html',
        result=result,
        active_defense=active_defense,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report
    )



@app.route('/ddos_demo', methods=['GET', 'POST'])
def ddos_demo():
    """
    Демонстрация DDoS-атаки.

    Имитация DDoS-атаки с контролем запросов.

    Глобальные переменные:
        request_count (int): Счётчик запросов.
        active_defense (str): Текущий активный метод защиты.

    Returns:
        str: HTML-шаблон с результатами демонстрации.
    """
    global request_count
    active_defense = session.get('active_defense',None) 
 
    show_attack_report = False
    show_defense_report = False
    attack_successful=None

    if request.method == 'POST':
        request_count += 1  
       
    
    if active_defense == "Rate Limiting" and request_count >= 10:
       attack_successful = False
       show_defense_report = True

    elif request_count >= 10:
        attack_successful = True
        show_attack_report = True
      
    else:
        attack_successful = None

    

    return render_template(
        'ddos_demo.html',
        request_count=request_count,
        active_defense=active_defense,
        attack_successful=attack_successful,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report
    )



@app.route('/test', methods=['GET', 'POST'])
def test():
    """
    Обработчик страницы теста на знание атак и методов защиты.

    Обеспечивает рендеринг страницы с тестом, который содержит вопросы
    о различных видах атак и защитных механизмах. Проверяет ответы пользователя
    и выводит итоговый результат.

    Questions:
        Вопросы теста с вариантами ответов, правильным ответом и пояснением:
        - "Что является основным последствием DDoS-атаки?"
        - "Какой метод защиты используется против SQL Injection?"
        - "Как работает защита от XSS?"
        - "Сколько запросов требуется для успешной DDoS-атаки (без защиты)?"
        - "Какой метод используется для ограничения количества запросов?"

    Аргументы:
        request (werkzeug.local.LocalProxy): Flask объект запроса, содержащий данные
            о методе (GET или POST) и предоставленные пользователем данные.

    Возвращаемые значения:
        str: HTML-шаблон с результатами теста и пояснениями:
            - При методе GET: отображает вопросы теста.
            - При методе POST: проверяет ответы пользователя и отображает результат.

    Поведение:
        - Если метод запроса GET: отображает форму теста.
        - Если метод запроса POST: обрабатывает ответы пользователя, подсчитывает
          количество правильных ответов и возвращает HTML-шаблон с итоговым результатом.

    Примеры:
        Пример запроса POST с правильным ответом:
        - Вопрос: "Что является основным последствием DDoS-атаки?"
        - Ответ пользователя: "Перегрузка сервера"
        - Итог: +1 к результату.

    HTML-шаблон:
        Использует шаблон `test.html`, который отображает:
        - Список вопросов.
        - Выбранные пользователем ответы (при наличии).
        - Итоговый результат (количество правильных ответов).

    """
    questions = [
    {
        "question": "Что является основным последствием DDoS-атаки?",
        "options": ["Кража данных", "Перегрузка сервера", "Изменение интерфейса"],
        "answer": "Перегрузка сервера",
        "explanation": "Основной целью DDoS-атаки является перегрузка сервера для нарушения его работы."
    },
    {
        "question": "Какой метод защиты используется против SQL Injection?",
        "options": ["Фильтрация IP-адресов", "Подготовленные запросы(Prepared Statements)", "Ограничение запросов"],
        "answer": 'Подготовленные запросы(Prepared Statements)',
        "explanation": "Prepared Statements - подготовленные шаблоны запросов защищают базы данных, предотвращая выполнение вредоносных SQL-запросов."
    },
    {
        "question": "Как работает защита от XSS?",
        "options":["Input Data Filtering", "Двухфакторная аутефикация", "Блокировка IP-адресов"],
        "answer": "Input Data Filtering",
        "explanation": "Input Data Filtering - экранирование данных предотвращает выполнение вредоносных скриптов, внедрённых пользователем."
    },
    {
        "question": "Сколько запросов требовалось для успешной DDoS-атаки (без защиты)?",
        "options": ["5", "10", "20"],
        "answer": "10",
        "explanation": "Без защиты сервер может быть перегружен, если количество запросов превышает лимит, в данном случае — 10."
    },
    {
        "question": "Какой метод используется для ограничения количества запросов на сервер?",
        "options": ["Content Security Policy", "Rate Limiting", "SQL Prepared Statements"],
        "answer": "Rate Limiting",
        "explanation": "Rate Limiting - ограничивает частоту запросов, предотвращая перегрузку сервера."
    }
     ]
        
    user_answers={}
    score= None

    if request.method == 'POST':
        user_answers = request.form  
        score = 0

       
        for i, question in enumerate(questions):
            if user_answers.get(f"q{i}") == question["answer"]:
                score += 1

        

    return render_template('test.html', questions=questions,user_answers=user_answers,score=score)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
