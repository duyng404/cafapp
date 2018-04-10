from app import cas, db
from app.data.user import User
from app.api.permissions import valid_call
from flask import abort
from flask_restful import Resource, reqparse


class UserApi(Resource):
    @valid_call
    def get(self, username):
        caller = User.query.filter_by(username=cas.username)
        if cas.username != username or not caller.is_admin:
            abort(403)
        return User.query.filter_by(username=username).one().serialize


class UsersApi(Resource):

    @valid_call
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('phonenumber', required=True)
        parser.add_argument('is_admin', type=bool, default=False)

        args = parser.parse_args()

        u = User(**args)
        db.session.add(u)
        db.session.commit()
