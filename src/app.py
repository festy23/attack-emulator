from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key2312'
active_defense = None  # Переменная для отслеживания включенной защиты
request_count = 0
app.jinja_env.globals.update(enumerate=enumerate)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Главная страница
@app.route('/')
def home(): 
    global request_count
    request_count=0 
    return render_template('index.html')

# Выполнение атаки
@app.route('/attack', methods=['POST'])
def attack():
    attack_type = request.form.get('attack_type')

    # Переход на страницу конкретной атаки
    if attack_type == "SQL Injection":
        return redirect(url_for('sql_demo'))
    elif attack_type == "XSS":
        return redirect(url_for('xss_demo'))
    elif attack_type == "DDoS":
        return redirect(url_for('ddos_demo'))
    else:
        flash("Выберите корректную атаку.")
        return redirect(url_for('home'))

   

# Выполнение защиты
@app.route('/defense', methods=['POST'])
def defense():
    action = request.form.get('action')  # Узнаём, что нужно сделать
    defense_type = request.form.get('defense_type')  # Тип защиты

    if action == "enable":
        session['active_defense'] = defense_type
        flash(f"Защита '{defense_type}' включена!", "success")
        # Перенаправляем в зависимости от типа защиты
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


#SQL иньекция
@app.route('/sql_demo', methods=['GET', 'POST'])
def sql_demo():
    # Фейковая база данных
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

    # Инициализация переменных
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
            # Проверяем защищённый вход
            for row in fake_db:
                if row["username"] == username and row["password"] == password:
                    result = f"Добро пожаловать, {username}!"
                    break
            else:
                result = "Доступ запрещён!"
                query = "SELECT * FROM users WHERE username=? AND password=?"
            show_defense_report = True  # Показываем кнопку для отчёта о защите
            
        else:
            # Уязвимый SQL-запрос
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            if "'--" in username or "OR" in username:
                result = "Вы украли данные из базы!"
                stolen_data = fake_db
                show_attack_report = True  # Показываем кнопку для отчёта об атаке
                
            else:
                for row in fake_db:
                    if row["username"] == username and row["password"] == password:
                        result = f"Добро пожаловать, {username}!"
                        break
                else:
                    result = "Доступ запрещён!"

    # Возвращаем шаблон для GET и POST запросов
    return render_template(
        'sql_demo.html',
        result=result,
        query=query,
        active_defense=active_defense,
        stolen_data=stolen_data,
        
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report
    )

@app.route('/attack_report', methods=['GET'])
def attack_report():
    attack_type = request.args.get('attack_type', 'Unknown')
    report = {
        "title": f"Отчёт об атаке: {attack_type}",
        "description": f"Атака типа {attack_type} имеет уникальный характер воздействия на систему.",
        "example": {
            "DDoS": "Перегрузка сервера за счёт большого числа запросов.",
            "SQL Injection": "Выполнение вредоносных SQL-запросов через вводимые данные.",
            "XSS": "Внедрение JavaScript-кода, выполняемого в браузере пользователя."
        }.get(attack_type, "Пример не предоставлен."),
        "impact": {
            "DDoS": "Сервер становится недоступным для пользователей.",
            "SQL Injection": "Компрометация данных и нарушение работы базы данных.",
            "XSS": "Кража данных пользователей или подмена интерфейса."
        }.get(attack_type, "Описание последствий отсутствует."),
        "how_it_works": {
            "DDoS": ["Генерация огромного числа запросов", "Перегрузка серверных ресурсов", "Блокировка доступа к ресурсу"],
            "SQL Injection": ["Использование неэкранированных данных", "Внедрение вредоносных запросов в SQL"],
            "XSS": ["Фильтрация данных", "Экранирование пользовательских данных"]
        }.get(attack_type, ["Описание отсутствует."]),
    }
    return render_template('attack_report.html', report=report) 


@app.route('/defense_report', methods=['GET'])
def defense_report():
    defense_type = request.args.get('defense_type', 'Unknown')
    report = {
        "title": f"Отчёт о защите: {defense_type}",
        "description": f"Механизм защиты {defense_type} обеспечивает защиту от определённых типов атак.",
        "example": {
            "Rate Limiting": "Ограничение кол-ва запросов на основе частоты.",
            "Prepared Statements": "Безопасное выполнение SQL-запросов.",
            "Input Data Filtering": "Экранирование пользовательских данных."
        }.get(defense_type, "Пример не предоставлен."),
        "impact": f"Активная защита {defense_type} может существенно снизить риск успешной атаки.",
        "how_it_works": {
            "DDoS Protection": ["Ограничение запросов", "Анализ трафика", "Блокировка IP-адресов"],
            "Prepared Statements": ["Экранирование данных", "Использование параметризованных запросов"],
            "XSS Protection": ["Фильтрация данных", "Установка CSP"]
        }.get(defense_type, ["Описание отсутствует."])
    }
    return render_template('defense_report.html', report=report)

#XSS attack
@app.route('/xss_demo', methods=['GET', 'POST'])
def xss_demo():
    result = ""
    active_defense = session.get('active_defense', None)  # Проверяем активную защиту
    show_attack_report = False
    show_defense_report = False
    executed_query=""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        executed_query = f"Отображённый скрипт: {user_input}"
   

        if active_defense == "XSS Protection":
            # Защищённая версия: экранирование пользовательского ввода
            safe_input = user_input.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
            result = f"Ваш ввод был обработан: {safe_input}"
            show_defense_report = True
        else:
            # Уязвимая версия: ввод отображается без фильтрации
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


#DDos
@app.route('/ddos_demo', methods=['GET', 'POST'])
def ddos_demo():
    global request_count
    active_defense = session.get('active_defense')  # Получаем состояние защиты
    show_attack_report = False
    show_defense_report = False

    if request.method == 'POST':
        request_count += 1  # Увеличиваем счётчик запросов

    # Проверка успешности атаки
    if active_defense == "DDoS Protection":
        if request_count >= 10:
            attack_successful = False  # Защита блокирует атаку
            show_defense_report = True
        else:
            attack_successful = None  # Атака ещё не достигла лимита запросов
    else:
        attack_successful = True if request_count >= 10 else None  # Если защита отключена
        if attack_successful:
            show_attack_report = True

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
    questions = [
        
    {
        "question": "Что является основным последствием DDoS-атаки?",
        "options": ["Кража данных", "Перегрузка сервера", "Изменение интерфейса"],
        "answer": "Перегрузка сервера",
        "explanation": "Основной целью DDoS-атаки является перегрузка сервера для нарушения его работы."
    },
    {
        "question": "Какой метод защиты используется против SQL Injection?",
        "options": ["Фильтрация IP-адресов", "Prepared Statements", "Ограничение запросов"],
        "answer": "Prepared Statements",
        "explanation": "Prepared Statements - подготовленные шаблоны запросов защищают базы данных, предотвращая выполнение вредоносных SQL-запросов."
    },
    {
        "question": "Как работает защита от XSS?",
        "options":["Input Data Filtering", "Фильтрация трафика", "Блокировка IP-адресов"],
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
        user_answers = request.form  # Получаем ответы пользователя
        score = 0

        # Проверяем ответы
        for i, question in enumerate(questions):
            if user_answers.get(f"q{i}") == question["answer"]:
                score += 1

        

    return render_template('test.html', questions=questions,user_answers=user_answers,score=score)


if __name__ == '__main__':
    app.run(debug=True)

