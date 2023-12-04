from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    working_position = db.Column(db.String(70), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    @classmethod
    def delete_manager(cls, username):
        manager = cls.get_manager_username(username)
        try:
            db.session.delete(manager)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка {e} при удалении данных из таблицы Managers(Менеджеры)")

    @classmethod
    def get_manager_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_manager_id(cls, username):
        manager = cls.get_manager_username(username)
        return manager.id

    @classmethod
    def get_manager_info(cls, username):
        return cls.query.filter_by(username=username).with_entities(cls.full_name, cls.working_position, cls.city,
                                                                    cls.phone_number, cls.email).first()

    @classmethod
    def get_manager_email(cls, username):
        """Возвращает список с 1-м элементом - почтой"""
        return cls.query.filter_by(username=username).with_entities(cls.email).first()


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    @classmethod
    def get_client_id(cls):
        last_client = cls.query.order_by(cls.id.desc()).first()
        if last_client:
            return last_client.id + 1
        else:
            return 1

    @classmethod
    def get_all_clients(cls):
        return cls.query.all()

    @classmethod
    def add_client(cls, customer, phone_number, email):
        client = cls(customer=customer, phone_number=phone_number, email=email)
        try:
            db.session.add(client)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка {e} при добавлении данных в таблицу Clients(Клиенты)")


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(65), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    income = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    dates = db.Column(db.Date, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    @classmethod
    def get_all_orders(cls):
        return cls.query.all()

    @classmethod
    def get_order_by_manager(cls, manager_id):
        return cls.query.filter_by(manager_id=manager_id).all()

    @classmethod
    def add_order_by_manager(cls, customer, description, income, status, dates, manager_id, client_id):
        order = cls(customer=customer, description=description,
                    income=income, status=status, dates=dates,
                    manager_id=manager_id, client_id=client_id)
        try:
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка {e} при добавлении данных в таблицу Orders(Заказы)")

    @classmethod
    def get_order_id(cls):
        last_order = cls.query.order_by(cls.id.desc()).first()
        if last_order:
            return last_order.id + 1
        else:
            return


class Combined(db.Model):
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)

    @classmethod
    def add_combined(cls, manager_id, order_id):
        data = cls(manager_id=manager_id, order_id=order_id)
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка {e} при добавлении данных в таблицу Combined")

    @classmethod
    def get_orders_by_manager(cls, username):
        """Метод класса Combined который возвращает словарь с данными,
        за: сегодня"""
        manager = Managers.get_manager_username(username)
        current_date = date.today()
        manager_orders_today = cls.filter_orders_by_today(manager.id, current_date)
        clients_today, total_income_today, total_orders_today = cls.calculate_metrics(manager_orders_today)
        return clients_today, total_income_today, total_orders_today

    @classmethod
    def filter_orders_by_today(cls, manager_id, current_date):
        return db.session.query(Orders).join(cls).filter(cls.manager_id == manager_id,
                                                         Orders.dates == current_date).all()

    @classmethod
    def filter_orders_by_manager(cls, manager_id):
        return db.session.query(Orders).join(cls).filter(cls.manager_id == manager_id).all()

    @classmethod
    def calculate_metrics(cls, orders):
        clients = len(set([order.client_id for order in orders]))
        total_income = sum([order.income for order in orders])
        total_orders = len(orders)
        return clients, total_income, total_orders
