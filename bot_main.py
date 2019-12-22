from basic_bot import *
import time


# Keeps script running and getting new updates
def main():

    # Generate IP file and send to my chat
    current_ip = home_functions.grab_ip()
    home_functions.save_ip_file(current_ip)

    start_up_message(current_ip)  # Send current IP

    # Start timer, this is gonna be used to check current again every 10 min
    seconds_timer = 0

    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            # Gets the last update, so next request comes only with new messages
            last_update_id = get_last_update_id(updates) + 1
            update_treatment(updates)

        # At every new loop at while, add more 3 seconds to timer
        seconds_timer = seconds_timer + 3

        # When timer counter gets to 10 min, check IP again to see if changed
        if seconds_timer >= 600:
            current_ip = home_functions.grab_ip()
            # If returns IP correctly, check if it changed from previous check. If so, rewrite file with new IP, and
            # send it again to chat.
            if 'Error' not in current_ip:
                if home_functions.grab_ip() != home_functions.read_ip_file():
                    home_functions.save_ip_file(current_ip)
                    send_message('Your home IP has changed. Sending current IP', ID)
                    send_message(current_ip, ID)
            else:
                send_message('An error occurred during IP grabbing', ID)
            seconds_timer = 0
        time.sleep(3)


# Python main or modular check
if __name__ == '__main__':
    main()
