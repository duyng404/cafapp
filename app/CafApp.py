from flask import render_template, redirect, url_for, jsonify
from app import api, app, cas, db, DEV
from flask_cas import login_required
from app.data.user import User
from app.api.order import OrderApi
from app.api.user import UserApi, UsersApi
from app.api.permissions import our_login_required


api.add_resource(OrderApi, '/api/v1/orders/<int:order_id>')
api.add_resource(UserApi, '/api/v1/users/<string:username>')
api.add_resource(UsersApi, '/api/v1/users')


def getUserInfo():
    """ Returns the info for the currently logged in user."""
    if (cas.token and cas.username and cas.attributes):
        a = {
                'username' : cas.username,
                'full_name' : '{} {}'.format(
                    cas.attributes.get('cas:givenName', ''),
                    cas.attributes.get('cas:surname', ''))
                #'student_id' : cas.attributes.get('cas:id')
                }
        return a
    elif DEV:
        a = {
                'username' : 'dev_mode',
                'full_name' : 'Dev Mode',
                'is_admin' : True
                #'student_id' : 0
                }
        return a
    else:
        return None


@app.route('/')
def landing_UI():
    userinfo = getUserInfo()
    return render_template('landing.html',user=userinfo)

@app.route('/apitest')
@our_login_required
def apitest_UI():
    return

@app.route('/order')
@our_login_required
def ordering_UI():
    userinfo = getUserInfo()
    # first off, check if user is in the database
    caller = User.query.filter_by(username=userinfo['username']).first()
    if caller is None:
        # if user is not in database, create it first
        print(userinfo)
        u = User(**userinfo)
        print(u)
        db.session.add(u)
        db.session.commit()
        # after adding to db, reload current route
        return redirect(url_for('ordering_UI'))
    else:
        # if user already in database, show the ordering UI
        return render_template('order.html',user=userinfo)

@app.route('/profile')
@our_login_required
def profile_UI():
    userinfo = getUserInfo()
    return render_template('profile.html',user=userinfo)

@app.route('/menu')
def menu_UI():
    userinfo = getUserInfo()
    return render_template('menu.html',user=userinfo)

@app.route('/about')
def about_UI():
    userinfo = getUserInfo()
    return render_template('about.html',user=userinfo)

#@app.errorhandler(Exception)
#def error_UI(e):
#    # TODO: make the error pages look bootyfull
#    return
