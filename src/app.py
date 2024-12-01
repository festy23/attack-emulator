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
    report = ""

    if attack_type == "SQL Injection":
        report = {
            "title": "SQL Injection",
            "description": "Эта атака позволяет злоумышленнику манипулировать SQL-запросами для доступа к базе данных.",
            "example": "SELECT * FROM users WHERE username='admin'--'"
        }
    elif attack_type == "XSS":
        report = {
            "title": "Cross-Site Scripting (XSS)",
            "description": "Эта атака позволяет внедрять вредоносные скрипты в веб-страницу.",
            "example": "<script>alert('XSS!');</script>"
        }
    elif attack_type == "DDoS":
        report = {
            "title": "DDoS Attack",
            "description": "Эта атака направлена на перегрузку сервера множеством запросов.",
            "example": "Тысячи запросов в секунду от ботнетов."
        }
    else:
        flash("Неизвестный тип атаки.")
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

if __name__ == '__main__':
    app.run(debug=True)