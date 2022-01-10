import _thread as thread

test = thread.allocate_lock()


def test_func(id, data):
    test.acquire()
    print(f"Thread {id}: {data}")
    test.release()


for i in range(0, 5):
    thread.start_new_thread(test_func, (i, "Dav!"))