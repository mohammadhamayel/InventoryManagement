import jsonConverter as jsonConverter
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, json
from flask_mysqldb import MySQL




app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Inventory_Management'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/insertProduct', methods = ['POST'])
def insertProduct():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product (product_name) VALUES (%s)", (name))
        mysql.connection.commit()
        return redirect(url_for('product'))

@app.route('/insertLocation', methods = ['POST'])
def insertLocation():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO location (location_Name) VALUES (%s)", (name))
        mysql.connection.commit()
        return redirect(url_for('location'))



@app.route('/insertMovement', methods = ['POST'])
def insertMovement():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        Product_Name = request.form['Product_Name']
        From_Location = request.form['From_Location']
        if (From_Location == ""):
            From_Location = 0

        To_Location = request.form['To_Location']
        if (To_Location == ""):
            To_Location = 0


        Qty = request.form['Qty']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productmovement (movement_product_id, movement_from_location, movement_to_location, "
                    "movement_qty) VALUES (%s,%s,%s,%s)", (Product_Name, From_Location, To_Location, Qty))
        mysql.connection.commit()
        return redirect(url_for('product_movement'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/deleteProduct/<string:id_data>', methods = ['GET'])
def deleteProduct(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE product_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('product'))

@app.route('/deleteLocation/<string:id_data>', methods = ['GET'])
def deleteLocation(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM location WHERE location_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('location'))

@app.route('/deleteMovement/<string:id_data>', methods = ['GET'])
def deleteMovement(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productmovement WHERE movement_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('product_movement'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/updateProduct', methods=['POST', 'GET'])
def updateProduct():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE product
               SET product_name=%s
               WHERE product_id=%s
            """, (name, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('product'))

@app.route('/updateLocation', methods=['POST', 'GET'])
def updateLocation():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE location
               SET location_Name=%s
               WHERE location_id=%s
            """, (name, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('location'))

@app.route('/updateMovement', methods=['POST', 'GET'])
def updateMovement():

    if request.method == 'POST':
        id_data = request.form['id']
        productId = request.form['Product_Name']
        fromLocation = request.form['From_Location']
        toLocation = request.form['To_Location']
        Qty = request.form['Qty']

        if (fromLocation == ""):
            fromLocation = 0

        if (toLocation == ""):
            toLocation = 0

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE productmovement
               SET movement_product_id=%s,
                movement_from_location=%s,
                movement_to_location=%s,
                movement_qty=%s
               WHERE movement_id =%s
            """, (productId, fromLocation, toLocation, Qty, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('product_movement'))


@app.route('/product')
def product():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM product")
    data = cur.fetchall()
    cur.close()

    return render_template('product.html', product=data )

@app.route('/location')
def location():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM location")
    data = cur.fetchall()
    cur.close()

    return render_template('location.html', location=data )

@app.route('/product_movement')
def product_movement():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  movement_id, movement_from_location, movement_to_location, movement_product_id,"
                " product_name, location_Name, movement_qty "
                "FROM productmovement left join product on movement_product_id = product_id "
                "left join location on (movement_from_location = location_id or movement_to_location = location_id ) ")
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('product_movement.html', productmovement=data)


@app.route('/getLists')
def getLists():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM location")
    location = cur.fetchall()
    cur.execute("SELECT  * FROM product")
    product = cur.fetchall()
    dynamicLists = {}

    dynamicLists["location"] = location
    dynamicLists["product"] = product
    return jsonify(dynamicLists)


if __name__ == "__main__":
    app.run(debug=True)



