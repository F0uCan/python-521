import flask
import requests

from services.authentication import login_required


ACCESS_TOKEN = 'vdsGWU4mhYL8ih5nUCbU'

blueprint =  flask.Blueprint('gitlab',__name__)

def get_users():

    res = requests.get('http://localhost:8001/api/v4/users/', headers={
        'PRIVATE-TOKEN': ACCESS_TOKEN
    }) 
    
    if res.status_code != 200:
        return[]

    def fn(u):
        return {
            'email': u.get('email'),
            'name':  u.get('name'),
            'status': u.get('state'),
            'is_admin': u.get('is_admin')
        }
    return [fn(u) for u in res.json()]



def get_projects():

    res = requests.get('http://localhost:8001/api/v4/projects/', headers={
        'PRIVATE-TOKEN': ACCESS_TOKEN
    }) 
    
    if res.status_code != 200:
        return[]

    def fn(p):
        return{
            'name': p.get('name'),
            'ssh_link': p.get('ssh_link'),
            'owner': p.get('owner').get('name'),
            'path': p.get('path')
        }
    return [fn(p) for p in res.json()]



@blueprint.route('/gitlab', methods=['GET'])
@login_required
def gitlab_action():
    context = {
        'user':get_users(),
        'projects':get_projects()
    }
    return flask.render_template('gitlab.html', context=context)