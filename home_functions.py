import urllib.request
import urllib.error
from ping3 import ping


def grab_ip():
    """
    This function requests a webservice to return the current external IP of the running machine.

    Args:
        Takes no args

    Returns:
        Current public IP address of server.

    Raises:
        Service not running: Raises an exception.
    """
    try:
        external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    except urllib.error.URLError:
        external_ip = "Error. Either connection is down or webservice 'http://ident.me' is offline."
    return external_ip


def check_connected(destination):
    """
        This function pings an ip address to check if it's connected to the local network.

        Args:
            destination (str): IP address of the device.

        Returns:
            bool: True if successful, False otherwise.
        """
    if ping(destination):
        return True
    else:
        return False


def check_home():
    # TODO ping every smartphone at home to see who is connected, and by that infer who is home at the moment as return
    return 0


def none():
    return 'Comando inválido.'


# This function works as a switch/case structure based on the message received
def function_selector(text):
    switcher = {
        "ip": grab_ip,
        "home": check_home
    }

    # function_name = switcher.get(text, lambda: none)
    function_name = switcher.get(text, none)
    return_text = function_name()
    return return_text


def save_ip_file(ip_addr):
    ip_file = open('current_ip.txt', 'w+')
    ip_file.write(ip_addr)
    ip_file.close()

    return 'IP stored on file.'


def read_ip_file():
    try:
        ip_file = open('current_ip.txt')
    except IOError:
        print('File does not exist')
        return 0
    ip = ip_file.read()

    return ip
