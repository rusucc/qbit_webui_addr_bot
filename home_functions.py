import urllib.request
from ping3 import ping


def grab_ip():
    external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    return external_ip


def check_connected(destination):
    if ping(destination):
        return True
    else:
        return False


def check_home():

    return 0


def none():
    return 'Comando inválido.'


# This function works as a Switch/case based on the message received
def function_selector(text):
    switcher = {
        "ip": grab_ip,
        "IP": grab_ip,
        'home': check_home
    }

    function_name = switcher.get(text, lambda: none)
    return_text = function_name()
    return return_text


