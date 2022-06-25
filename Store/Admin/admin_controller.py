from Store.Commons.models import Category, Product, ProductOrder, database


class AdminController():

    def productStatistics():
        data = {}
        for productOrder in ProductOrder.query.all():
            productId = productOrder.productId

            if not productId in data:
                data[productId] = {'sold': productOrder.received,
                                   'waiting': productOrder.requested - productOrder.received}
            else:
                data[productId]['sold'] += productOrder.received
                data[productId]['waiting'] += (
                    productOrder.requested - productOrder.received)

        statistics = []
        for productId in data:
            statistics.append({
                'name': Product.query.filter(Product.id == productId).first().name,
                'sold': data[productId]['sold'],
                'waiting': data[productId]['waiting']
            })

        return statistics

    def categoryStatistics():
        data = {}
        for category in Category.query.all():
            data[category.name] = 0

        for productOrder in ProductOrder.query.all():
            product = Product.query.filter(
                Product.id == productOrder.productId).first()

            for category in product.categories:
                data[category.name] += productOrder.received

        sortedData = sorted(
            data.items(), key=lambda item: (-item[1], item[0]))

        return [item[0] for item in sortedData]
