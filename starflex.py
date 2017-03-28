import requests
import time
import json


class star_client:
    def __init__(self, host, port='80'):
        self.host = host
        self.port = port

    @staticmethod
    def build_json(data):
        '''
        Builds a dummy json

        :param data:
        :return:
        '''
        print " sending data:" + data
        json = '{ "data1": \"' + data + '\"}'
        return json

    def post_msg(self, message, end_point='/'):
        '''
        post any messge to an enpoing
        :param message: messsage string to send to endpoint
        :param end_point: default value is root '/'
        :return:
        '''
        json = self.build_json("123")

        url = 'http://' + self.host + ':' + self.port + '/' + end_point

        headers = {'Connection ': 'keep-alive',
                   # 'Content-Length': '170',
                   'Content-Type': 'application/json',
                   }

        r = requests.post(url, data=json, headers=headers)
        print r.status_code
        print r.text

    def put_msg(self, msg=None, end_point='/'):
        '''
        puts someting to an endpoint
        :param msg: this is optional body to sent in the put request
        :param end_point: default value
        :return:
        '''
        if not (end_point.startswith('/')):
            end_point = '/' + end_point

        if self.port.__eq__('80'):
            url = 'http://' + self.host + end_point
        else:
            url = 'http://' + self.host + ':' + self.port + end_point
        print "URL : " + url
        r = requests.put(url)
        print r.status_code
        print r.text

    def del_msg(self, end_point='/'):
        '''
        Deletet post action to kill a process in the starflex
        :param end_point:
        :return:
        '''
        if not (end_point.startswith('/')):
            end_point = '/' + end_point

        if self.port.__eq__('80'):
            url = 'http://' + self.host + end_point
        else:
            url = 'http://' + self.host + ':' + self.port + end_point
        print "URL : " + url
        r = requests.delete(url)
        print r.status_code
        print r.text

    def get_msg(self, end_point='/'):
        '''
        simple get to read endpoint
        :param end_point: path to resource
        :return: nothing
        '''
        if not (end_point.startswith('/')):
            end_point = '/' + end_point

        if self.port.__eq__('80'):
            url = 'http://' + self.host + end_point
        else:
            url = 'http://' + self.host + ':' + self.port + end_point
        print "URL : " + url
        r = requests.get(url, stream=True)
        print r.status_code
        # print r.text

    def listen_during(self, time_window, end_point='/', rounds=0):
        '''
        listen an endpoint for a given period of time
        :param time_window: period of time waitn got
        :param end_point:
        :param rounds:
        :return:
        '''
        if not (end_point.startswith('/')):
            end_point = '/' + end_point

        if self.port.__eq__('80'):
            url = 'http://' + self.host + end_point
        else:
            url = 'http://' + self.host + ':' + self.port + end_point
        print "URL : " + url
        r = requests.get(url, stream=True)
        print r.status_code
        print 'waiting time: ' + str(time_window)
        self.start_listening(r.iter_lines(), rounds, time_window)

    def start_listening(self, iterable, rounds, time_window):
        '''
        Consumes iterable connected to an starflex reader
        :param iterable:
        :param rounds:
        :param time_window:
        :return:
        '''
        print iterable

        t0 = time.time()

        ## list of dictionaries
        tags = {}

        with open('start_stream.txt', 'a') as f:
            print 'process started...'
            for line in iterable:
                # filter out keep-alive new lines
                current_time = time.time() - t0
                # print 'current time:  ' + str(current_time)
                if time_window < current_time:
                    break
                if line:
                    decoded_line = line.decode('utf-8')
                    # if it a json payload
                    if decoded_line.startswith("data: "):
                        x = json.loads(decoded_line[6:])  # decodes json
                        # if it is a new round counter increments
                        if x['type'] == "RoundStart":
                            rounds += 1
                            # print 'Round: ' + str(rounds)

                        # if it is a tag data increment counter in tags' dictionary
                        if x['type'] == "TagReadData":
                            # the tag ID is found in the data field
                            tag_key = x['data']
                            # if the tags dict contains the key then
                            # we increment counter
                            if tags.has_key(tag_key):
                                cnt = tags.get(tag_key)
                                tags[tag_key] = cnt + 1
                            else:
                                # however if
                                tags[tag_key] = 1
                                # print tags

                    f.write(decoded_line + "\n")
                    # print decoded_line
        print 'time ended'
        print '========================='
        print '========================='
        print '        Summary'
        print '========================='
        print '========================='
        print 'Total rounds: ' + str(rounds)
        print 'List of tags: ' + str(tags)
        print 'Unique: ' + str(len(tags))


    def wait_first_round(self, time_window, end_point='/'):
        '''
        Waits for first round message and then starts to read the stream
        :param time_window: time period where it listens the messages
        :param end_point:
        :return:
        '''
        if not (end_point.startswith('/')):
            end_point = '/' + end_point

        if self.port.__eq__('80'):
            url = 'http://' + self.host + end_point
        else:
            url = 'http://' + self.host + ':' + self.port + end_point
        print "URL : " + url
        r = requests.get(url, stream=True)
        print r.status_code

        print 'Waiting for round....'
        iterable = r.iter_lines()
        for line in iterable:
            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                # if it a json payload
                if decoded_line.startswith("data: "):
                    x = json.loads(decoded_line[6:])  # decodes json
                    # if it is a new round counter increments
                    if x['type'] == "RoundStart":
                        print 'Found first round.'
                        break
        if time_window > 0:
            self.start_listening(iterable=iterable, rounds=1, time_window=time_window)
        return iterable
