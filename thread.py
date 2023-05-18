import threading
import time


class MyClass:
    resource = 0

    def function1(self):
        while True:
            print(self.resource)
            time.sleep(5)

    def function2(self):
        while True:
            self.resource += 1
            time.sleep(5)




