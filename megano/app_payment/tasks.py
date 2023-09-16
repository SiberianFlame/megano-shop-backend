from rq import Queue
from redis import Redis


redis_conn = Redis()
queue = Queue(connection=redis_conn)

from app_order.models import Order


def func_for_payment(id: int) -> None:
    """
    Func which imitates payment process.
    :param id: Order primary key
    """

    order = Order.objects.get(pk=id)
    order.status = 'Paid'

    for product in order.products.all():
        product.product.count -= product.amount
        product.product.purchases_num += product.amount
        product.product.save()

    order.save()