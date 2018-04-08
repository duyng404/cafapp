from flask import Flask, render_template
from app import app, cas
from flask_cas import login_required

@app.route('/')
@login_required
def default():
    print('someone access this page')
    print('dir=',dir(cas))
    print('vars:')
    attrs = vars(cas)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    return render_template('index.html',username=cas.username)
