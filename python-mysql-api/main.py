import json
import pandas as pd
import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash


class Account:
	id =0
	name=""
	amount=0.0
	def __init__(self,row):
		self.id = row["id"]
		self.name = row["name"]
		self.amount = row["amount"]
		
@app.route('/add', methods=['POST'])
def add_user():
	try:
		response = request.get_json()
		_id = int(response['id'])
		_name = response['name']
		_amount = float(response['amount'])
		# validate the received values
			# save edits
		sql = "INSERT INTO account (id, name, amount) VALUES(%s, %s, %s)"
		data = (_id,_name,_amount)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		n_data = ('id','name','amount')
		n_data = dict(zip(n_data,data))
		conn.commit()
		flash('account updated successfully!')
		#return redirect('/')
		result = json.dumps(n_data, indent=2, sort_keys=True)
		return result 
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM account")
		rows = cursor.fetchall()
		df = pd.DataFrame(rows)
		result  =df.to_json(orient="records")
		return result
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		#return "ok"+str(id)
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM account WHERE id=%s", id)
		row = cursor.fetchone()
		amnt =Account(row)
		result = json.dumps(amnt.__dict__, indent=2, sort_keys=True)
		if row:
			return result
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
		print("ok")

@app.route('/update', methods=['POST'])
def update_user():
	try:	
		json2 = request.get_json()	
		_id = json2['id']
		_id = int(_id)
		_name = json2['name']
		_amount = json2['amount']
		_amount = float(_amount)
		# validate the received values
		if _name and _id and _amount and request.method == 'POST':
			#do not save password as a plain text
			# save edits
			sql = "UPDATE account SET name=%s, amount=%s WHERE id=%s"
			data = (_name, _amount, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('account updated successfully!')
			result = json.dumps(data, indent=2, sort_keys=True)
			return result 
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
	try:
		resp=request.get_data()
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(f"SELECT * FROM account WHERE id={id}")
		addm=cursor.fetchone()
		cursor.execute("DELETE FROM account WHERE id=%s", (id))
		parm=('id','name','amount')
		parm=dict(zip(parm,addm))
		js=json.dumps(parm)
		conn.commit()
		return js

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
