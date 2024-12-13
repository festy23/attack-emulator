import sys
import os


import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from app import app  
@pytest.fixture
def client():
    """Создаёт тестовый клиент Flask для отправки запросов."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Тестирует главную страницу."""
    response = client.get('/')
    assert response.status_code == 200
    assert "Моделирование атак и защит".encode('utf-8') in response.data
    print(response.data.decode('utf-8'))

def test_xss_demo_post(client):
    """Тестирует POST-запрос к маршруту XSS Demo."""
    response = client.post('/xss_demo', data={'user_input': '<script>alert("XSS")</script>'})
    assert response.status_code == 200
    assert "Демонстрация XSS".encode('UTF-8') in response.data  
def test_sql_demo_post(client):
    """Тестирует POST-запрос к маршруту SQL Demo."""
    response = client.post('/sql_demo', data={'username': 'admin', 'password': 'P@ssw0rd123'})
    assert response.status_code == 200
    assert b"admin" in response.data

def test_ddos_demo(client):
    """Тестирует маршрут DDoS Demo."""
    response = client.post('/ddos_demo')
    assert response.status_code == 200
    assert "Демонстрация DDoS".encode('utf-8') in response.data  

def test_attack_report(client):
    """Тестирует отчёт об атаках."""
    response = client.get('/attack_report?attack_type=XSS')
    assert response.status_code == 200
    assert "Отчёт об атаке: XSS".encode('utf-8') in response.data
    assert "Внедрение JavaScript-кода, выполняемого в браузере пользователя.".encode('utf-8') in response.data
    assert "Кража данных или подмена интерфейса.".encode('utf-8') in response.data
def test_defense_report(client):
    """Тестирует отчёт о защите."""
    response = client.get('/defense_report?defense_type=Prepared Statements')
    assert response.status_code == 200
    assert b"Prepared Statements" in response.data

def test_test_page(client):
    """Тестирует маршрут теста /test."""
    # Проверяем доступность страницы (GET-запрос)
    response = client.get('/test')
    assert response.status_code == 200
    assert "Что является основным последствием DDoS-атаки?".encode('utf-8') in response.data  # Проверяем текст вопроса

def test_test_submission(client):
    """Тестирует отправку ответов на вопросы /test."""
   
    answers = {
        'q0': "Перегрузка сервера",
        'q1': 'Подготовленные запросы(Prepared Statements)',
        'q2': "Input Data Filtering",
        'q3': "10",
        'q4': "Rate Limiting"
    }

 
    response = client.post('/test', data=answers)
    assert response.status_code == 200
    assert "Ваш результат: 5/5".encode('utf-8') in response.data  


    assert "Основной целью DDoS-атаки является перегрузка сервера для нарушения его работы.".encode('utf-8') in response.data