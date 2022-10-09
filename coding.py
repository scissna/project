from datetime import datetime

from flask import request,render_template,Flask
from werkzeug.utils import redirect

from DBConnection import Db

app=Flask(__name__)

@app.route('/')
def log():
    return render_template("loginindex.html")

@app.route('/login', methods=['post'])
def login():
    username=request.form['un']
    password=request.form['pwd']
    db=Db()
    qry=" SELECT * FROM `login`WHERE `username`='"+username+"' and`password`='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return '''<script>alert("invaild");window.location="login_index"</script>'''
    elif res['usertype'] == "admin":
        return '''<script>alert("vaild");window.location="admin"</script>'''
    elif res['usertype'] == "user":
        return '''<script>alert("vaild");window.location="userhome"</script>'''

    else:
        return '''<scrpit>alert("invaild");window.location="login_index"</scrpit>'''


@app.route('/admin')
def admin_home():
    return render_template("aindex.html")


@app.route('/admin_add_product')
def admin_add_product():
    qry="select * from category"
    db=Db()
    res=db.select(qry)
    return render_template("admin/Addproduct.html",data=res)

@app.route('/admin_add_product_post', methods=['post'])
def admin_add_product_post():
    name=request.form['textfield1']
    price=request.form['textfield2']
    image=request.files['fileField']
    date=datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:/Users/Hp/PycharmProjects/onlineshopping/src/static/photo/" +date+".jpg")
    path="/static/photo/"+date+".jpg"
    category=request.form['jumpMenu']
    description=request.form['textfield3']

    db = Db()
    qry=" INSERT INTO product(`Category_id`,`name`,`price`,`image`,`description`) VALUES ('"+category+"','"+name+"','"+price+"','"+path+"','"+description+"')"
    res=db.insert(qry)
    return '''<script>alert('Successfully added');window.location="/view_admin_product_manage"</script>'''




@app.route('/admin_categories')
def admin_categories():
    return render_template("admin/categories.html")

@app.route('/admin_categories_post', methods=['post'])
def admin_categories_post():
    Category=request.form['textfield']
    Description=request.form['textarea']
    db=Db()
    qry= "INSERT INTO category(`Categoryname`,`Description`) VALUES('"+Category+"','"+Description+"')"
    res=db.insert(qry)
    return '''<script>alert('Successfully added');window.location="/view_admin_category_management"</script>'''



@app.route('/view_admin_category_management')
def view_admin_category_management():
    qry = "select * from category"
    db = Db()
    res = db.select(qry)
    return render_template("admin/categorymanagement.html",data=res)

@app.route('/delete_admin_category_management/<id>')
def delete_admin_category_management(id):
    qry="delete from  category    where Category_id='"+id+"'  "
    db=Db()
    res=db.delete(qry)
    return view_admin_category_management()

@app.route('/edit_admin_category_management/<id>')
def edit_admin_category_management(id):
    qry="select * from category where Category_id='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("admin/editcategories.html",data=res)

@app.route('/edit_admin_category_management_post',methods=['post'])
def edit_admin_category_management_post():
    Category = request.form['textfield']
    Description = request.form['textarea']
    id=request.form['cat']
    qry="update category set Categoryname='"+Category+"',Description='"+Description+"' where Category_id='"+id+"' "
    db=Db()
    res=db.update(qry)
    return view_admin_category_management()




@app.route('/view_admin_product_manage')
def view_admin_product_manage():
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id`"
    db = Db()
    res = db.select(qry)
    qry1 = "select * from category"
    res1 = db.select(qry1)
    return render_template("admin/productmanagement.html",data=res,data1=res1)



@app.route('/search_admin_product_post',methods=['post'])
def search_admin_product_post():
    select=request.form['jumpMenu']
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` where `category`.`Category_id`='"+select+"'"
    print(qry)
    db = Db()
    res = db.select(qry)
    qry1 = "select * from category"
    res1 = db.select(qry1)
    return render_template("admin/productmanagement.html", data=res, data1=res1)


@app.route('/delete_view_admin_product_manage/<id>')
def delete_view_admin_product_manage(id):
    qry = "delete from  product    where Product_id='" + id + "'  "
    db = Db()
    res = db.delete(qry)
    return view_admin_product_manage()



@app.route('/admin_edit_product/<id>')
def admin_edit_product(id):
    db=Db()
    qry="SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` and product.Product_id='"+ id +"'  "
    res=db.selectOne(qry)
    qry1="select * from category"
    res1=db.select(qry1)
    return render_template("admin/editproduct.html",data=res,data1=res1)

@app.route('/admin_edit_product_post',methods=['post'])
def admin_edit_product_post():
    name = request.form['textfield1']
    price = request.form['textfield2']
    image = request.files['fileField']
    date = datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:/Users/Hp/PycharmProjects/onlineshopping/src/static/photo/" + date + ".jpg")
    path = "/static/photo/" + date + ".jpg"
    category = request.form['jumpMenu']
    description = request.form['textfield3']
    id = request.form['cat']

    qry=" update product set name='"+name+"',price='"+price+"',image='"+path+"',Category_id='"+category+"',description='"+description+"' where Product_id='"+id+"'  "
    db=Db()
    res=db.update(qry)
    return view_admin_product_manage()



