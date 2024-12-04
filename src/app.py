from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key2312'

# Главная страница
@app.route('/')
def home():
    
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
    action = request.form.get('action')
    if action == "enable":
        defense_type = request.form.get('defense_type')
        if defense_type == "Prepared Statements":
            session['active_defense'] = "Prepared Statements"
            flash("Защита 'Prepared Statements' включена!")
        elif defense_type == "XSS Protection":
            session['active_defense'] = "XSS Protection"
            flash("Защита 'XSS Protection' включена!")
        elif defense_type == "Rate Limiting":
            session['active_defense'] = "Rate Limiting"
            session['request_count'] = 0  # Сбросить счётчик запросов
            flash("Защита 'Rate Limiting' включена!")
        else:
            flash("Выбранная защита пока не реализована.")
    elif action == "disable":
        session['active_defense'] = None
        flash("Защита отключена.")
    return redirect(url_for('home'))


#SQL иньекция
@app.route('/sql_demo', methods=['GET', 'POST'])
def sql_demo():
    # Фейковая база данных
    fake_db = [
        {"username": "admin", "password": "12345"},
        {"username": "user", "password": "password"},
        {"username": "artur", "password": "qwerty"},
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
    
@app.route('/attack_report')
def attack_report():
    # Получаем тип атаки из параметров URL
    attack_type = request.args.get('attack_type', 'Unknown')
    query = request.args.get('query', 'Запрос не выполнялся.')

    # Конфигурация данных для каждой атаки
    attack_details = {
        "SQL Injection": {
        
            "description": "Эта атака позволяет злоумышленнику манипулировать SQL-запросами для получения несанкционированного доступа к данным.",
            "impact": "Атакующий смог получить доступ к конфиденциальным данным.",
            "prevention": [
                "Используйте подготовленные выражения (Prepared Statements).",
                "Экранируйте пользовательский ввод.",
                "Используйте ORM-библиотеки для работы с базой данных.",
            ]
        },
        "XSS": {
           
            "description": "Cross-Site Scripting позволяет злоумышленникам внедрять вредоносные скрипты в веб-страницы.",
            "impact": "Атакующий смог выполнить вредоносный скрипт, который похитил пользовательские данные.",
            "prevention": [
                "Экранируйте пользовательский ввод.",
                "Используйте Content Security Policy (CSP).",
                "Избегайте прямого отображения непроверенных данных.",
            ]
        },
        "DDoS": {
            "title": "DDoS Attack",
             "description": "Эта атака перегружает сервер, отправляя множество запросов за короткий промежуток времени.",
            "example": "Отправка 1000 запросов за 1 секунду к одному ресурсу.",
            "impact": "Сервер перестаёт отвечать из-за перегрузки.",
            "how_it_works": [
             "Отправка большого количества запросов с одного или нескольких IP-адресов.",
            "Использование ботов для имитации легитимного трафика.",
            "Направление запросов на сервер, чтобы исчерпать его ресурсы."
             ]
        } 
    }

    # Получаем данные для отчёта или создаём пустой отчёт
    report = attack_details.get(attack_type, {
        "description": "Нет данных по данной атаке.",
        "impact": "Неизвестно.",
        "prevention": []
    })

    report["title"] = f"Отчёт об атаке: {attack_type}"
    report["query"] = query
    print("Attack type:", attack_type)
    print("Query executed:", query) 

    return render_template('attack_report.html', report=report)

@app.route('/defense_report')
def defense_report():
    defense_type = request.args.get('defense_type', 'Unknown')
    
    # Логируем для проверки
    print("Defense Type:", defense_type)

    # Конфигурация отчёта для защиты
    defense_details = {
        "Prepared Statements": {
            "title": "Отчёт о защите: Prepared statements",
            "description": "Prepared Statements предотвращают SQL-инъекции.",
            "example": "SELECT * FROM users WHERE username=? AND password=?",
            "impact": "SQL-инъекции предотвращены.",
            "how_it_works": [
                "Используются параметры вместо прямого ввода.",
                "Запросы параметризованы и экранированы."
            ],
            "defense_type": "Prepared Statements"
        },
        "XSS Protection": {
            "title": "Отчёт о защите: XSS Protection",
            "description": "Экранирование пользовательского ввода и использование Content Security Policy защищают от XSS-атак.",
            "example": "&lt;script&gt;alert('XSS')&lt;/script&gt;",
            "impact": "Вредоносные скрипты не были выполнены в браузере жертвы.",
            "how_it_works": [
                "Экранирование HTML-тегов и специальных символов.",
                "Content Security Policy предотвращает выполнение внешних скриптов."
            ],
            "defense_type": "XSS Protection"
        },
        "Rate Limiting": {
        "title": "Защита от DDoS: Rate Limiting",
        "description": "Ограничение частоты запросов от одного клиента для защиты от DDoS-атак.",
        "example": "Максимум 5 запросов в секунду от одного IP-адреса.",
        "impact": "Сервер продолжает работать, блокируя избыточные запросы.",
        "how_it_works": [
            "Отслеживание количества запросов от каждого клиента за определённое время.",
            "Блокировка запросов, превышающих установленный лимит.",
            "Использование алгоритмов, таких как Token Bucket или Leaky Bucket."
        ]
    }
    }

    # Выбираем данные для отчёта
    report = defense_details.get(defense_type, {
        "description": "Нет данных по данной защите.",
        "example": "Неизвестно.",
        "impact": "Неизвестно.",
        "how_it_works": [],
        "defense_type": "Unknown"
    })

    print("Report data:", report)  # Лог данных для проверки
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

@app.route('/ddos_demo', methods=['GET', 'POST'])
def ddos_demo():
    # Инициализация переменных
    result = ""
    show_attack_report = False
    show_defense_report = False
    active_defense = session.get('active_defense', None)

    if request.method == 'POST':
        if active_defense == "Rate Limiting":
            result = "DDoS атака заблокирована!"
            show_defense_report = True
        else:
            result = "Сервер перегружен: DDoS атака удалась!"
            show_attack_report = True

    # Убедитесь, что шаблон 'ddos_demo.html' существует
    return render_template(
        'ddos_demo.html',
        result=result,
        active_defense=active_defense,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report
    )
    








if __name__ == '__main__':
    app.run(debug=True)

