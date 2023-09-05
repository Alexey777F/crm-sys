from config import create_app

app, db = create_app()


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
    def get_manager_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_manager_id(cls, username):
        manager = cls.get_manager_username(username)  # получаем объект менеджера по имени пользователя
        return manager.id  # возвращаем id менеджера

    @classmethod
    def get_manager_info(cls, username):
        return cls.query.filter_by(username=username).with_entities(cls.full_name, cls.working_position, cls.city,
                                                                    cls.phone_number, cls.email).first()


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    @classmethod
    def get_client_id(cls):
        last_client = cls.query.order_by(cls.id.desc()).first()  # получаем id последнего клиента в базе
        if last_client:
            return last_client.id + 1  # если есть записи, то возвращаем следующий номер после последнего
        else:
            return 1  # если база пуста, то присваиваем номер 1

    @classmethod
    def get_all_clients(cls):
        return cls.query.all()

    @classmethod
    def add_client(cls, customer, phone_number, email):
        client = cls(customer=customer, phone_number=phone_number, email=email)
        db.session.add(client)
        db.session.commit()


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
        # Add order to database
        order = cls(customer=customer, description=description, income=income, status=status, dates=dates,
                       manager_id=manager_id, client_id=client_id)
        db.session.add(order)
        db.session.commit()

    @classmethod
    def get_order_id(cls):
        last_order = cls.query.order_by(cls.id.desc()).first()  # получаем последнего клиента в базе
        if last_order:
            return last_order.id + 1  # если есть записи, то возвращаем следующий номер после последнего
        else:
            return 1  # если база пуста, то присваиваем номер 1


class Combined(db.Model):
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)

    @classmethod
    def add_combined(cls, manager_id, order_id):
        data = cls(manager_id=manager_id, order_id=order_id)
        db.session.add(data)
        db.session.commit()

    @classmethod
    def get_orders_by_manager(cls, username):
        manager = Managers.get_manager_username(username)
        manager_orders = db.session.query(Orders).join(cls).filter(cls.manager_id == manager.id).all()
        clients = len([order.client_id for order in manager_orders])
        total_income = sum([order.income for order in manager_orders])
        total_orders = len(manager_orders)
        return clients, total_income, total_orders


# 1) Функция, которая возвращает все записи из таблицы "Orders":
# Orders.query.all()
#
# 2) Функция, которая возвращает все заказы, сделанные клиентом с именем "John":
# Orders.query.filter_by(customer='John').all()
#
# 3) Функция, которая возвращает все заказы, у которых доход больше 1000:
# Orders.query.filter(Orders.income > 1000).all()
#
# 4) Функция, которая возвращает все заказы, отсортированные по дате в обратном порядке:
# Orders.query.order_by(Orders.dates.desc()).all()
#
# 5) Функция, которая возвращает первые 10 заказов:
# Orders.query.limit(10).all()
#
# 7) Функция, которая возвращает все заказы, у которых имя клиента содержит "John":
# Orders.query.filter(Orders.customer.like('%John%')).all()
#
# 9) Функция, которая возвращает все заказы, у которых дата между "2021-01-01" и "2021-12-31":
# Orders.query.filter(Orders.dates.between('2021-01-01', '2021-12-31')).all()
#
# 10) Функция, которая возвращает все заказы со статусом "pending" или "processing":
# Orders.query.filter(Orders.status.in_(['pending', 'processing'])).all()
#
# 11) Функция, которая возвращает все заказы, у которых id менеджера равен 2:
# Orders.query.filter(Orders.manager_id == 2).all()
#
# 12) Функция, которая объединяет таблицы "Orders" и "Managers" и возвращает все заказы, у которых имя менеджера "John Doe":
# Orders.query.join(Managers).filter(Managers.name == 'John Doe').all()
#
# 13) Функция, которая объединяет таблицы "Orders" и "Clients" и возвращает все заказы, у которых имя клиента "Apple Inc.":
# Orders.query.join(Clients).filter(Clients.name == 'Apple Inc.').all()
#
# 14) Функция, которая возвращает только поля "orders" и "income" из заказов, сделанных клиентом с именем "John":
# Orders.query.filter(Orders.customer == 'John').with_entities(Orders.orders, Orders.income).all()
#
# 15) Функция, которая возвращает первый заказ, сделанный клиентом с именем "John":
# Orders.query.filter_by(customer='John').first()
#
# 16) Функция, которая возвращает единственный заказ, сделанный клиентом с именем "John" (если такой заказ не найден, возникает ошибка):
# Orders.query.filter_by(customer='John').one()
#
# 17) Функция, которая возвращает количество заказов, сделанных клиентом с именем "John":
# Orders.query.filter_by(customer='John').count()
#
# 18) Функция, которая удаляет все заказы, сделанные клиентом с именем "John":
# Orders.query.filter_by(customer='John').delete()
#
# 19) Функция, которая обновляет доход всех заказов, сделанных клиентом с именем "John", на 2000:
# Orders.query.filter_by(customer='John').update({Orders.income: 2000})
