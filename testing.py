# celery version
from flask import render_template, request, redirect, flash, url_for, session
from wtforms import Form, StringField, PasswordField, validators
import os
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from db_queries.db_querie import app
from celeries.celeries import get_manager_info, get_manager_username, get_manager_id, get_client_id, get_order_id, add_client, add_order_by_manager, add_combined, get_orders_by_manager, get_order_by_manager, get_all_clients


app.secret_key = f"{os.environ.get('SECRET_KEY')}"
app.permanent_session_lifetime = datetime.timedelta(hours=10)


def set_manager_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session.permanent = True
        if 'username' in session:
            username = session['username']
            manager_info = get_manager_info.delay(username).get()
            if manager_info:
                manager_name = ' '.join(manager_info[0].split()[1:3])
                working_position = manager_info[1]
                short_name = manager_info[0].split()[1][0] + '. ' + manager_info[0].split()[0]
                return func(username=username, manager_name=manager_name, working_position=working_position,
                            short_name=short_name, *args, **kwargs)
        return redirect(url_for('login'))
    return wrapper


class LoginForm(Form):
    username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=4, max=12)])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=5, max=16)])


class ClientOrder(Form):
    customer = StringField('customer', validators=[validators.DataRequired(), validators.Length(min=7, max=40)])
    phone_number = StringField('phone_number', validators=[validators.DataRequired(), validators.Length(min=10, max=11)])
    email = StringField('email', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    description = StringField('description', validators=[validators.DataRequired(), validators.Length(min=1, max=35)])
    income = StringField('income', validators=[validators.DataRequired(), validators.Length(min=1, max=100000)])
    status = StringField('status', validators=[validators.DataRequired(), validators.Length(min=1, max=12)])


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
        manager = get_manager_username.delay(username).get()
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
    orders_by_manager = get_orders_by_manager.delay(username).get()
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
        manager_id = get_manager_id.delay(username).get()
        client_id = get_client_id.delay().get()
        order_id = get_order_id.delay().get()
        # Add client to database
        add_client(customer, phone_number, email)
        # Add order to database
        add_order_by_manager(customer, description, income, status, dates, manager_id, client_id)
        add_combined(manager_id, order_id)
        return redirect(url_for('orders'))

    return render_template("add_order.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, form=form)


@app.route('/orders', methods=["POST", "GET"])
@set_manager_session
def orders(username, manager_name, working_position, short_name):
    manager_id = get_manager_id.delay(username).get()
    order = get_order_by_manager.delay(manager_id).get()
    return render_template("orders.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, order=order)


@app.route('/clients', methods=["POST", "GET"])
@set_manager_session
def clients(username, manager_name, working_position, short_name):
    client = get_all_clients.delay().get()
    return render_template("clients.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, client=client)


@app.route('/profile', methods=["POST", "GET"])
@set_manager_session
def profile(username, manager_name, working_position, short_name):
    manager_info = get_manager_info.delay(username).get()
    return render_template("profile.html", username=username, manager_name=manager_name,
                           working_position=working_position, short_name=short_name, manager_info=manager_info)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5140, debug=True)


# WOrking version
from flask import render_template, request, redirect, flash, url_for, session
from wtforms import Form, StringField, PasswordField, validators
import os
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from db_querie import app, Managers, Orders, Clients, Combined
# from celeries import get_manager_info, get_manager_username, get_manager_id, get_client_id, get_order_id, add_client, add_order_by_manager, add_combined, get_orders_by_manager, get_order_by_manager, get_all_clients


app.secret_key = f"{os.environ.get('SECRET_KEY')}"
app.permanent_session_lifetime = datetime.timedelta(hours=10)


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


class LoginForm(Form):
    username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=4, max=12)])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=5, max=16)])


