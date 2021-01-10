#The procedure we follow to connect Flask-MySQL is as follows:
import json
import datetime
from flask import Flask , jsonify ,request
from flask_mysqldb import MySQL
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '<mo3tasem>'      ##########Note that: this should be changed according to your mysql root's password

#the name of the database :)
app.config['MYSQL_DB'] = 'theonlinestore'

mysql = MySQL(app)
parser = reqparse.RequestParser() 

################ Noran ################################
def ConvertTupleToJson(cursor,tuple):
    field_names = [i[0] for i in cursor.description]
    print(field_names)
    d = {}
    for i in range(len(field_names)):
        d[field_names[i]] = tuple[i]
        print(tuple[i])

    json_string = json.dumps(d)
    print(json_string)
    return json_string

def ConvertListOfListsToJson(cursor,ListOfLists):

    field_names = [i[0] for i in cursor.description]
    print(field_names)
    ListOfObjects = []
    for tuple in ListOfLists:
        d = {}
        for i in range(len(field_names)):
            d[field_names[i]] = tuple[i]
            print(tuple[i])
        ListOfObjects.append(d)
    json_string = json.dumps(ListOfObjects)

    print(json_string)
    return json_string

def CreateInsertQuery(tableName, Map):
    query = "insert into theonlinestore.{} (".format(tableName)
    values = " values ("
    print(Map)
    for key,value in Map.items():
        print("lsa")
        if(value != ''):
            query=query+key+','
            values= values +(" '{}' ".format(value))+','
            print(query)
            print(values)
            print("gwa")

    query = query[:-1] + ')'
    values = values[:-1] + ')'
    print(query)
    print(values)
    query=query+values

    return query

def CreateGetQuery(tableName, Map):
    query = "select * from {} where ".format(tableName)
    print(Map)
    for key,value in Map.items():
        print("lsa")
        if(value != ''):
            query=query+key+"='"+value+"' and "
            print(query)
            print("gwa")

    query = query[:-4]
    print(query)
    return query

####################################### Building the our restful api ##################################

class login_getCustomer(Resource):
    def post(self):
        try:
            parser.add_argument("Email")
            parser.add_argument("Password")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_getCustomerIdWithEmailAndPassword = " Select * From customer where Email = '{}' and Password = '{}'; ".format(args["Email"],args["Password"])
            cursor.execute(query_getCustomerIdWithEmailAndPassword)
            customerData = cursor.fetchall()
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if(customerData==()):
            # no matching email and password (If customer credentials are invalid!)
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertTupleToJson(cursor,customerData[0])


class signup_addCustomer(Resource):
    def post(self):
        try:
            parser.add_argument("FirstName")
            parser.add_argument("SecondName")
            parser.add_argument("PhoneNumber")
            parser.add_argument("Gender")
            parser.add_argument("Email")
            parser.add_argument("Password")
            parser.add_argument("Governorate")
            parser.add_argument("City")
            parser.add_argument("StreetName")
            parser.add_argument("BuildingNumber")
            parser.add_argument("AppartmentNumber")

            args = parser.parse_args()
            cursor = mysql.connection.cursor()
            query_insertCustomer = " insert into customer (FirstName,SecondName,Governorate,City,StreetName,BuildingNumber,AppartmentNumber,Gender,PhoneNumber,Email,Password) values ('{}','{}','{}','{}','{}',{},{},'{}',{},'{}','{}');".format(args["FirstName"] , args["SecondName"] , args["Governorate"] , args["City"] , args["StreetName"] , args["BuildingNumber"] , args["AppartmentNumber"] , args["Gender"] , args["PhoneNumber"] , args["Email"], args["Password"])
            cursor.execute(query_insertCustomer)
            query_getCustomerWithEmail = "select * from customer where Email = '{}'".format(args["Email"])
            cursor.execute(query_getCustomerWithEmail)
            customerData = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        except:
            #an exception will be thrown if phoneNum or email or both are duplicated (If customer is already signed up (registered))
            cursor.close()
            return None
        #cursor.fetchall() returns a table (i.e. [[val_1,val_2,....,val_lastAttribute]] )
        return ConvertTupleToJson(cursor,customerData[0])

