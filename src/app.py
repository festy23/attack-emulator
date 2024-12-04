from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key2312'
active_defense = None  # Переменная для отслеживания включенной защиты
request_count = 0
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
        if defense_type == "DDoS Protection":
            return redirect('/')
        elif defense_type == "Prepared Statements":
            return redirect('/')
        elif defense_type == "XSS Protection":
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
    
@app.route('/attack_report', methods=['GET'])
def attack_report():
    attack_type = request.args.get('attack_type', 'Unknown')
    report = {
        "title": f"Отчёт об атаке: {attack_type}",
        "description": f"Атака типа {attack_type} имеет уникальный характер воздействия на систему.",
        "impact": "Возможные последствия зависят от типа атаки. Например, сервер может стать недоступным (для DDoS), данные могут быть скомпрометированы (для SQL Injection) или нарушена работа интерфейса (для XSS).",
        "details": {
            "Тип атаки": attack_type,
            "Количество запросов (только для DDoS)": request_count if attack_type == "DDoS" else "Не применимо",
            "Результат": "Успех" if (attack_type == "DDoS" and request_count >= 10) else "Заблокирована"
        },
        "prevention": {
            "DDoS": ["Используйте защиту от DDoS", "Ограничьте количество запросов в секунду", "Фильтрация IP-адресов"],
            "SQL Injection": ["Используйте подготовленные выражения (Prepared Statements)", "Проверяйте пользовательский ввод"],
            "XSS": ["Включите защиту от XSS", "Экранируйте пользовательский ввод", "Используйте Content Security Policy (CSP)"]
        }.get(attack_type, ["Общие рекомендации по безопасности"])
    }
    return render_template('attack_report.html', report=report)


@app.route('/defense_report', methods=['GET'])
def defense_report():
    defense_type = request.args.get('defense_type', 'Unknown')
    report = {
        "title": f"Отчёт о защите: {defense_type}",
        "description": f"Механизм защиты {defense_type} обеспечивает защиту от определённых типов атак.",
        "example": {
            "DDoS Protection": "Фильтрация запросов на основе частоты.",
            "Prepared Statements": "Безопасное выполнение SQL-запросов.",
            "XSS Protection": "Экранирование пользовательских данных."
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

if __name__ == '__main__':
    app.run(debug=True)

