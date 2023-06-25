from app_order.models import Order


def adding_information_to_order(order: Order, data: dict):
    """
    Add new information to order from request data
    :param order: Order object
    :param data: Data from request object
    """

    order.deliveryType = data['deliveryType']
    order.paymentType = data['paymentType']
    order.status = data['status']
    order.city = data['city']
    order.address = data['address']
    order.set_total_cost()
    order.status = 'Awaits payment'
    order.fullName = data['fullName']
    order.email = data['email']
    order.phone = data['phone']

    order.save()