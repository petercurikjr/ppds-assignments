from fei.ppds import Thread, Semaphore
from time import sleep
from random import randint


class Shared:
    def __init__(self):
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)

        self.customer_at_barber = -1


def customer_func(customer_id, shared):
    shared.customer.signal()
    shared.barber.wait()

    shared.customer_at_barber = customer_id
    print("zakaznik %2d: striha ma barber" % customer_id)
    sleep(randint(1, 5) / 10)

    shared.customer_done.signal()
    print("zakaznik %2d: hotovo staci dakujem" % customer_id)
    shared.barber_done.wait()


def barber_func(shared):
    shared.customer.wait()
    shared.barber.signal()

    print("barber: striham zakaznika %2d" % shared.customer_at_barber)
    sleep(randint(1, 5) / 10)

    shared.customer_done.wait()
    shared.barber_done.signal()
    print("barber: dovidenia zakaznik %2d dakujem" % shared.customer_at_barber)


def main():
    shared = Shared()
    customer_num = 10
    customers = []

    barber = Thread(barber_func, shared)

    for i in range(customer_num):
        customers.append(Thread(customer_func, i, shared))

    for t in customers:
        t.join()
    barber.join()


if __name__ == "__main__":
    main()
