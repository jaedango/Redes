import time
Timeout = 10
end_time = time.time() + Timeout
while time.time() < end_time:
    res = input('What is your input: ')
    try:
        # process user input
        print(res)
    except:
        print('There was an error, try again.')
    else:
        break