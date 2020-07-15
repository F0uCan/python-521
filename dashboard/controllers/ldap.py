
import logging

import flask
import ldap3
import hashlib

blueprint =  flask.Blueprint('ldap',__name__)

def get_ldap_connection():
    
    user ='cn=admin,dc=dexter,dc=com,dc=br'
    password='4linux' 
    server =  ldap3.Server('ldap://localhost:389')

    try:
        return ldap3.Connection(server, user, password, auto_bind=True)
    except Exception as err:
        logging.error(f'Falha na conexão com ldap: \n{err}')
    
def create_user(conn, first_name, last_name, email, password):
    try:

        cn = 'uid={},dc=dexter,dc=com,dc=br'.format(email)
        
        object_class = [
            'top',
            'person',
            'organizationalPerson',
            'inetOrgPerson',
            'posixAccount'
        ]
        
        user = {
            'cn': first_name,
            'sn': last_name,
            'mail': email,
            'uidNumber': '123',
            'gidNumber': '123',
            'uid': email,
            'homeDirectory': '/home/{}'.format(email),
            'userPassword': password
        }

        conn.add(cn, object_class, user)

        return True

    except Exception as err:

        logging.error(f'Falha ao localizar e-mail: \n{err}')

        return False

def find_user_by_email(email, conn):    
    try:      
        conn.search(
            'uid={},dc=dexter,dc=com,dc=br'.format(email),
            '(objectClass=person)',
            attributes=[
                'sn',
                'userPassword'
            ]
        )
    except Exception as err:
        logging.error(f'Falha ao localizar e-mail: \n{err}')


    return conn.entries[0] if len(conn.entries) > 0 else None

def verify_password(user, password):
    return password == user.userPassword.value.decode()


@blueprint.route('/sign-in', methods=['GET','POST'])
def sign_in():

    conn = get_ldap_connection()
    
    if conn and flask.request.method == 'POST':
       
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        user = find_user_by_email(email, conn)    

        if not user:

            logging.info(f'Usuário e-mai\t{email} não encontrado!')
            flask.flash(f'Usuário e-mai\t{email} não encontrado' , 'warning')

        elif verify_password(user, password):

            logging.info(f'Usuário e-mai\n{email} autenticado com sucesso!')
            flask.flash(f'Usuário e-mai\n{email} autenticado com sucesso!' , 'success')

            flask.session['authenticated'] = True
            return flask.redirect('/')
  
    context = {
        'public_route': True
    }

    return flask.render_template('ldap.html', context=context)


@blueprint.route('/sign-out', methods=['GET', 'POST'])
def sign_out():

    try:       
        del flask.session['authenticated']
    except KeyError as err:
        logging.error(f'Falha ao no logout: \n{err}')
    return flask.redirect('/')

@blueprint.route('/sign-up', methods=[ 'GET', 'POST' ])
def sign_up():

    conn = get_ldap_connection()
    
    if conn and flask.request.method == 'POST':
        
        first_name = flask.request.form.get('first_name')
        last_name = flask.request.form.get('last_name')
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        if create_user(conn, first_name, last_name, email, password):
            return flask.redirect('/')
        else:
            flask.flash('Falha ao cadastrar novo usuário' , 'warning')
            return flask.redirect('/sign-up')

    context = {
        'public_route': True
    }

    return flask.render_template('sign-up.html', context=context)