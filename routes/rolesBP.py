from flask import Blueprint

from controllers.roleController import save,find_all

role_blueprint = Blueprint('role_bp', __name__)
role_blueprint.route('/',methods=['GET'])(find_all)
role_blueprint.route('/add-role',methods=['POST'])(save)