class ClientOrder(Form):
    customer = StringField('customer', validators=[validators.DataRequired(), validators.Length(min=7, max=40)])
    phone_number = StringField('phone_number', validators=[validators.DataRequired(), validators.Length(min=10, max=11)])
    email = StringField('email', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    description = StringField('description', validators=[validators.DataRequired(), validators.Length(min=1, max=35)])
    income = StringField('income', validators=[validators.DataRequired(), validators.Length(min=1, max=100000)])
    status = StringField('status', validators=[validators.DataRequired(), validators.Length(min=1, max=12)])


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
# version: "3.9"
# services:
#   postgres:
#     container_name: postgres_container
#     image: postgres:14.8-alpine3.18
#     command:
#       - "postgres"
#       - "-c"
#       - "max_connections=50"
#       - "-c"
#       - "shared_buffers=1GB"
#       - "-c"
#       - "effective_cache_size=4GB"
#       - "-c"
#       - "work_mem=16MB"
#       - "-c"
#       - "maintenance_work_mem=512MB"
#       - "-c"
#       - "random_page_cost=1.1"
#       - "-c"
#       - "temp_file_limit=10GB"
#       - "-c"
#       - "log_min_duration_statement=200ms"
#       - "-c"
#       - "idle_in_transaction_session_timeout=10s"
#       - "-c"
#       - "lock_timeout=1s"
#       - "-c"
#       - "statement_timeout=60s"
#       - "-c"
#       - "shared_preload_libraries=pg_stat_statements"
#       - "-c"
#       - "pg_stat_statements.max=10000"
#       - "-c"
#       - "pg_stat_statements.track=all"
#     environment:
#       PG_DB_HOST: "postgres"
#       POSTGRES_DB: "database"
#       POSTGRES_USER: "user"
#       POSTGRES_PASSWORD: "password"
#     volumes:
#       - db-data:/var/lib/postgresql/data
#       - ./db/postgresql/init.sql:/docker-entrypoint-initdb.d/init.sql
#     ports:
#       - "5432:5432"
#     healthcheck:
#       test: ["CMD-SHELL", "pg_isready -U user -d database"]
#       interval: 10s
#       timeout: 5s
#       retries: 5
#       start_period: 10s
#     restart: unless-stopped
#     networks:
#       - postgres
#
#   nginx:
#       container_name: nginx_container
#       image: nginx
#       ports:
#         - "443:443"
#       volumes:
#         - ./nginx/nginx.conf:/etc/nginx/conf.d/nginx.conf
#         - ./ssl:/etc/ssl
#       depends_on:
#         - app
#       restart: unless-stopped
#       networks:
#         - postgres
#
#   pgadmin:
#       container_name: pgadmin_container
#       image: dpage/pgadmin4:7.2
#       environment:
#         PGADMIN_DEFAULT_EMAIL: "pguser@gmail.com"
#         PGADMIN_DEFAULT_PASSWORD: "pgadminpwd4hr"
#         PGADMIN_CONFIG_SERVER_MODE: "False"
#       volumes:
#         - pgadmin-data:/var/lib/pgadmin
#       ports:
#         - "5050:80"
#       restart: unless-stopped
#       networks:
#         - postgres
#
#   app:
#       container_name: app_container
#       build:
#         context: ./app
#       environment:
#         SECRET_KEY: b'\xfb\xa0\xdfW"\x1e\xe6\xf0\xfb\xeb\xa7\xde\x8fa\x1d1'
#         POSTGRES_USER: "user"
#         POSTGRES_PASSWORD: "password"
#         PG_DB_HOST: "postgres"
#         PG_DB_NAME: "database"
#         CELERY_BROKER_URL: "redis://redis:6379/0"
#         CELERY_RESULT_BACKEND: "redis://redis:6379/0"
#       expose:
#         - 5140
#       ports:
#         - "5140:5140"
#       volumes:
#         - web-data:/var/www/html
#       depends_on:
#         - postgres
#         - redis
#       restart: unless-stopped
#       networks:
#         - postgres
#
#   redis:
#       container_name: redis_container
#       image: redis:6.2-alpine
#       command: redis-server --requirepass password
#       volumes:
#         - redis-data:/data
#       ports:
#         - "6379:6379"
#       restart: unless-stopped
#       networks:
#         - postgres
#
# volumes:
#     db-data:
#     pgadmin-data:
#     web-data:
#     redis-data:
#
# networks:
#     postgres:
#       driver: bridge