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

    return render_template('attack_report.html', report=report)

# Выполнение защиты
@app.route('/defense', methods=['POST'])
def defense():
    action = request.form.get('action')  # Узнаем, что пользователь хочет сделать
    if action == "enable":
        defense_type = request.form.get('defense_type')
        if defense_type == "Prepared Statements":
            session['active_defense'] = "Prepared Statements"
            flash("Защита 'Prepared Statements' включена!")
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
    # Отчёт об атаке
    report = {
        "title": "Отчёт об атаке: SQL Injection",
        "description": "Эта атака позволяет злоумышленнику манипулировать SQL-запросами.",
        "query": "SELECT * FROM users WHERE username='admin'-- AND password=''",
        "impact": "Атакующий получил доступ к конфиденциальным данным.",
        "prevention": [
            "Используйте подготовленные выражения (Prepared Statements).",
            "Экранируйте пользовательский ввод.",
            "Применяйте ORM для работы с базой данных.",
        ]
    }
    return render_template('attack_report.html', report=report)

@app.route('/defense_report')
def defense_report():
    # Отчёт о защите
    report = {
        "title": "Отчёт о защите: Prepared Statements",
        "description": "Prepared Statements предотвращают SQL-инъекции, изолируя пользовательский ввод от структуры SQL-запроса.",
        "example": "SELECT * FROM users WHERE username=? AND password=?",
        "impact": "SQL-инъекция была успешно заблокирована.",
        "how_it_works": [
            "Вводимые данные передаются как параметры запроса.",
            "SQL-запросы и данные обрабатываются раздельно.",
            "Попытки манипуляции запросами игнорируются."
        ]
    }
    return render_template('defense_report.html', report=report)
if __name__ == '__main__':
    app.run(debug=True)