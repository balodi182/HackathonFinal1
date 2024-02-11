from flask import Flask , render_template ,request
app=Flask(__name__)
import sqlite3
import os


currentdir=os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def choice():
    return render_template("loginpage.html")

@app.route("/consumer")
def cnsmr():
    return render_template("sign in (1).html")


@app.route("/sellerloginpg")
def Sellerlogin():
    return render_template("seller.html")


@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/grocery')
def grocery():
    return render_template("grocery.html")

@app.route('/cosmetics')
def cosmetics():
    return render_template("cosmetics.html")

@app.route('/medical')
def medical():
    return render_template("medical.html")

@app.route("/newslr")
def newshop23():
    return render_template("newseller.html")

@app.route("/newusr34")
def newuser2():
    return render_template("signup.html")

@app.route("/newusr2")
def newuser22():
    return render_template("sign in (1).html")

@app.route("/oldslr")
def oldshop():
    return render_template("sign in.html")


@app.route("/sellerLogin")
def slrlog():
    return render_template("seller.html")




@app.route("/go")
def student(shopID):
    return render_template("index.html",shopID=shopID)



@app.route("/result",methods=["POST","GET"])
def result(): 
    if request.method=="POST":
        result=request.form
        shopID=request.args.get('usrnm')
        name=result["Name"]
        quat=result["Quantity"]
        prc=result["Price"]
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM stock WHERE name = ?"
        cursor.execute(query, (name,))
        count = cursor.fetchone()[0]
        absence=count
                
        if count==0:    
            query1= "INSERT INTO stock VALUES('{id}','{n}','{qt}','{pr}')".format(id=shopID,n=name , qt=quat, pr=prc)
            cursor.execute(query1)
            connection.commit()
            connection.close()
            return student(shopID)
        else:
            # If a row with the given name exists, update the quantity
            query_update = "UPDATE stock SET quantity = quantity + ? WHERE name = ?"
            query_update2 = "UPDATE stock SET price = price + ? WHERE name = ?"
            cursor.execute(query_update, (quat, name))
            cursor.execute(query_update2, (prc, name))
            connection.commit()
            connection.close()
            return student(shopID)
        
             
@app.route("/newshop",methods=["POST","GET"])
def newshop1():
    if request.method=="POST":
        values=request.form
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        shpnm=values["productName"]
        shpadd=values["productDescription"]
        shpcdd=values["coordinates"]
        shppwd=values["password"]
        shpct=values["contact"]
        
        query1= "INSERT INTO Shop('Shop Name','Address','Coordinates','Password','Rating','No_Rating','Contact') VALUES('{sn}','{sa}','{cd}','{ps}','0','0','{sct}')".format(sct=shpct,sn=shpnm,sa=shpadd , cd=shpcdd, ps=shppwd)
        cursor.execute(query1)
        connection.commit()
        connection.close()
        return render_template("sign in.html")
    
@app.route("/newUsrCrt",methods=["POST","GET"])
def newusr1():
    if request.method=="POST":
        values=request.form
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        usrnm=values["username"]
        usremail=values["email"]
        usrpwd=values["password"]
        
        query1= "INSERT INTO Customer ('Name','Email','Password') VALUES('{un}','{ue}','{up}')".format(un=usrnm,ue=usremail , up=usrpwd)
        cursor.execute(query1)
        connection.commit()
        connection.close()
        return render_template("sign in (1).html")
    

@app.route("/usrLgn",methods=["post","get"])
def usrlgn():
    if request.method=="POST":
        values=request.form
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        usrnm=values["username"]
        usrpwd=str(values["password"])
        query2 = "SELECT * FROM Customer WHERE Name=?"
        cursor.execute(query2, (usrnm,))
        row=cursor.fetchone()
        if row:
            password= str(row[2])
            if usrpwd==password:
                connection.close()
                return render_template("Hack.html")
            else:
                connection.close()
                return render_template('sign in (1).html')
        elif row==None:
            return render_template('sign in (1).html')
                
@app.route("/shpLgn",methods=["post","get"])
def shplgn():
    if request.method=="POST":
        values=request.form
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        usrnm=str(values["username"])
        usrpwd=str(values["password"])
        query2 = "SELECT * FROM Shop WHERE ShopID = ?"
        cursor.execute(query2, (usrnm,))
        row=cursor.fetchone()
        if row:
            password= str(row[4])
            if usrpwd==password:
                connection.close()
                return render_template("index.html",usrpwd=usrpwd,usrnm=usrnm)
        elif row==None:
            return render_template("sign in.html")
    

@app.route('/search')
def searchindex():
    return render_template('index1.html')

@app.route('/search_product', methods=['POST'])
def search_product1():
    if request.method=="POST":
        product_name = request.form['itemname']

        # Connect to SQLite database
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        # Execute SELECT query to search for product
        c.execute('''SELECT * FROM stock JOIN Shop ON Shop.ShopID = stock.ShopID WHERE stock.Name=?''', (product_name,))
        
        shop_info = c.fetchall()
        # Close database connection
        conn.close()

        if shop_info:
            return render_template('shop_info.html', shop_info=shop_info)
        else:
            return render_template('grocery.html')

app.run(debug=True)
