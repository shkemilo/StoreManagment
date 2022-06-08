from Store.Commons.models import Product, ProductOrder


class AdminController():

    def productStatistics():
        data = {}
        for productOrder in ProductOrder.query.all():
            productId = productOrder.productId
            if productId in data:
                data[productId] = {'sold': productOrder.received,
                                   'waiting': productOrder.requested - productOrder.received}
            else:
                data[productId]['sold'] += productOrder.received
                data[productId]['waiting'] += (
                    productOrder.requested - productOrder.received)

        statistics = []
        for productId in data:
            statistics.append({
                'name': Product.query.filter(Product.id == productId).first(),
                'sold': data[productId]['sold'],
                'waiting': data[productId]['waiting']
            })

        return statistics

    def compareCategoryData(item1, item2):
        if item1[1] < item2[1]:
            return -1
        elif item1[1] > item2[1]:
            return 1
        elif item1[0] < item2[0]:
            return -1
        elif item1[0] > item2[0]:
            return 1
        else:
            return 0

    def categoryStatistics():
        data = {}
        for productOrder in ProductOrder.query.all():
            product = Product.query.filter(
                Product.id == productOrder.productId).first()
            for category in product.categories:
                if category in data:
                    data[category] += productOrder.received
                else:
                    data[category] = productOrder.received

        sortedData = sorted(
            data.items(), key=AdminController.compareCategoryData)

        return sortedData
