import starflex


client = starflex.star_client('10.100.1.71')
# Start
client.put_msg(end_point='/rfid/activeProgram/basic')
# Listening for 10 seconds
client.listen_during(10, end_point='/rfid/events')
# Stop time
client.del_msg(end_point='/rfid/activeProgram')


# print r.content
