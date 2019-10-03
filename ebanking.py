from japronto import Application, RouteNotFoundException

from customerAPI import *

api = Application()

router = api.router

# router.add_route("/customer/list", CustomerResource.list_customer, method="GET")
router.add_route("/address/list", AddressResource.list_address, method="GET")
router.add_route("/address/{address_id}", AddressResource.getaddressbyid, method="GET")
router.add_route("/address/create", AddressResource.address_create, method="POST")
router.add_route("/address/update/{address_id}", AddressResource.address_update, method="PUT")

api.run(port=8000)