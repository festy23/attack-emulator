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

    Глобальные переменные:
        request_count (int): Счётчик запросов для симуляции DDoS.

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

    Аргументы формы:
        attack_type (str): Тип выбранной атаки. Возможные значения:
            - "SQL Injection"
            - "XSS"
            - "DDoS"

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
        flash("Выберите корректную атаку.", "danger")
        return redirect(url_for("home"))

@app.route("/defense", methods=["POST"])
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
    action = request.form.get("action")
    defense_type = request.form.get("defense_type")
    if action == "enable":
        session["active_defense"] = defense_type
        flash(f"Защита '{defense_type}' включена!", "success")
    elif action == "disable":
        session["active_defense"] = None
        flash("Защита отключена.", "danger")
    return redirect("/")

@app.route("/sql_demo", methods=["GET", "POST"])
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
    Генерация отчёта об атаке.

    Генерирует отчёт об атаке на основе переданного типа атаки.

    Аргументы запроса:
        attack_type (str): Тип атаки, переданный через параметры URL.

    Returns:
        str: HTML-шаблон attack_report.html с отчётом об атаке.
    """
    attack_type = request.args.get("attack_type", "Unknown")
    report = {
        "title": f"Отчёт об атаке: {attack_type}",
        "description": f"Атака типа {attack_type} имеет уникальный характер воздействия.",
        "example": {
            "DDoS": "Массовая генерация запросов.",
            "SQL Injection": "Вредоносные SQL-запросы.",
            "XSS": "Внедрение скриптов.",
        }.get(attack_type, "Пример отсутствует."),
    }
    return render_template("attack_report.html", report=report)

@app.route("/defense_report", methods=["GET"])
def defense_report():
    """
    Генерация отчёта о защите.

    Формирует отчёт о выбранной защите.

    Аргументы запроса:
        defense_type (str): Тип защиты, переданный через параметры URL.

    Returns:
        str: HTML-шаблон defense_report.html с отчётом о защите.
    """
    defense_type = request.args.get("defense_type", "Unknown")
    report = {
        "title": f"Отчёт о защите: {defense_type}",
        "description": f"Механизм защиты {defense_type} предотвращает атаки.",
    }
    return render_template("defense_report.html", report=report)

@app.route("/ddos_demo", methods=["GET", "POST"])
def ddos_demo():
    """
    Демонстрация DDoS-атаки.

    Имитация DDoS-атаки с контролем запросов.

    Глобальные переменные:
        request_count (int): Счётчик запросов.
        active_defense (str): Текущий активный метод защиты.

    Returns:
        str: HTML-шаблон ddos_demo.html с результатами демонстрации.
    """
    global request_count
    active_defense = session.get("active_defense")
    if request.method == "POST":
        request_count += 1

    attack_successful = None
    if active_defense == "DDoS Protection" and request_count < 10:
        attack_successful = False
    elif request_count >= 10:
        attack_successful = True

    return render_template(
        "ddos_demo.html",
        request_count=request_count,
        active_defense=active_defense,
        attack_successful=attack_successful,
    )

@app.route("/xss_demo", methods=["GET", "POST"])
def xss_demo():
    """
    Демонстрация защиты от XSS-атак.

    Симулирует атаку XSS с фильтрацией пользовательского ввода.

    Аргументы формы (POST):
        user_input (str): Пользовательский ввод, который будет отрендерен в шаблоне.

    Глобальные переменные:
        active_defense (str): Текущий активный метод защиты.
    
    Returns:
        str: HTML-шаблон xxs_demo.html с результатами демонстрации.
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



if __name__ == "__main__":
    app.run(debug=True)