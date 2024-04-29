from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/grocery_management'
db = SQLAlchemy(app)

@app.route("/")
def firstpg():
    return render_template('firstpg.html')


class product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    unit = db.Column(db.String(120))
    price_per_unit = db.Column(db.Integer)
    no_of_products_available = db.Column(db.Integer)

    def __repr__(self):
        return '<product %r>' % self.product_id


@app.route("/product1", methods=['GET', 'POST'])
def product1():
    if request.method == 'POST':
        if 'delete' in request.form:
            # Handling form submission for deleting a product
            product_id = request.form.get('delete')
            
            # Querying the product to be deleted from the database
            product_to_delete = product.query.get_or_404(product_id)
                
            # Deleting the product from the database session
            db.session.delete(product_to_delete)
                
            # Committing the session to save the changes to the database
            db.session.commit()


        
        else:
            # Handling form submission for adding a new product
            product_id = request.form.get('product_id')
            name = request.form.get('name')
            unit = request.form.get('unit')
            price_per_unit = request.form.get('price_per_unit')
            no_of_products_available = request.form.get('no_of_products_available')

            no_of_products_available = int(unit)

            
            # Creating a new instance of the Product class
            new_product = product(product_id=product_id, name=name, unit=unit, price_per_unit=price_per_unit, no_of_products_available=no_of_products_available)
            
            # Adding the new product to the database session
            db.session.add(new_product)
            
            # Committing the session to save the changes to the database
            db.session.commit()
            
            
    
    # Rendering the product.html template for GET requests
    return render_template('product1.html', products=product.query.all())





class orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80))
    total = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return '<orders %r>' % self.order_id





@app.route("/orders1", methods=['GET', 'POST'])
def orders1():
    if request.method == 'POST':
        if 'delete' in request.form:
            order_id = request.form.get('delete')
            
            order_to_delete = orders.query.get_or_404(order_id)
                
            db.session.delete(order_to_delete)
            
            db.session.commit()

            
        
        else:
            order_id = request.form.get('order_id')
            customer_name = request.form.get('customer_name')
            total = 0
            datetime = request.form.get('datetime')

            
            new_order = orders(order_id=order_id, customer_name=customer_name, total=total, datetime=datetime )
            
            db.session.add(new_order)
        
            db.session.commit()

            update_order_total(order_id)         
            
    return render_template('orders1.html', orders=orders.query.all())


def update_order_total(order_id):
    # Query the order_details table for details related to the given order_id
    order_details_items = order_details.query.filter_by(order_id=order_id).all()
    
    # Calculate the total based on the order details
    total = sum(detail.subtotal for detail in order_details_items)
    
    # Update the total in the orders table
    order = orders.query.get(order_id)
    if order:
        order.total = total
        db.session.commit()




class order_details(db.Model):
    __tablename__ = 'order_details'
    sr_no = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Integer)

    def __repr__(self):
        return '<order_details %r>' % self.sr_no




@app.route("/order_details1", methods=['GET', 'POST'])
def order_details1():
    
    if request.method == 'POST':
        if 'delete' in request.form:
            sr_no = request.form.get('delete')
            
            order_details_to_delete = order_details.query.get_or_404(sr_no)
                
            db.session.delete(order_details_to_delete)
                
            db.session.commit()
        

        
        else:
            sr_no = request.form.get('sr_no')
            order_id = request.form.get('order_id')
            product_id = request.form.get('product_id')
            product_name = request.form.get('product_name')
            quantity = request.form.get('quantity')
            subtotal = request.form.get('subtotal')
            
            # Query the product based on the product_id
            product_entry = product.query.get(product_id)

            
            # Calculate the subtotal
            subtotal = int(quantity) * product_entry.price_per_unit

            product_entry.no_of_products_available -= int(quantity)

            
            new_order_details = order_details(sr_no=sr_no, order_id=order_id, product_id=product_id, product_name=product_name, quantity=quantity , subtotal=subtotal)
            
            db.session.add(new_order_details)
            
            db.session.commit()

            
    return render_template('order_details1.html', order_details=order_details.query.all() , products=product.query.all())


class contact_us(db.Model):
    __tablename__ = 'contact_us'
    sr__no = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80))
    mobile_no = db.Column(db.String(120))
    email = db.Column(db.String(120))
    issue = db.Column(db.String(120))

    def __repr__(self):
        return '<contact_us %r>' % self.sr__no


@app.route("/contact_us1", methods=['GET', 'POST'])
def contact_us1():
    if request.method == 'POST':
            customer_name = request.form.get('customer_name')
            mobile_no = request.form.get('mobile_no')
            email = request.form.get('email')
            issue = request.form.get('issue')
            
           
            new_issue = contact_us( customer_name=customer_name,mobile_no=mobile_no, email=email, issue=issue)
            
            db.session.add(new_issue)
            
            db.session.commit()
            
            
    return render_template('contact_us1.html', contact_uss=contact_us.query.all())

   


   


    
if __name__ == "__main__":
    app.run(debug=True)

