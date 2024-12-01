from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    defense_type = request.form.get('defense_type')
    report = {}

    if defense_type == "Prepared Statements":
        report = {
            "title": "Prepared Statements",
            "description": "Подготовленные выражения защищают от SQL-инъекций.",
            "example": "SELECT * FROM users WHERE username=? AND password=?"
        }
    elif defense_type == "Sanitization":
        report = {
            "title": "Sanitization",
            "description": "Очистка пользовательского ввода защищает от XSS-атак.",
            "example": "Пример экранирования: &lt; вместо <"
        }
    elif defense_type == "Rate Limiting":
        report = {
            "title": "Rate Limiting",
            "description": "Ограничение частоты запросов защищает от DDoS-атак.",
            "example": "Максимум 5 запросов в минуту."
        }
    else:
        flash("Неизвестный тип защиты.")
        return redirect(url_for('home'))

    
    return render_template('defense_report.html', report=report)


#SQL иньекция
@app.route('/sql_demo', methods=['GET', 'POST'])
def sql_demo():
    # Фейковая база данных
    fake_db = [
        {"username": "admin", "password": "12345"},
        {"username": "user", "password": "hse"},
        {"username": "Oleg", "password": "Potato24"},
        {"username": "Diddy", "password": "2283_92xeq_oil"},
        {"username": "Vlad", "password": "123yd*__e3hx"},
        {"username": "Artur", "password": "Nex!20wjdi3u?"},
    ]
    

    result = ""
    query = ""
    stolen_data = []  # Переменная для украденных данных

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Уязвимый SQL-запрос (имитация)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(f"Выполняется SQL-запрос: {query}")

        # Логика для SQL-инъекции
        if "'1'='1" in username or "admin'" in username:
            # SQL-инъекция: возвращаем всю базу данных
            result = "Вы украли данные из базы!"
            stolen_data = fake_db
            print('Украденные данные:', stolen_data)
             # Перенаправляем на страницу отчёта
            return redirect(url_for('attack_report', attack_type="SQL Injection", query=query))
          
        else:
            # Обычная проверка пользователя
            for row in fake_db:
                if row["username"] == username and row["password"] == password:
                    result = f"Добро пожаловать, {username}!"
                    break
            else:
                result = "Доступ запрещён!"

    # Отправляем результат, запрос и украденные данные в шаблон
    return render_template('sql_demo.html', result=result, query=query, stolen_data=stolen_data)
#SQL защита
@app.route('/sql_secure_demo', methods=['GET', 'POST'])
def sql_secure_demo():
    fake_db = [
        {"username": "admin", "password": "12345"},
        {"username": "user", "password": "password"},
    ]

    result = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Безопасный подход: подготовленный запрос (симуляция)
        for row in fake_db:
            if row["username"] == username and row["password"] == password:
                result = f"Добро пожаловать, {username}!"
                break
        else:
            result = "Доступ запрещён!"

    return render_template('sql_secure_demo.html', result=result)

@app.route('/attack_report')
def attack_report():
    # Получаем тип атаки и SQL-запрос из параметров URL
    attack_type = request.args.get('attack_type', 'Unknown')
    query = request.args.get('query', '')

    # Конфигурация отчёта для каждой атаки
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
            "description": "Cross-Site Scripting позволяет внедрять вредоносные скрипты в веб-страницы, которые исполняются в браузере жертвы.",
            "impact": "Атакующий смог украсть пользовательские данные или выполнить вредоносный код.",
            "prevention": [
                "Экранируйте пользовательский ввод.",
                "Используйте Content Security Policy (CSP).",
                "Избегайте прямого отображения непроверенных данных.",
            ]
        }
    }

    # Данные отчёта
    report = attack_details.get(attack_type, {
        "description": "Нет данных по данной атаке.",
        "impact": "Неизвестно.",
        "prevention": []
    })

    report["title"] = f"Отчёт об атаке: {attack_type}"
    report["query"] = query

    print("Проверка данных отчёта:", report)  # Лог для проверки
    return render_template('attack_report.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)