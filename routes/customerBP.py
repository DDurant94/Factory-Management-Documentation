from flask import Blueprint
from controllers.customerController import save, find_all,lifetime_value

customer_blueprint = Blueprint('customer_bp',__name__)
customer_blueprint.route('/add-customer',methods=['POST'])(save)
customer_blueprint.route('/',methods=['GET'])(find_all)
customer_blueprint.route('/customer-lifetime-value')(lifetime_value)
