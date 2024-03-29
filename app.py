from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:password@server/database'
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    contact = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    modify_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'address': self.address,
            'is_active': self.is_active,
            'created_on': self.created_on,
            'modify_on': self.modify_on
        }

class Employee(db.Model):
    __tablename__ = 'Employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    contact = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    employee_id = Column(String(20), unique=True, nullable=False)
    qualifications = Column(Text)
    profile_photo = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    modify_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'address': self.address,
            'employee_id': self.employee_id,
            'qualifications': self.qualifications,
            'profile_photo': self.profile_photo,
            'is_active': self.is_active,
            'created_on': self.created_on,
            'modify_on': self.modify_on
        }

# Customer APIs
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], contact=data['contact'], address=data['address'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_dict()), 201

@app.route('/customers/<int:id>', methods=['PUT', 'PATCH'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    if 'name' in data:
        customer.name = data['name']
    if 'contact' in data:
        customer.contact = data['contact']
    if 'address' in data:
        customer.address = data['address']
    db.session.commit()
    return jsonify(customer.to_dict())

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict())

# Employee APIs
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(name=data['name'], contact=data['contact'], address=data['address'], 
                             employee_id=data['employee_id'], qualifications=data['qualifications'],
                             profile_photo=data['profile_photo'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

@app.route('/employees/<int:id>', methods=['PUT', 'PATCH'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.json
    if 'name' in data:
        employee.name = data['name']
    if 'contact' in data:
        employee.contact = data['contact']
    if 'address' in data:
        employee.address = data['address']
    if 'employee_id' in data:
        employee.employee_id = data['employee_id']
    if 'qualifications' in data:
        employee.qualifications = data['qualifications']
    if 'profile_photo' in data:
        employee.profile_photo = data['profile_photo']
    db.session.commit()
    return jsonify(employee.to_dict())

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
