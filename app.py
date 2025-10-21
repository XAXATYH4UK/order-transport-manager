from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Order & Transport Manager - Flask Web Application
# Система управления заказами и транспортировкой
app = Flask(__name__)

# Настройки базы данных (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

# Модель базы данных
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(100))
    cargo_description = db.Column(db.String(200))
    load_date = db.Column(db.String(20))
    delivery_date = db.Column(db.String(20))
    status = db.Column(db.String(20))

    def __init__(self, order_number, client_name=None, cargo_description=None, load_date=None, delivery_date=None, status=None):
        self.order_number = order_number
        self.client_name = client_name
        self.cargo_description = cargo_description
        self.load_date = load_date
        self.delivery_date = delivery_date
        self.status = status

# Главная страница с фильтрацией
@app.route('/')
def index():
    # Получаем параметры фильтрации из URL
    status_filter = request.args.get('status', '')
    client_filter = request.args.get('client', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Получаем все заказы
    orders = Order.query.all()
    
    # Применяем фильтры в Python (для простоты)
    filtered_orders = orders
    
    if status_filter:
        filtered_orders = [order for order in filtered_orders if order.status == status_filter]
    
    if client_filter:
        filtered_orders = [order for order in filtered_orders 
                          if order.client_name and client_filter.lower() in order.client_name.lower()]
    
    if date_from:
        filtered_orders = [order for order in filtered_orders 
                          if order.load_date and order.load_date >= date_from]
    
    if date_to:
        filtered_orders = [order for order in filtered_orders 
                          if order.delivery_date and order.delivery_date <= date_to]
    
    # Получаем уникальные статусы для выпадающего списка
    all_statuses = list(set([order.status for order in orders if order.status]))
    
    return render_template('index.html', 
                         orders=filtered_orders, 
                         statuses=sorted(all_statuses),
                         current_status=status_filter,
                         current_client=client_filter,
                         current_date_from=date_from,
                         current_date_to=date_to)

# Добавление заказа
@app.route('/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        new_order = Order(
            order_number=request.form['order_number'],
            client_name=request.form['client_name'],
            cargo_description=request.form['cargo_description'],
            load_date=request.form['load_date'],
            delivery_date=request.form['delivery_date'],
            status=request.form['status']
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect('/')
    return render_template('add_order.html')

# Маршрут для очистки фильтров
@app.route('/clear_filters')
def clear_filters():
    return redirect(url_for('index'))

# API для получения статистики (опционально)
@app.route('/api/stats')
def get_stats():
    total_orders = Order.query.count()
    statuses_count = {}
    
    for order in Order.query.all():
        status = order.status or 'Не указан'
        statuses_count[status] = statuses_count.get(status, 0) + 1
    
    return {
        'total_orders': total_orders,
        'statuses': statuses_count
    }

# Удаление заказа
@app.route('/delete/<int:order_id>')
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('index'))

# Редактирование заказа
@app.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if request.method == 'POST':
        order.order_number = request.form['order_number']
        order.client_name = request.form['client_name']
        order.cargo_description = request.form['cargo_description']
        order.load_date = request.form['load_date']
        order.delivery_date = request.form['delivery_date']
        order.status = request.form['status']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_order.html', order=order)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
