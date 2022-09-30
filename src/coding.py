from flask import *

from dbconnection import *
from datetime import datetime
app=Flask(__name__)

@app.route('/')
def log():
    return render_template("login.html")

@app.route('/login', methods=['post'])
def login():
    username=request.form['un']
    password=request.form['pwd']
    qry=" SELECT * FROM login WHERE username=%s and password=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("invalid");window.location="login_index"</script>'''
    elif res['usertype'] == "admin":
        return '''<script>alert("valid");window.location="admin"</script>'''
    elif res['usertype'] == "user":
         return '''<script>alert("valid");window.location="user"</script>'''
    else:
        return '''<scrpit>alert("invalid");window.location="login"</scrpit>'''

@app.route('/admin')
def admin_home():
    return render_template("admin.html")

@app.route('/user')
def user_home():
    return render_template("user.html")

app.run(debug=True)
