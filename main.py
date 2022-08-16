import random
from flask import *
from pymongo import *
import string

app=Flask(__name__,template_folder="template")
app.secret_key="i love pooja"

cli=MongoClient("mongodb://localhost:27017")
mydba=cli["Privacy"]
mytba=mydba["userdata"]
mytba2=mydba["logindetails"]

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/regi")
def regi():
    return render_template("newhtml.html")

@app.route("/new",methods=["GET","POST"])
def new():
    if request.method=="POST":
        name = request.form['name']
        username = request.form['uname']
        password = request.form['passw']
        mydata={
            "Name":name,
            "username":username,
            "Password":password

        }
        mytba2.insert_one(mydata)
        return redirect("/")
    return render_template("newhtml.html")





@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
       usname=request.form["uname"]
       password = request.form["passw"]

       session['user']=usname

       for i in mytba2.find({},{"username":usname,"Password":password}):
           user=i["username"]
           passw = i["Password"]
           print(user)
           if usname == user and password == passw:
               return redirect("/show")
           else:
               return "<h1>Login Failed <br/><a href='/'>Log in </a> <h1/>"

















    return render_template("index.html")









@app.route("/show",methods=["GET","POST"])
def show():
    name=session.get("user")
    if request.method=="POST":
        normname = request.form['name']
        email = request.form['email']
        password = request.form['pass']

        data = {
            "Name": normname,
            "email": email,
            "Password": password,
            "username": name
        }
        mytba.insert_one(data)

        return redirect("/show")
    find = mytba.find({"username": name})

    return render_template("page.html",data=find)



@app.route("/sh/<id>")
def dels(id):

    mytba.delete_one({"Name":id})
    return redirect("/show")

@app.route("/update/<id>",methods=["POST"])
def update(id):
    oldpass={
        "Password":id

    }
    newpass=request.form["passw"]
    myval={
        "$set":{
            "Password":newpass
        }
    }
    mytba.update_one(oldpass,myval)
    return redirect("/show")
@app.route("/del")
def delete():
    session.pop("user")
    return redirect("/")






if __name__=="__main__":
    app.run()