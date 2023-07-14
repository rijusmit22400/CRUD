from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_ACCOUNT'] = 'riju'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mummyandpapa2020'
app.config['MYSQL_DATABASE_DB'] = 'bank'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
