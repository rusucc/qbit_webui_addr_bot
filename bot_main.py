from basic_bot import *
import time


# Keeps script running and getting new updates
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            # Gets the last update, so next request comes only with new messages
            last_update_id = get_last_update_id(updates) + 1
            update_treatment(updates)
        time.sleep(3)


# Python main or modular check
if __name__ == '__main__':
    main()
