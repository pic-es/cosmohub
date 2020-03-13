import logging

from flask import Blueprint
from flask import jsonify
from flask.views import MethodView
from webargs.flaskparser import use_args

from ..database import model
from ..database.model import db
from ..database.session import transactional_session

log = logging.getLogger(__name__)

users_blp = Blueprint("users", __name__)


class UsersView(MethodView):
    def get(self, id_=None):
        with transactional_session(db.session, read_only=True) as session:
            if id_:
                user = model.User.query.get_or_404(id_)
                return jsonify(model.UserSchema().dump(user)), 200
            else:
                users = model.User.query.all()
                return jsonify(model.UserSchema(many=True).dump(users)), 200

    @use_args(model.UserSchema)
    def post(self, user):
        with transactional_session(db.session) as session:
            session.add(user)
            session.flush()
            return jsonify(model.UserSchema().dump(user)), 201

    def delete(self, id_):
        with transactional_session(db.session) as session:
            user = model.User.query.with_for_update().get_or_404(id_)
            session.delete(user)
            return "", 200


users_view = UsersView.as_view("users")

users_blp.add_url_rule("/users", view_func=users_view, methods=["GET", "POST"])
users_blp.add_url_rule("/users/<int:id_>", view_func=users_view, methods=["GET", "DELETE"])
