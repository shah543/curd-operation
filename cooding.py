from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)

# Database connection configuration
server = 'mysql@localhost:3306'
database = 'customerdb'
username = 'root'
password = 'shahnawaz@12345'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Create a cursor from the connection
cursor = conn.cursor()

# API routes

# Add Customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data['name']
    contact = data['contact']
    address = data['address']
    is_active = data.get('is_active', True)
    created_on = datetime.now()
    modify_on = datetime.now()
    
    cursor.execute("INSERT INTO Customers (Name, Contact, Address, IsActive, CreatedOn, ModifyOn) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, contact, address, is_active, created_on, modify_on))
    conn.commit()
    
    return jsonify({'message': 'Customer added successfully'}), 201

# Update Customer
@app.route('/customers/<int:id>', methods=['PUT', 'PATCH'])
def update_customer(id):
    data = request.get_json()
    name = data.get('name')
    contact = data.get('contact')
    address = data.get('address')
    is_active = data.get('is_active')
    modify_on = datetime.now()

    query = "UPDATE Customers SET ModifyOn = ?"
    parameters = [modify_on]

    if name:
        query += ", Name = ?"
        parameters.append(name)
    if contact:
        query += ", Contact = ?"
        parameters.append(contact)
    if address:
        query += ", Address = ?"
        parameters.append(address)
    if is_active is not None:
        query += ", IsActive = ?"
        parameters.append(is_active)

    query += " WHERE ID = ?"
    parameters.append(id)

    cursor.execute(query, tuple(parameters))
    conn.commit()

    return jsonify({'message': 'Customer updated successfully'}), 200

# Delete Customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    cursor.execute("DELETE FROM Customers WHERE ID = ?", (id,))
    conn.commit()
    
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Get All Customers
@app.route('/customers', methods=['GET'])
def get_all_customers():
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        customer = {
            'id': row.ID,
            'name': row.Name,
            'contact': row.Contact,
            'address': row.Address,
            'is_active': row.IsActive,
            'created_on': row.CreatedOn.strftime('%Y-%m-%d %H:%M:%S'),
            'modify_on': row.ModifyOn.strftime('%Y-%m-%d %H:%M:%S')
        }
        customers.append(customer)
    return jsonify(customers), 200

# Get Customer by ID
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    cursor.execute("SELECT * FROM Customers WHERE ID = ?", (id,))
    row = cursor.fetchone()
    if row:
        customer = {
            'id': row.ID,
            'name': row.Name,
            'contact': row.Contact,
            'address': row.Address,
            'is_active': row.IsActive,
            'created_on': row.CreatedOn.strftime('%Y-%m-%d %H:%M:%S'),
            'modify_on': row.ModifyOn.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(customer), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
