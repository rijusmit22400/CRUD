import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple
from json import JSONEncoder
import requests
import json


apibasedurl = 'http://localhost:8080'
#apibasedurl = 'http://localhost:8090'

class Account:
	id =0
	name=""
	amount=0.0
	def __init__(self,row):
		self.id = row["id"]
		self.name = row["name"]
		self.amount = row["amount"]

def toAccount(json):
	acnt = json.loads(json, object_hook=customAccountDecoder)
	return acnt

def customAccountDecoder(account):
    return namedtuple('X', account.keys())(*account.values())


@app.route('/new_user')
def add_user_view():
	return render_template('add.html')
		
@app.route('/add', methods=['POST'])
def add_user():
	try:		
		_id = request.form['inputid']
		_id = int(_id)
		_name = request.form['inputname']
		_amount = request.form['inputamount']
		_amount = float(_amount)
		# validate the received values
			#do not save password as a plain text
			# save edits
		url = apibasedurl + '/add'

		params = {
				'id':_id,
				'name':_name,
				'amount': _amount
			}
		resp = requests.post(url=url,json=params)
		row = resp.json() 
		flash('account added successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
		
@app.route('/')
def users():
	try:
		url =  apibasedurl + '/'
		resp = requests.get(url=url)
		data = resp.json() 
		#table = toAccount(data)
		#table.border = True
		return render_template('users.html', table=data)
	except Exception as e:
		print(e)
	finally:
		print('done')

@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		url = apibasedurl + '/edit/' + str(id)

		params = dict(
			id=id
		)
		resp = requests.get(url=url)
		row = resp.json() 
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)


@app.route('/update', methods=['POST'])
def update_user():
	try:		
		_id = request.form['inputid']
		_id = int(_id)
		_name = request.form['inputname']
		_amount = request.form['inputamount']
		_amount = float(_amount)
		# validate the received values
		if _name and _id and _amount and request.method == 'POST':
			#do not save password as a plain text
			# save edits
			url = apibasedurl + '/update'

			params = {
				'id':_id,
				'name':_name,
				'amount': _amount
			}
			resp = requests.post(url=url,json=params)
			row = resp.json() 
			flash('account updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)


		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		id_=id
		parm = {'id' : id_}
		url = apibasedurl + '/delete/' + str(id)
		resp=requests.post(url,json=parm)
		flash('account deleted successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
