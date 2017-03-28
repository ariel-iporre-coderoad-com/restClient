import starflex
import thread


def kill_after(time_window):
    # Stop time
    print 'thread 1: waiting to kill...'
    starflex.time.sleep(time_window)
    client.del_msg(end_point='/rfid/activeProgram')
    print 'thread 1: stop'


# wait for fist round and listen by 10 seconds
def listen(iterable, time_window):
    client.start_listening(iterable, 1, time_window)


# Start killing thread
time_window = 10
client = starflex.star_client('10.100.1.71')
iterable = client.wait_first_round(time_window=0, end_point='/rfid/events')
try:
    thread.start_new_thread(kill_after, (time_window - 2,))
    thread.start_new_thread(listen, (iterable, time_window,))
except:
    print "Error: unable to start thread"
while True:
    pass
