from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/attack',methods=['POST'])
def attack():
    attack_type = request.form.get('attack_type')

    if attack_type == "SQL Injection":
       flash("SQL Injection выполнена! ()")
    elif attack_type == "XSS":
       flash("XSS атака выполнена! ()")
    elif attack_type == "Brute Force":
       flash("Brute Force атака выполнена! ()")
    else:
       flash("Неизвестный тип атаки.")

    return redirect(url_for('home'))


@app.route('/defense',methods=['POST'])
def defense():
    defense_type = request.form.get('defense_type')

    if defense_type == "Prepared Statements":
       flash("Защита с помощью Prepared Statements включена!")
    elif defense_type == "Sanitization":
       flash("Защита с помощью Sanitization включена!")
    elif defense_type == "Brute Force protection":
       flash("Защита от Brute Force включена!")
    else:
       flash("Неизвестный тип защиты.")


if __name__ == '__main__':
    app.run(debug=True) 