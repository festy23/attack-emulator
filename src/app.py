from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key2312"
active_defense = None  # Отслеживание текущей активной защиты
request_count = 0  # Счётчик запросов для DDoS-симуляции
app.jinja_env.globals.update(enumerate=enumerate)  # Обновление глобальных переменных для jinja
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Автоматическая перезагрузка шаблонов

@app.route("/")
def home():
    """
    Главная страница.

    Сбрасывает счётчик запросов для DDoS атаки.

    Returns:
        str: Рендерит шаблон index.html.
    """
    global request_count
    request_count = 0
    return render_template("index.html")

@app.route("/attack", methods=["POST"])
def attack():
    """
    Страница для выбора типа атаки.

    Перенаправляет на страницы с демонстрациями различных атак.

    Returns:
        redirect: Перенаправление на страницы с демонстрацией атак.
    """
    attack_type = request.form.get("attack_type")
    
    if attack_type == "SQL Injection":
        return redirect(url_for("sql_demo"))
    elif attack_type == "XSS":
        return redirect(url_for("xss_demo"))
    elif attack_type == "DDoS":
        return redirect(url_for("ddos_demo"))
    else:
        flash("Выберите корректную атаку.")
        return redirect(url_for("home"))

@app.route("/defense", methods=["POST"])
def defense():
    """
    Страница для включения или отключения защиты.

    Обрабатывает включение/выключение защиты и перенаправляет на главную.

    Returns:
        redirect: Перенаправление на главную страницу.
    """
    action = request.form.get("action")  # Действие (включить или выключить защиту)
    defense_type = request.form.get("defense_type")  # Тип защиты
    if action == "enable":
        session["active_defense"] = defense_type
        flash(f"Защита '{defense_type}' включена!", "success")
        
        if defense_type == "Rate limiting":
            return redirect("/")
        elif defense_type == "Prepared Statements":
            return redirect("/")
        elif defense_type == "Input Data Filtering":
            return redirect("/")
    elif action == "disable":
        session["active_defense"] = None
        flash("Защита отключена.", "danger")
        return redirect("/")
    return redirect("/")

@app.route("/sql_demo", methods=["GET", "POST"])
def sql_demo():
    """
    Демонстрация SQL-инъекций.

    Симулирует SQL-инъекцию с использованием фейковой базы данных и 
    защищённых/не защищённых методов выполнения запросов.

    Returns:
        str: Рендерит шаблон sql_demo.html с результатами.
    """
    fake_db = [
        {"username": "admin", "password": "P@ssw0rd123", "role": "Administrator", "email": "admin@example.com"},
        {"username": "user1", "password": "mypassword1", "role": "User", "email": "user1@example.com"},
        # (И так далее для других пользователей)
    ]
    
    result = ""
    query = ""
    stolen_data = []
    show_attack_report = False
    show_defense_report = False
    active_defense = session.get("active_defense", None)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if active_defense == "Prepared Statements":
            # Защищённая версия
            for row in fake_db:
                if row["username"] == username and row["password"] == password:
                    result = f"Добро пожаловать, {username}!"
                    break
            else:
                result = "Доступ запрещён!"
                query = "SELECT * FROM users WHERE username=? AND password=?"
            show_defense_report = True  # Показываем отчёт о защите
        else:
            # Уязвимая версия
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            if "'--" in username or "OR" in username:
                result = "Вы украли данные из базы!"
                stolen_data = fake_db
                show_attack_report = True  # Показываем отчёт об атаке
            else:
                for row in fake_db:
                    if row["username"] == username and row["password"] == password:
                        result = f"Добро пожаловать, {username}!"
                        break
                else:
                    result = "Доступ запрещён!"
 
    return render_template(
        "sql_demo.html",
        result=result,
        query=query,
        active_defense=active_defense,
        stolen_data=stolen_data,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report,
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
            "SQL Injection": "Выполнение вредоносных SQL-запросов через вводимые данные.",
            "XSS": "Внедрение JavaScript-кода, выполняемого в браузере пользователя.",
        }.get(attack_type, "Пример не предоставлен."),
        "impact": {
            "DDoS": "Сервер становится недоступным для пользователей.",
            "SQL Injection": "Компрометация данных и нарушение работы базы данных.",
            "XSS": "Кража данных пользователей или подмена интерфейса.",
        }.get(attack_type, "Описание последствий отсутствует."),
        "how_it_works": {
            "DDoS": [
                "Генерация огромного числа запросов",
                "Перегрузка серверных ресурсов",
                "Блокировка доступа к ресурсу",
            ],
            "SQL Injection": [
                "Использование неэкранированных данных",
                "Внедрение вредоносных запросов в SQL",
            ],
            "XSS": [
                "Фильтрация данных",
                "Экранирование пользовательских данных",
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
        "description": f"Механизм защиты {defense_type} обеспечивает защиту от определённых типов атак.",
        "example": {
            "Rate Limiting": "Ограничение кол-ва запросов на основе частоты.",
            "Prepared Statements": "Безопасное выполнение SQL-запросов.",
            "Input Data Filtering": "Экранирование пользовательских данных.",
        }.get(defense_type, "Пример не предоставлен."),
        "impact": f"Активная защита {defense_type} может существенно снизить риск успешной атаки.",
        "how_it_works": {
            "DDoS Protection": [
                "Ограничение запросов",
                "Анализ трафика",
                "Блокировка IP-адресов",
            ],
            "Prepared Statements": [
                "Экранирование данных",
                "Использование параметризованных запросов",
            ],
            "XSS Protection": ["Фильтрация данных", "Установка CSP"],
        }.get(defense_type, ["Описание отсутствует."]),
    }
    return render_template("defense_report.html", report=report)

@app.route("/xss_demo", methods=["GET", "POST"])
def xss_demo():
    """
    Демонстрация защиты от XSS-атак.

    Симулирует атаку XSS с фильтрацией пользовательского ввода.

    Returns:
        str: Рендерит шаблон xss_demo.html с результатами.
    """
    result = ""
    active_defense = session.get("active_defense", None)
    show_attack_report = False
    show_defense_report = False
    executed_query = ""
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        executed_query = f"Отображённый скрипт: {user_input}"
        if active_defense == "XSS Protection":
            # Защищённая версия
            safe_input = (
                user_input.replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;")
            )
            result = f"Ваш ввод был обработан: {safe_input}"
            show_defense_report = True
        else:
            # Уязвимая версия
            result = f"Ваш ввод: {user_input}"
            if "<script>" in user_input:
                show_attack_report = True
    return render_template(
        "xss_demo.html",
        result=result,
        active_defense=active_defense,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report,
    )

@app.route("/ddos_demo", methods=["GET", "POST"])
def ddos_demo():
    """
    Демонстрация защиты от DDoS-атак.

    Симулирует атаку DDoS с контролем количества запросов.

    Returns:
        str: Рендерит шаблон ddos_demo.html с результатами.
    """
    global request_count
    active_defense = session.get("active_defense")
    show_attack_report = False
    show_defense_report = False
    if request.method == "POST":
        request_count += 1  

    if active_defense == "DDoS Protection":
        if request_count >= 10:
            attack_successful = False
            show_defense_report = True
        else:
            attack_successful = None
    else:
        attack_successful = True if request_count >= 10 else None
        if attack_successful:
            show_attack_report = True

    return render_template(
        "ddos_demo.html",
        request_count=request_count,
        active_defense=active_defense,
        attack_successful=attack_successful,
        show_attack_report=show_attack_report,
        show_defense_report=show_defense_report,
    )