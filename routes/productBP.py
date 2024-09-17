from flask import Blueprint
from controllers.productController import save,find_all,find_top_selling_product

product_blueprint = Blueprint('product_bp',__name__)
product_blueprint.route("/add-product",methods=['POST'])(save)
product_blueprint.route('/',methods=['GET'])(find_all)
product_blueprint.route('/top-selling',methods=['GET'])(find_top_selling_product)