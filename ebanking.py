from japronto import Application, RouteNotFoundException

from crud_service import *
from customerAPI import *

api = Application()

router = api.router

# Product Router
router.add_route("/customer/list", CustomerResource.list_customer, method="GET")
router.add_route("/customer/{customer_id}", CustomerResource.get_customer, method="GET")
router.add_route("/customer/create", CustomerResource.create_customer, method="POST")
router.add_route("/customer/update/{customer_id}", CustomerResource.update_product, method="PUT")
router.add_route("/customer/delete/{customer_id}", CustomerResource.delete_product, method="DELETE")


api.run(port=8000)