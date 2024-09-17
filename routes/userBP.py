from flask import Blueprint

from controllers.userController import save,find_all,login

user_blueprint = Blueprint('user_bp', __name__)
user_blueprint.route('/add-user',methods=['POST'])(save)
user_blueprint.route('/',methods=['GET'])(find_all)
user_blueprint.route('/login',methods=['POST'])(login)