import starflex


client = starflex.star_client('10.100.1.71')
# wait for fist round and listen by 10 seconds
client.wait_first_round(time_window=10, end_point='/rfid/events')
# Stop time
client.del_msg(end_point='/rfid/activeProgram')


# print r.content
