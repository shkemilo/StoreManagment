import csv
import io
import json
from redis import Redis

from Commons.exceptions import BadRequestException
from Store.Warehouse.configuration import Configuration


class WarehouseController():

    def update(file):
        if(file == None):
            raise BadRequestException("Field file is missing.")

        content = file.stream.read().decode("utf-8")
        stream = io.StringIO(content)
        reader = csv.reader(stream)

        products = WarehouseController.getProductsFromFile(reader)

        with Redis(host=Configuration.REDIS_HOST) as redis:
            for product in products:
                redis.rpush(Configuration.REDIS_PRODUCTS_LIST, json.dump(product))
            
    def getProductsFromFile(reader):
        products = []
        currentLine = 0
        for row in reader:
            product = {}

            if(len(row) != 4):
                raise BadRequestException(
                    "Incorrect number of values on line {}.".format(currentLine))

            product['categories'] = row[0].split('|')
            product['name'] = row[1]

            if(not row[2].isdigit()):
                raise BadRequestException(
                    "Incorrect quantity on line {}.".format(currentLine))

            product['quantity'] = int(row[2])

            if(not row[3].replace('.', '', 1).isdigit()):
                raise BadRequestException(
                    "Incorrect price on line {}.".format(currentLine))

            product['price'] = float(row[3])

            products.append(product)
            currentLine += 1

        return products
