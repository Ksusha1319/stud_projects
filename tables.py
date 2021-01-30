from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('ID', show=True)
    ticket = Col('Ticket')
    nickname = Col('Nickname')
    service_login = Col('ServiceLogin')
    incident_type = Col('Incident type')
    incident_date = Col('Incident date')
    game_type = Col('Game')
    comment = Col('Comment')
    username = Col('Username')
    priority = Col('Priority')
    status = Col('Status')
    resolution = Col('Resolution')
    comment_soc = Col('SOC comment')
    created_date = Col('Creation date', show=True)
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))