from japronto import Application, RouteNotFoundException

from customerAPI import *

api = Application()

router = api.router

# router.add_route("/customer/list", CustomerResource.list_customer, method="GET")
router.add_route("/address/list", CustomerResource.list_address, method="GET")
router.add_route("/address/{address_id}", CustomerResource.getaddressbyid, method="GET")


api.run(port=8000)