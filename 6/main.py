from fei.ppds import Thread, Mutex, Semaphore, Event
from time import sleep
from random import randint

N = 10


class Counter:
    def __init__(self):
        self.waiting_customers = 0
        self.waiting_room_capacity = 5
        self.mutex = Mutex()
        self.queue = []

    def incoming_customer(self, customer_id):
        self.mutex.lock()
        if self.waiting_customers == self.waiting_room_capacity:
            print("zakaznik %2d: odchadzam. je tu plno" % customer_id)
        else:
            print("zakaznik %2d: prisiel som. cakam v cakarni" % customer_id)
            self.queue.append(customer_id)
            self.waiting_customers += 1
        self.mutex.unlock()

    def outcoming_customer(self, customer_id):
        self.mutex.lock()
        print("zakaznik %2d: odchadzam z holicstva" % customer_id)
        self.waiting_customers -= 1
        self.queue.pop(0)
        self.mutex.unlock()


class Shared:
    def __init__(self):
        self.customer = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.customer_at_barber = Mutex()
        self.customer_at_barber_ready = Event()

        self.barber = Semaphore(0)
        self.barber_done = Semaphore(0)

        self.customer_id_at_barber = None
        self.counter = Counter()


def customer_func(customer_id, shared):
    while True:
        sleep(randint(1, 2))
        shared.counter.incoming_customer(customer_id)

        if customer_id not in shared.counter.queue:
            continue

        shared.customer_at_barber.lock()
        shared.customer.signal()
        shared.barber.wait()

        shared.customer_id_at_barber = customer_id
        shared.customer_at_barber_ready.signal()
        print("zakaznik %2d: striha ma barber" % customer_id)
        sleep(randint(1, 5) / 10)

        shared.customer_at_barber_ready.clear()
        shared.customer_done.signal()
        print("zakaznik %2d: uz ma nestrihaj staci" % customer_id)
        shared.barber_done.wait()
        shared.customer_at_barber.unlock()

        shared.counter.outcoming_customer(customer_id)


def barber_func(shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        shared.customer_at_barber_ready.wait()
        print("barber: striham zakaznika %2d" % shared.customer_id_at_barber)
        sleep(randint(1, 5) / 10)

        shared.customer_done.wait()
        shared.barber_done.signal()
        print("barber: na ziadost zakaznika %2d koncim" % shared.customer_id_at_barber)


def main():
    shared = Shared()

    customers = []
    barber = Thread(barber_func, shared)

    for i in range(N):
        customers.append(Thread(customer_func, i, shared))

    for t in customers:
        t.join()
    barber.join()


if __name__ == "__main__":
    main()
