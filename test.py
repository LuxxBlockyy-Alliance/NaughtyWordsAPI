import time
import requests


class Countdown:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.time = None

    def count_start(self):
        self.start_time = time.time()

    def count_stop(self):
        self.end_time = time.time()

    def counted_time(self):
        if self.end_time is None:
            return "Countdown was never started or completed."
        else:
            self.time = time.gmtime(self.end_time - self.start_time)
            self.time = time.strftime("%H:%M:%S:%MS", self.time)
            return self.time


def send_data(message):
    url = "http://195.62.46.112:3331/api"
    headers = {'Content-Type': 'application/json'}
    data = {'message': f'{message}'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f'Error: {response.json()}')


while True:
    message = input("Enter message: ")
    countdown = Countdown()
    countdown.count_start()
    send_data(message.lower())
    countdown.count_stop()
    print(f"{countdown.counted_time()}")
