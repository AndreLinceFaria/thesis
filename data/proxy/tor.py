from selenium import webdriver
import time, subprocess

class TorProxy():

    def __init__(self):
        self.browser_path = raw_input("Type the path for Tor browser executable:\n")
        self.phantom_path = raw_input("Enter the path to PhantomJs:\n")
        self.driver = None
        self.proc = None

    def start_tor(self):
        service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]
        self.proc = subprocess.Popen(self.browser_path)
        self.driver = webdriver.PhantomJS(executable_path=self.phantom_path, service_args=service_args)
        time.sleep(5)
        print("==================================\n=> TOR is running on port 9150...\n==================================\n ")

    def stop_tor(self):
        self.driver.close()
        self.proc.kill()

if __name__ == "__main__":
    tor = TorProxy()
    tor.start_tor()