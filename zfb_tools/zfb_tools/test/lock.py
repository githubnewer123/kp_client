import threading
import time
import datetime

# 创建一个互斥锁
mutex = threading.Lock()

# 共享资源
shared_resource = 0

# 定义一个函数，模拟线程对共享资源的操作
def thread_function(name):
    global shared_resource
    print(f"{datetime.datetime.now()} Thread {name}: starting")
    for _ in range(5):
        # 获取互斥锁
        mutex.acquire()
        try:
            print(f"{datetime.datetime.now()} Thread {name}: updating shared resource")
            shared_resource += 1
            print(f"{datetime.datetime.now()} Thread {name}: shared resource is now {shared_resource}")
        finally:
            # 释放互斥锁
            mutex.release()
        time.sleep(1)
    print(f"{datetime.datetime.now()} Thread {name}: finishing")

# 创建并启动两个线程
thread1 = threading.Thread(target=thread_function, args=(1,))
thread2 = threading.Thread(target=thread_function, args=(2,))

thread1.start()
thread2.start()

# 等待所有线程完成
thread1.join()
thread2.join()

print("Main thread is done.")
