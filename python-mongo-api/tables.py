from flask_table import Table, Col, LinkCol
 
class Results(Table):
    #id = Col('id')
    name = Col('Name')
    amount = Col('Amount')
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_account', url_kwargs=dict(id='id'))