class signup_addEmployee(Resource):
    def post(self):
        try:
            parser.add_argument("FirstName")
            parser.add_argument("SecondName")
            parser.add_argument("PhoneNumber")
            parser.add_argument("Email")
            parser.add_argument("Password")
            parser.add_argument("Position")
            parser.add_argument("Governorate")
            parser.add_argument("City")
            parser.add_argument("StreetName")
            parser.add_argument("BuildingNumber")
            parser.add_argument("AppartmentNumber")

            args = parser.parse_args()
            cursor = mysql.connection.cursor()

            query_insertEmployee = " insert into {} (FirstName,SecondName,Governorate,City,StreetName,BuildingNumber,AppartmentNumber,PhoneNumber,Email,Password) values ('{}','{}','{}','{}','{}',{},{},{},'{}','{}');".format(args["Position"],args["FirstName"] , args["SecondName"] , args["Governorate"] , args["City"] , args["StreetName"] , args["BuildingNumber"] , args["AppartmentNumber"] , args["PhoneNumber"] , args["Email"], args["Password"])
            cursor.execute(query_insertEmployee)
            query_getEmployeeWithEmail = "select * from {} where Email = '{}'".format(args["Position"], args["Email"])
            cursor.execute(query_getEmployeeWithEmail)
            employeeData = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        except:
            #an exception will be thrown if phoneNum or email or both are duplicated (If employee is already signed up (registered))
            cursor.close()
            return None
        #cursor.fetchall() returns a table (i.e. [[id]] ) thats why we return [0][0]
        return ConvertTupleToJson(cursor,employeeData[0])


class login_getEmployee(Resource):
    def post(self):
        try:
            parser.add_argument("Email")
            parser.add_argument("Password")
            parser.add_argument("Position")

            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_getEmployeeWithEmailAndPassword = " Select * From {} where Email = '{}' and Password = '{}'; ".format(args["Position"],args["Email"],args["Password"])
            cursor.execute(query_getEmployeeWithEmailAndPassword)
            employeeData = cursor.fetchall()
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if (employeeData == ()):
            # no matching email and password (If customer credentials are invalid!)
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertTupleToJson(cursor, employeeData[0])

class addPromocode(Resource):
    def post(self):
        try:
            parser.add_argument("Code")
            parser.add_argument("Discount")
            parser.add_argument("EndTime")

            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_insertPromocode = " insert into promocode (Code,Discount,EndTime) values ('{}',{},'{}');".format(args["Code"], args["Discount"], args["EndTime"])
            cursor.execute(query_insertPromocode)
            print("Hereeeeeeeeee")
            query_getPromocode = "select * from promocode where Code = '{}'".format(args["Code"])
            cursor.execute(query_getPromocode)
            promocodeData = cursor.fetchall()
            print(promocodeData)
            mysql.connection.commit()

        except:
            cursor.close()
            print("In excpet")
            #Code couldn't be added because it already exists
            return None

        if (promocodeData == ()):
            #this condition will never happen
            print("In empty")
            cursor.close()
            return None
        else:
            print("In empty else")
            cursor.close()
            return ConvertTupleToJson(cursor, promocodeData[0])

class addDiscount(Resource):
    def post(self):
        try:
            parser.add_argument("ID")
            parser.add_argument("Discount")
            parser.add_argument("EndTimeOffer")

            args = parser.parse_args()

            cursor = mysql.connection.cursor()

            query_addDiscount = " UPDATE product SET Discount = {} , EndTimeOffer = '{}' WHERE ID = {} ;".format(args["Discount"], args["EndTimeOffer"], args["ID"])
            cursor.execute(query_addDiscount)

            mysql.connection.commit()
            cursor.close()
            return None
        except:
            cursor.close()
            print("In excpet")
            return None

class requestProduct(Resource):
    def post(self):
        try:
            parser.add_argument("ID")
            parser.add_argument("Quantity")
            parser.add_argument("requestedQuantity")
            parser.add_argument("userIDWhoRequested")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()

            #updating the product with the new total quantity
            newQuantity = int(args["Quantity"])+int(args["requestedQuantity"])
            query_requestProduct = " UPDATE product SET Quantity = '{}' WHERE ID = {} ;".format(newQuantity, args["ID"])
            cursor.execute(query_requestProduct)


            print(newQuantity)
            print('args')
            print(args)
            # adding the request
            query_insertRequest = "insert into request (SalesManId,ProductId,Quantity) values({},{},{})".format(args["userIDWhoRequested"], args["ID"], args["requestedQuantity"])
            cursor.execute(query_insertRequest)

            print("newQuantity")

            mysql.connection.commit()
            cursor.close()
            return None
        except:
            cursor.close()
            print("In excpet")
            return None

