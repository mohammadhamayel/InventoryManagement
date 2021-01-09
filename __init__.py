from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, json
from flask_mysqldb import MySQL




app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Inventory_Management'

mysql = MySQL(app)
#cur = mysql.connection.cursor()


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, location_Name, SUM(movement_qty), movement_to_location " 
                " FROM productmovement left join product on movement_product_id = product_id "
                " left join location on movement_to_location = location_id"
                " GROUP BY product_name, location_Name, movement_to_location")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', report=data )


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
        cur = mysql.connection.cursor()
        Product_Name = request.form['Product_Name']
        From_Location = request.form['From_Location']
        Qty = int(request.form['Qty'])

        To_Location = request.form['To_Location']
        if (To_Location == ""):
            To_Location = 0

        if (From_Location == ""):
            From_Location = 0
        else:
            cur.execute("SELECT SUM(movement_qty) FROM productmovement WHERE movement_product_id= %s "
                               "and movement_to_location= %s", (Product_Name, From_Location))
            tot = 0
            data = cur.fetchall()
            for row in data:
                print(row)
                tot = int(row[0])
                break
            print(tot)
            if tot < Qty:
               flash("You can't move a Qty grater than the existence in this location", 'error')
               return redirect(url_for('product_movement'))
            else:
                 restQty = tot - Qty
                 cur.execute(""" UPDATE productmovement SET
                                movement_qty=%s
                                WHERE movement_product_id= %s and movement_to_location= %s""",
                                (restQty, Product_Name, To_Location))



        cur.execute("INSERT INTO productmovement (movement_product_id, movement_from_location, movement_to_location, "
                    "movement_qty) VALUES (%s,%s,%s,%s)", (Product_Name, From_Location, To_Location, Qty))
        mysql.connection.commit()
        flash("Data Inserted Successfully", 'success')

        return redirect(url_for('product_movement'))


def check_sql_string(sql, values):
    unique = "%PARAMETER%"
    sql = sql.replace("?", unique)
    for v in values: sql = sql.replace(unique, repr(v), 1)
    return sql

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
    cur.execute("SELECT  * FROM product order by product_id")
    data = cur.fetchall()
    cur.close()

    return render_template('product.html', product=data )

@app.route('/location')
def location():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM location order by location_id")
    data = cur.fetchall()
    cur.close()

    return render_template('location.html', location=data )

@app.route('/product_movement')
def product_movement():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  movement_id, movement_from_location, movement_to_location, movement_product_id,"
                " product_name, location_Name, movement_qty "
                "FROM productmovement left join product on movement_product_id = product_id "
                "left join location on (movement_from_location = location_id or movement_to_location = location_id ) order by movement_id")
    data = cur.fetchall()
    cur.close()
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

def dbSelectAll(tblName):
    cur = mysql.connection.cursor()
    data = cur.execute("SELECT  * FROM "+ tblName)
    return  data


#def db_insert(tblName, fieldNames, values):
#    cur.execute("INSERT INTO "+tblName +" (" + fieldNames + " ) VALUES (%s,%s,%s,%s)", (values))


if __name__ == "__main__":
    app.run(debug=True)



