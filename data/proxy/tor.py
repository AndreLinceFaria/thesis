from selenium import webdriver
import time, subprocess
import socket, socks

class TorProxy():

    def __init__(self):
        self.browser_path = raw_input("Type the path for Tor browser executable:\n")
        self.phantom_path = raw_input("Enter the path to PhantomJS:\n")
        self.driver = None
        self.proc = None
        self.default_socket = socket.socket

    def start_tor(self):
        service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]
        self.proc = subprocess.Popen(self.browser_path)
        self.driver = webdriver.PhantomJS(executable_path=self.phantom_path, service_args=service_args)
        time.sleep(20)
        print("==================================\n=> TOR is running on port 9150...\n==================================\n ")

    def stop_tor(self):
        #recover default socket
        socket.socket = self.default_socket
        self.driver.close()
        self.proc.kill()

    def proxy_requests(self):
        # Configuration
        SOCKS5_PROXY_HOST = '127.0.0.1'
        SOCKS5_PROXY_PORT = 9150

        # Set up a proxy
        socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
        socket.socket = socks.socksocket
        print("==================================\n"
              "=> Using TOR on " + SOCKS5_PROXY_HOST + ":" + str(SOCKS5_PROXY_PORT) + "...\n"
                "==================================\n ")

if __name__ == "__main__":
    tor = TorProxy()
    tor.start_tor()