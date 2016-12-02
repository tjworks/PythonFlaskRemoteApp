from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('mongodb:27017')
db = client.mydb1

@application.route("/addCustomer",methods=['POST'])
def addCustomer():
    try:
        json_data = request.json['info']
        # json_data:  { device: "", ip: "", username:"", password:"" }
        db.customers.insert(json_data);        
        return jsonify(status='OK',message='inserted successfully')
    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showCustomerList():
    return render_template('list.html')

@application.route('/getCustomer',methods=['POST'])
def getCustomer():
    try:
        CustomerId = request.json['customer_id']
        Customer = db.customers.find_one({'customer_id': CustomerId})
        CustomerDetail = {
                'customer_id':Customer['customer_id'],
                'name':Customer['name'],
                'phone':Customer['phone'],                
                'address':Customer['address'],                
                'email':Customer['email']                
                }
        print "*** ", CustomerDetail
        return json.dumps(CustomerDetail)
    except Exception, e:
        print(e)
        return str(e)

@application.route('/updateCustomer',methods=['POST'])
def updateCustomer():
    try:
        CustomerInfo = request.json['info']
        customer_id = CustomerInfo['customer_id']
        name = CustomerInfo['name']
        phone = CustomerInfo['phone']
        address = CustomerInfo['address']
        email = CustomerInfo['email']
        
        db.customers.update({'customer_id': customer_id},{'$set':{'customer_id':customer_id,
            'name': name,
            'phone': phone,
            'address':address,
            'email':email}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getCustomerList",methods=['POST'])
def getCustomerList():
    try:
        customers = db.customers.find();

        CustomerList = []
        for Customer in customers:
            print "####### !!!"
            print Customer
            
            CustomerItem = {
                    'customer_id':Customer['customer_id'],
                    'name':Customer['name'],
                    'phone':Customer['phone'],
                    'address':Customer['address'],
                    'email':Customer['email']                    
                    }
            CustomerList.append(CustomerItem)
    except Exception,e:
        print(e)
        return str(e)
    print("=====1")
    print json.dumps(CustomerList)
    print("=====2")
    return json.dumps(CustomerList)

@application.route("/execute",methods=['POST'])
def execute():
    try:
        CustomerInfo = request.json['info']
        ip = CustomerInfo['ip']
        username = CustomerInfo['username']
        password = CustomerInfo['password']
        command = CustomerInfo['command']
        isRoot = CustomerInfo['isRoot']
        
        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK',message=resp)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))

@application.route("/deleteCustomer",methods=['POST'])
def deleteCustomer():
    try:
        CustomerId = request.json['customer_id']
        db.customers.remove({'customer_id': CustomerId })
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='0.0.0.0')

