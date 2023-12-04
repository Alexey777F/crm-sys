from typing import Callable
from flask import render_template, request, redirect, flash, url_for, session
from forms import LoginForm, ClientOrder
from functools import wraps
from werkzeug.security import check_password_hash
from models import Managers, Orders, Clients, Combined
import datetime
from my_app import CreateApp

create_app = CreateApp()
app = create_app.return_app()


def set_manager_session(func: Callable) -> Callable:
    """Декоратор, который проверяет клиента в сессии и добавляет данные в шаблон"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        session.permanent = True
        if 'username' in session:
            username = session['username']
            manager_info = Managers.get_manager_info(username)
            if manager_info:
                manager_name = ' '.join(manager_info[0].split()[1:3])
                working_position = manager_info[1]
                short_name = manager_info[0].split()[1][0] + '. ' + manager_info[0].split()[0]
                return func(username=username, manager_name=manager_name, working_position=working_position,
                            short_name=short_name, *args, **kwargs)
        return redirect(url_for('login'))
    return wrapper


@app.route('/')
def index():
    """Роутер / который редиректит на login"""
    return redirect(url_for('login'), 302)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Роутер /login, который рендерит страницу login.html и при успешной проверке - редиректит на функцию main"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        # Проверяем наличие пользователя в базе данных
        manager = Managers.get_manager_username(username)
        if manager:
            if check_password_hash(manager.password, password):
                # Логин и пароль совпадают
                session['username'] = username
                return redirect(url_for('main'))
            else:
                # Пароль не совпадает
                flash("Неверный пароль")
        else:
            flash("Пользователь не найден")
    return render_template("login.html", title="Вход")


@app.route('/main', methods=["POST", "GET"])
@set_manager_session
def main(username, manager_name, working_position, short_name):
    """Роутер /main, который возвращает страницу main.html"""
    orders_by_manager = Combined.get_orders_by_manager(username)
    return render_template("main.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name,
                           orders_by_manager=orders_by_manager)


@app.route('/add_order', methods=["POST", "GET"])
@set_manager_session
def add_order(username, manager_name, working_position, short_name):
    """Роутер /add_order, который берет данные из формы и добавляет их в бд"""
    form = ClientOrder(request.form)
    if request.method == "POST" and form.validate():
        customer = request.form['customer']
        phone_number = request.form['phone_number']
        email = request.form['email']
        description = request.form['description']
        income = request.form['income']
        status = request.form['status']
        dates = datetime.datetime.now()
        manager_id = Managers.get_manager_id(username)
        client_id = Clients.get_client_id()
        order_id = Orders.get_order_id()
        Clients.add_client(customer, phone_number, email)
        Orders.add_order_by_manager(customer, description, income, status, dates, manager_id, client_id)
        Combined.add_combined(manager_id, order_id)
        return redirect(url_for('orders'))
    return render_template("add_order.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, form=form)


@app.route('/orders', methods=["POST", "GET"])
@set_manager_session
def orders(username, manager_name, working_position, short_name):
    """Роутер /orders который отображает страницу orders.html и отображает таблицу с заказами из таблицы Orders"""
    manager_id = Managers.get_manager_id(username)
    order = Orders.get_order_by_manager(manager_id)
    return render_template("orders.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, order=order)


@app.route('/clients', methods=["POST", "GET"])
@set_manager_session
def clients(username, manager_name, working_position, short_name):
    """Роутер /clients который отображает страницу clients.html и отображает таблицу с клиентами из таблицы Clients"""
    client = Clients.get_all_clients()
    return render_template("clients.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, client=client)


@app.route('/profile', methods=["POST", "GET"])
@set_manager_session
def profile(username, manager_name, working_position, short_name):
    """Роутер /profile который отображает страницу profile.html и отображает данные из таблицы Managers"""
    manager_info = Managers.get_manager_info(username)
    return render_template("profile.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, manager_info=manager_info)


@app.route('/logout')
def logout():
    """Роутер /logout который завершает сессию и редиректит на страницу входа и прохождения авторизации"""
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5140, debug=True)
