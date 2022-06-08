from curses.ascii import isdigit
from Commons.exceptions import BadRequestException
from Store.Commons.models import Category, Order, Product, ProductOrder, database


class CustomerController ():

    def search(productName, categoryName):
        if (productName == None):
            productName = ""
        productSearchPattern = "%{}%".format(productName)
        products = Product.query.filter(
            Product.name.like(productSearchPattern)).all()

        if (categoryName == None):
            categoryName = ""
        categorySearchPattern = "%{}%".format(categoryName)
        categories = Category.query.filter(
            Category.name.like(categorySearchPattern)).all()

        return {"categories": [category.name for category in categories], "products": [product.to_dict() for product in products]}

    def order(requests):
        if(requests == None or len(requests) == 0):
            raise BadRequestException("Field requests is missing.")

        productOrders = []
        requestCount = 0
        for request in requests:
            productId = request['id']
            if(productId == None):
                raise BadRequestException(
                    "Product id is missing for request number {}.".format(requestCount))

            productQuantity = request['quantity']
            if(productQuantity == None):
                raise BadRequestException(
                    "Product quantity is missing for request number {}.".format(requestCount))

            if(not isdigit(productId)):
                raise BadRequestException(
                    "Invalid product id for request number {}.".format(requestCount))

            if(not isdigit(productQuantity)):
                raise BadRequestException(
                    "Invalid product quantity for request number {}.".format(requestCount))

            product = Product.query.filter(Product.id == productId).first()
            if(product == None):
                raise BadRequestException(
                    "Invalid product for request number {}.".format(requestCount))

            productOrders.append(
                {'id': productId, 'quantity': productQuantity})

        order = Order()
        database.session.add(order)
        database.session.commit(order)

        for productOrderData in productOrders:
            productOrder = ProductOrder(
                productId=productOrderData['id'], orderId=order.id, quantity=productOrderData['quantity'])
            database.session.add(productOrder)
        database.session.commit()

        return order.id
