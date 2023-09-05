from flask import render_template, request, redirect, flash, url_for, session
from forms import LoginForm, ClientOrder
from functools import wraps
from werkzeug.security import check_password_hash
from models import Managers, Orders, Clients, Combined
from config import create_app
import datetime

app, db = create_app()

def set_manager_session(func):
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
    return redirect(url_for('login'), 301)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
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
    orders_by_manager = Combined.get_orders_by_manager(username)
    return render_template("main.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, orders_by_manager=orders_by_manager)


@app.route('/add_order', methods=["POST", "GET"])
@set_manager_session
def add_order(username, manager_name, working_position, short_name):
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
        # Add client to database
        Clients.add_client(customer, phone_number, email)
        # Add order to database
        Orders.add_order_by_manager(customer, description, income, status, dates, manager_id, client_id)
        Combined.add_combined(manager_id, order_id)
        return redirect(url_for('orders'))

    return render_template("add_order.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, form=form)


@app.route('/orders', methods=["POST", "GET"])
@set_manager_session
def orders(username, manager_name, working_position, short_name):
    manager_id = Managers.get_manager_id(username)
    order = Orders.get_order_by_manager(manager_id)
    return render_template("orders.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, order=order)


@app.route('/clients', methods=["POST", "GET"])
@set_manager_session
def clients(username, manager_name, working_position, short_name):
    client = Clients.get_all_clients()
    return render_template("clients.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, client=client)


@app.route('/profile', methods=["POST", "GET"])
@set_manager_session
def profile(username, manager_name, working_position, short_name):
    manager_info = Managers.get_manager_info(username)
    return render_template("profile.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, manager_info=manager_info)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5140, debug=True)


# import smtplib
# from email.mime.text import MIMEText
#
#
# def send_mail():
#     sender = "fominb2bservice@gmail.com"
#     recipient = 'почта клиента'
#     password = "fnptltgbofcfqjcw"
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     try:
#         with open("templates/main.html") as file:
#             report = file.read()
#     except IOError:
#         return "Файл отчет не найден"
#     try:
#         server.login(sender, password)
#         msg = MIMEText(report, "html")
#         msg["FROM"] = sender
#         msg["To"] = recipient
#         msg["SUBJECT"] = "Посмотри меня!"
#         server.sendmail(sender, recipient, msg.as_string())
#         return "Успешно"
#     except Exception as ex:
#         return f"{ex} Проверь логин и пароль"
#
#
# if __name__ == "__main__":
#     send_mail()