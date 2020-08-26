import time
try:
    import minibot # import minibot in your project
except:# You might have to use (when Minibot is in a subdirectory)
    from Minibot import minibot


if __name__ == '__main__':
    # 1. Do your work
    print("Let's do some work. Counting to 10...")
    for i in range(10):
        print(i)
        time.sleep(0.1)

    print("All work done. Calling minibot...")
    # 2. Handle the Telegram messaging
    mb = minibot.MiniBot() # create a minibot instance
    mb.send_message("All work done.") # send a notification
    print("Telegram message sent.")
