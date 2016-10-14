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
        CustomerId = request.json['id']
        Customer = db.customers.find_one({'_id':ObjectId(CustomerId)})
        CustomerDetail = {
                'device':Customer['device'],
                'ip':Customer['ip'],
                'username':Customer['username'],
                'password':Customer['password'],
                'port':Customer['port'],
                'id':str(Customer['_id'])
                }
        print CustomerDetail
        return json.dumps(CustomerDetail)
    except Exception, e:
        return str(e)

@application.route('/updateCustomer',methods=['POST'])
def updateCustomer():
    try:
        CustomerInfo = request.json['info']
        CustomerId = CustomerInfo['id']
        device = CustomerInfo['device']
        ip = CustomerInfo['ip']
        username = CustomerInfo['username']
        password = CustomerInfo['password']
        port = CustomerInfo['port']

        db.customers.update({'_id':ObjectId(CustomerId)},{'$set':{'device':device,'ip':ip,'username':username,'password':password,'port':port}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getCustomerList",methods=['POST'])
def getCustomerList():
    try:
        customers = db.customers.find()
        
        CustomerList = []
        for Customer in customers:
            print Customer
            print "#######"
            CustomerItem = {
                    'device':Customer['device'],
                    'ip':Customer['ip'],
                    'username':Customer['username'],
                    'password':Customer['password'],
                    'port':Customer['port'],
                    'id': str(Customer['_id'])
                    }
            CustomerList.append(CustomerItem)
    except Exception,e:
        return str(e)
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
        CustomerId = request.json['id']
        db.customers.remove({'_id':ObjectId(CustomerId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='0.0.0.0')