@app.route('/view_admin_feedback')
def view_admin_feedback():
    qry="SELECT `product`.*,`registration`.*,`feedback`.* FROM `feedback` JOIN `product` ON `feedback`.`Product_id`=`product`.`Product_id` JOIN `registration` ON `registration`.`login_id`=`feedback`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/feedback.html",data=res)

@app.route('/search_admin_feedback_post',methods=['post'])
def search_admin_feedback_post():
    From=request.form['textfield']
    To=request.form['textfield2']

    qry = "SELECT `product`.*,`registration`.*,`feedback`.* FROM `feedback` JOIN `product` ON `feedback`.`Product_id`=`product`.`Product_id` JOIN `registration` ON `registration`.`login_id`=`feedback`.`user_id` where `feedback`.Date between '"+From+"' and '"+To+"'"
    db = Db()
    res = db.select(qry)

    return render_template("admin/feedback.html",data=res)




@app.route('/view_admin_orders')
def view_admin_orders():
    qry= " SELECT `order`.*,`registration`.* FROM `order` JOIN `registration` ON `registration`.`login_id`=`order`.`user_id` "
    db=Db()
    res=db.select(qry)
    return render_template("admin/vieworders.html",data=res)

@app.route('/view_admin_orders_post',methods=['post'])
def view_admin_orders_post():
    return "ok"



@app.route('/view_admin_order_more/<id>')
def view_admin_order_more(id):
    qry=" SELECT * FROM `product` INNER JOIN  orderdetails ON `product`.`Product_id`=`orderdetails`.`Product_id` INNER JOIN `category` ON `product`.`Category_id`=`category`.`Category_id` INNER JOIN `order` ON `order`.`order_id`=`orderdetails`.`order_id` "
    db=Db()
    res=db.select(qry)
    print(qry)
    print(res)
    return render_template("admin/ordermore.html",data=res)

@app.route('/view_admin_order_more_post',methods=['post'])
def view_admin_order_more_post():
    return "ok"





@app.route('/view_admin_custom_order')
def view_admin_custom_order():
    qry="SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/viewcustomorder.html",data=res)

@app.route('/view_admin_custom_order_post',methods=['post'])
def view_admin_custom_order_post():
    return "ok"

@app.route('/approve_custorder/<id>')
def approve_custorder(id):
    qry="UPDATE customorder set Status='Approved' where cust_id='"+id+"' "
    db=Db()
    res=db.update(qry)
    return redirect('/view_approved_custorder')

@app.route('/view_approved_custorder')
def view_approved_custorder():
    qry = "SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where Status='Approved'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/viewapprovedcustomorder.html",data=res)



@app.route('/reject_custorder/<id>')
def reject_custorder(id):
    qry = "UPDATE customorder set Status='Rejected' where cust_id='" + id + "' "
    db = Db()
    res = db.update(qry)
    return redirect('/view_reject_customorder')

@app.route('/view_reject_customorder')
def view_reject_customorder():
    qry = "SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where Status='Rejected'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/viewrejectedcustomorder.html", data=res)


@app.route('/view_admin_custom_order_more/<id>')
def view_admin_custom_order_more(id):
    qry="SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where cust_id='"+id+"'"
    db=Db()
    res=db.select(qry)
    return render_template("admin/customordermore.html",data=res)

@app.route('/view_admin_custom_order_more_post',methods=['post'])
def view_admin_custom_order_more_post():
    return "ok"




@app.route('/view_admin_payment')
def view_admin_payment():
    qry="SELECT * FROM `payment` INNER JOIN `order` ON `order`.`order_id`=`payment`.`order_id` INNER JOIN `registration` ON `registration`.`login_id`=`order`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/Payment.html",data=res)

@app.route('/view_admin_payment_post',methods=['post'])
def view_admin_payment_post():
    return "ok"




@app.route('/view_admin_refund')
def view_admin_refund():
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Pending' "
    db=Db()
    res=db.select(qry)
    return render_template("admin/Refund.html",data=res)

@app.route('/view_admin_refund_post',methods=['post'])
def view_admin_refund_post():
    return "ok"

@app.route('/approved_refund_product/<id>')
def approved_refund_product(id):
    qry="update `return` set Status='Pending' where return_id='"+id+"'"
    db=Db()
    res=db.update(qry)
    qry1="update `order"
    return redirect('/view_approved_refund')

@app.route('/view_approved_refund')
def view_approved_refund():
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Approved' "
    db=Db()
    res=db.select(qry)
    return render_template("admin/Refundapproved.html",data=res)

@app.route('/approved_refund/<id>')
def approved_refund(id):
    db=Db()
    qry=" update `return` set Status='Approved' where return_id='"+id+"'"
    res=db.update(qry)
    return redirect('/view_approved_refund')

@app.route('/rejected_refund/<id>')
def rejected_refund(id):
    db=Db()
    qry=" Update `return` set Status='Rejected' where return_id='"+id+"'"
    res=db.update(qry)
    return redirect('/view_rejected_refund')

@app.route('/view_rejected_refund')
def view_rejected_refund():
    db=Db()
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Rejected' "
    res=db.select(qry)
    return render_template("admin/Refundrejected.html",data=res)

if __name__=='__main__':
    app.run(debug=True)