class getPromocodes(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            query_getPromocodes = " Select * From promocode"
            cursor.execute(query_getPromocodes)
            allPromocodes = cursor.fetchall()
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if (allPromocodes == ()):
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertListOfListsToJson(cursor, allPromocodes)

class editPromocode(Resource):
    def post(self):
        try:
            parser.add_argument("Code")
            parser.add_argument("Discount")
            parser.add_argument("EndTime")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_editPromocode = " UPDATE promocode SET Discount = {} , EndTime = '{}' , WHERE Code = '{}' ;".format(args['Discount'],args['EndTime'],args['Code'])
            cursor.execute(query_editPromocode)
            mysql.connection.commit()
            cursor.close()
            return None
        except:
            cursor.close()
            return None

class deletePromocode(Resource):
    def post(self):
        try:
            parser.add_argument("Code")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            print("Here")
            query_deletePromocode = " DELETE FROM promocode WHERE Code = '{}';".format(args['Code'])
            cursor.execute(query_deletePromocode)
            mysql.connection.commit()
            cursor.close()
            print("Here")
            return 1
        except:
            cursor.close()
            return None

class getSuppliers(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            query_getSuppliers = " Select * From supplier"
            cursor.execute(query_getSuppliers)
            allSuppliers = cursor.fetchall()
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if (allSuppliers == ()):
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertListOfListsToJson(cursor, allSuppliers)

class getCategories(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            query_getCategories = " Select * From Category"
            cursor.execute(query_getCategories)
            allCategories = cursor.fetchall()
            mysql.connection.commit()
        except:
            # Error from the Database Side
            # If the query is mis-spelled or there's no table called category or if there is no database already
            cursor.close()
            return None
        if (allCategories == ()):
            # If no tuples(records) yet in category table
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertListOfListsToJson(cursor, allCategories)

class getProducts_SalesManView(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            query_getProducts = " Select * From Product"
            cursor.execute(query_getProducts)
            allProducts = cursor.fetchall()
            print(allProducts)
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if (allProducts == ()):
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertListOfListsToJson(cursor, allProducts)

class addCategory(Resource):
    def post(self):
        try:
            parser.add_argument("Name")
            parser.add_argument("CategoryImage")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_insertCategory = " insert into theonlinestore.Category (Name, CategoryImage) values ('{}','{}');".format(args["Name"],args["CategoryImage"])
            print("before")
            print(query_insertCategory)
            cursor.execute(query_insertCategory)
            print("after query" )
            mysql.connection.commit()
            cursor.close()
            print("Finishing addCategory")
            return 1
        except:
            cursor.close()
            print("In excpet")
            #Category couldn't be added because a one with the same name already exists
            return None

class addSupplier(Resource):
    def post(self):
        try:
            parser.add_argument("Name")
            parser.add_argument("Email")
            parser.add_argument("PhoneNumber")
            args = parser.parse_args()

            cursor = mysql.connection.cursor()
            query_insertSupplier = " insert into Supplier (Name, Email, PhoneNumber) values ('{}','{}',{});".format(args["Name"],args["Email"],args["PhoneNumber"])
            cursor.execute(query_insertSupplier)
            mysql.connection.commit()
            cursor.close()
            print("Finishing addSupplier")
            return 1
        except:
            cursor.close()
            print("In excpet")
            #Supplier couldn't be added because a one with the same email or password already exists
            return None

class getLimitedProducts(Resource):
    def get(self):
        try:
            print("At the start")
            cursor = mysql.connection.cursor()
            query_getLimitedProducts = "Select p.ID, p.Quantity, s.PhoneNumber, s.Email, s.Id, p.Name as Name, s.Name as SupplierName From Product AS p,supplier AS s where s.Id = p.SupplierID and p.quantity < 10;"
            cursor.execute(query_getLimitedProducts)
            allLimitedProducts = cursor.fetchall()
            print(allLimitedProducts)
            mysql.connection.commit()
        except:
            cursor.close()
            return None
        if (allLimitedProducts == ()):
            cursor.close()
            return None
        else:
            cursor.close()
            return ConvertListOfListsToJson(cursor, allLimitedProducts)

class addProduct(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("CategoryID")
            parser.add_argument("SupplierID")
            parser.add_argument("Name")
            parser.add_argument("Price")
            parser.add_argument("Quantity")
            parser.add_argument("ExpiryDate")
            parser.add_argument("ProductImage")
            parser.add_argument("Description")
            parser.add_argument("Discount")
            parser.add_argument("EndTimeOffer")

            args = parser.parse_args()
            cursor = mysql.connection.cursor()

            #Adding the product
            query_insertProduct = CreateInsertQuery("product",args)
            cursor.execute(query_insertProduct)

            # Getting the product ID
            query_lastInsertedProduct = CreateGetQuery("product",args)
            cursor.execute(query_lastInsertedProduct)
            lastInsertedProduct = cursor.fetchall()
            #lastInsertedProduct[0][0] is the ID pf the recently(last) added product
            ProductId = lastInsertedProduct[0][0]
            print(ProductId)

            #Adding the request
            parser.add_argument("userIDWhoRequested")
            args = parser.parse_args()
            query_insertRequest = "insert into request (SalesManId,ProductId,Quantity) values({},{},{})".format(args["userIDWhoRequested"],ProductId,args["Quantity"])
            cursor.execute(query_insertRequest)

            mysql.connection.commit()

        except:
            cursor.close()
            print("In excpet")
            #Code couldn't be added because it already exists
            return None

        cursor.close()
        return 1

api.add_resource(addSupplier,'/addSupplier')
api.add_resource(addCategory,'/addCategory')
api.add_resource(requestProduct,'/requestProduct')
api.add_resource(getLimitedProducts,'/getLimitedProducts')
api.add_resource(addDiscount,'/addDiscount')
api.add_resource(getProducts_SalesManView,'/getProducts_SalesManView')
api.add_resource(addProduct,'/addProduct')
api.add_resource(getCategories,'/getCategories')
api.add_resource(getSuppliers,'/getSuppliers')
api.add_resource(deletePromocode, '/deletePromocode')
api.add_resource(getPromocodes,'/getPromocodes')
api.add_resource(addPromocode,'/addPromocode')
api.add_resource(signup_addCustomer,'/addCustomer')
api.add_resource(signup_addEmployee,'/addEmployee')
api.add_resource(login_getCustomer,'/getCustomer')
api.add_resource(login_getEmployee,'/getEmployee')


 ######################################## Hala  ###########################################################

@app.route("/deliveryman",methods=['GET'])
def GetUndeliveredOrders():
    cursor = mysql.connection.cursor()
    cursor.execute("select  FirstName, SecondName , city ,StreetName , theonlinestore.order.Id from customer  , theonlinestore.order where customer.ID like CustomerId and DeliveryManId  Is  Null")
    Order_table=cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    order_list = []
    for row in Order_table:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        order_list.append(d)
    json_string = json.dumps(order_list)
    mysql.connection.commit()
    cursor.close()

    return json_string

@app.route("/MyOrders",methods=['POST'])
def GetMyOrders():
    parser.add_argument("Id")
    args=parser.parse_args()
    cursor =mysql.connection.cursor()
    sql="select  FirstName,SecondName, Governorate,City,StreetName,BuildingNumber,AppartmentNumber,PhoneNumber,TotalPayment,theonlinestore.order.Id   from customer  ,theonlinestore.order where customer.ID like CustomerId and IsDelivered=0 and DeliveryManId = {} ;".format(args["Id"])
    cursor.execute(sql)
    MyOrders=cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    order_list = []
    for row in MyOrders:
        d = {}
        for i in range (len (field_names)):
            d[field_names[i]] = row[i]
        order_list.append(d)

    json_string = json.dumps(order_list)
    mysql.connection.commit()
    cursor.close()

    return json_string

@app.route("/DeliverOrder",methods=['POST'])
def DeliverOrder():
    parser.add_argument('DMId')
    parser.add_argument('OrderId')
    args=parser.parse_args()
    cursor=mysql.connection.cursor()
    sql="UPDATE `theonlinestore`.`order` SET `DeliveryManId` = {} WHERE (`Id` = {});".format(args['DMId'],args['OrderId'])
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return "200"

@app.route("/MarkOrderDelivered",methods=['POST'])
def MarkOrderDelivered():
    parser.add_argument('OrderId')
    args=parser.parse_args()
    cursor=mysql.connection.cursor()
    sql="UPDATE `theonlinestore`.`order` SET `IsDelivered` = '1' WHERE (`Id` = {});".format(args['OrderId'])
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()
    return "200"

#################################### Marim Naser ################################################################
#Home page 
# Best Seller products
@app.route('/BestproductsHome', methods=['GET'])
def BestSellerProducts_View():
    cursor= mysql.connection.cursor()
    cursor.execute("select * from product where Frequency > 15 ")
    Best_products= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in Best_products:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
         
        objects_list.append(d)
    json_string = json.dumps(objects_list)
    mysql.connection.commit()
    cursor.close()
    return json_string
# Prodcuts with offers
@app.route('/OffersHome', methods=['GET'])
def OfferProducts_View():
    cursor= mysql.connection.cursor()
    cursor.execute("select * from theOnlinestore.product where Discount > 0 ")
    Offers= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in Offers:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
         
        objects_list.append(d)
    json_string = json.dumps(objects_list)
    mysql.connection.commit()
    cursor.close()
    return json_string
###################################################
# Categories
@app.route('/Categories', methods=['GET'])
def GetCategories_View():
    cursor= mysql.connection.cursor()
    cursor.execute("select * from Category")
    Categories= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in Categories:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
         
        objects_list.append(d)
    json_string = json.dumps(objects_list)
    mysql.connection.commit()
    cursor.close()
    return json_string
# Products of each Category
@app.route('/CategoryProducts', methods=['POST'])
def GetCategoryProducts_View():
    parser.add_argument("CID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("select * from Product where CategoryID = {} ; ".format(args["CID"]))
    products= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in products:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()   
    cursor.close()
    return json_string
    
## ADD TO CART 
@app.route('/addtocart', methods=['POST'])
def ADD_TO_CART():
    parser.add_argument("proID")
    parser.add_argument("custID")
    parser.add_argument("QTY")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("insert into AddToCart values ({},{},{});".format(args["proID"],args["custID"],args["QTY"]))
    mysql.connection.commit()
    cursor.close()
    return "1"

 # Get Prodcuts in the cart
@app.route('/getCart', methods=['POST'])
def GetCartProducts_View():
    parser.add_argument("CID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("select Distinct * from Product,AddToCart where Product.ID = AddToCart.ProductId AND AddToCart.CustomerId = {} ; ".format(args["CID"]))
    products= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in products:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()   
    cursor.close()
    return json_string
# qty ++
@app.route('/incQTY', methods=['POST'])
def INC_QTY():
    parser.add_argument("proID")
    parser.add_argument("custID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("update AddToCart set Quantity = Quantity+1 where AddToCart.ProductId = {} AND AddToCart.CustomerId = {} AND (select Quantity from Product where Product.ID = {}) >= AddToCart.Quantity ;".format(args["proID"],args["custID"],args["proID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"
# qty --
@app.route('/decQTY', methods=['POST'])
def DEC_QTY():
    parser.add_argument("proID")
    parser.add_argument("custID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("update AddToCart set Quantity = Quantity-1 where AddToCart.ProductId = {} AND AddToCart.CustomerId = {} AND AddToCart.Quantity > 1  ;".format(args["proID"],args["custID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"  
# get qty of a certrain product (used in cart card)    
@app.route('/getqty', methods=['POST'])
def GetQty():
    parser.add_argument("proID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("select Quantity from Product where ID = {} ;".format(args["proID"]))
    products= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in products:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()   
    cursor.close()
    return json_string        
# delete product from cart
@app.route('/deletefromcart', methods=['POST'])
def Delete_From_Cart():
    parser.add_argument("proID")
    parser.add_argument("custID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("delete from AddToCart where AddToCart.ProductId = {} AND AddToCart.CustomerId = {} ;".format(args["proID"],args["custID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"        
# Making Order
#  1- get price and qty and discount of products in the cart to get total payment
@app.route('/priceQTYget', methods=['POST'])
def GetTotalPayment_View():
    parser.add_argument("CID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("select Price,Discount, AddToCart.Quantity from Product,AddToCart where AddToCart.CustomerId = {} AND product.ID= addtocart.ProductId;".format(args["CID"]))
    products= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in products:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()   
    cursor.close()
    return json_string   
#   2- insert new order 
@app.route('/makeorder', methods=['POST'])
def Make_Order():
    parser.add_argument("custID")
    parser.add_argument("totpay")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("INSERT INTO `theonlinestore`.`order` (`CustomerId`, `TotalPayment`) VALUES ('{}', '{}');".format(args["custID"],args["totpay"]))
    mysql.connection.commit()
    cursor.close()
    return "1"
#   3- delete all products in the cart ONLY for this customer
@app.route('/emptycart', methods=['POST'])
def Empty_Cart():
    parser.add_argument("CID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("Delete from theonlinestore.AddToCart where theonlinestore.AddToCart.CustomerId = {};".format(args["CID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"
# Get all orders of this customer
@app.route('/getorder', methods=['POST'])
def GetOrders_View():
    parser.add_argument("CID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("select * from theonlinestore.order where theonlinestore.order.CustomerId = {} ; ".format(args["CID"]))
    orders= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in orders:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()   
    cursor.close()
    return json_string    
    
#feed back delivery man    
@app.route('/feedbackdm', methods=['POST'])
def Feedback_DM():
    parser.add_argument("myrate")
    parser.add_argument("MSG")
    parser.add_argument("custID")
    parser.add_argument("dmID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    qurey="INSERT INTO `theonlinestore`.`feedbackdelivery` (`Rate`, `Message`, `CustomerId`, `DeliveryManId`) VALUES ({}, '{}', {}, {});".format( args["myrate"],args["MSG"],args["custID"],args["dmID"])
    print(qurey)
    cursor.execute(qurey)
    mysql.connection.commit()
    cursor.close()
    return "1" 
##Commment productttttttttt
@app.route('/commentproduct', methods=['POST'])
def Comment_Product():
    parser.add_argument("MSG")
    parser.add_argument("custID")
    parser.add_argument("proID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("INSERT INTO `theonlinestore`.`commentproduct` (`Message`, `CustomerId`, `ProductId`) VALUES ('{}', {}, {});".format(args["MSG"],args["custID"],args["proID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"   
## Show Commments on certain productttttttttt
@app.route('/showcommentproduct', methods=['POST'])
def Show_Comment_Product():
    parser.add_argument("PROID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("SELECT Message FROM commentproduct where ProductId = {};".format(args["PROID"]))
    comments= cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    objects_list = []
    for row in comments:
        d = {}
        for i in range (len(field_names)):
            d[field_names[i]] = row[i]
        objects_list.append(d)    
    json_string = json.dumps(objects_list)  
    mysql.connection.commit()
    cursor.close()
    cursor.fetchall()
    return json_string
## rattte productttttttttt
@app.route('/rateproduct', methods=['POST'])
def Rate_Product():
    parser.add_argument("myrate")
    parser.add_argument("custID")
    parser.add_argument("proID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("INSERT INTO `theonlinestore`.`rateproduct` (`Rate`, `CustomerId`, `ProductId`) VALUES ({}, {}, {});".format(args["myrate"],args["custID"],args["proID"]))
    mysql.connection.commit()
    cursor.close()
    return "1"    
## show rattte  ofproductttttttttt
@app.route('/showrateproduct', methods=['POST'])
def Show_Rate_Product():
    parser.add_argument("PROID")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    print("here 1")
    query="select AVG(Rate) from rateproduct where rateproduct.ProductId = '{}';".format(args["PROID"])
    cursor.execute(query)
    print(query)
    avg= cursor.fetchall()  
    print(avg)
    mysql.connection.commit()   
    cursor.close()
    return json.dumps(avg)           
## Make Complaint 
@app.route('/complaint', methods=['POST'])
def Make_Complaint():
    parser.add_argument("custID")
    parser.add_argument("MSG")
    args=parser.parse_args()
    cursor= mysql.connection.cursor()
    cursor.execute("insert into complaint (CustomerId,Message)values ({},'{}');".format(args["custID"],args["MSG"]))
    mysql.connection.commit()
    cursor.close()
    return "1"        

if __name__ == '__main__':
    app.run(debug=True)
