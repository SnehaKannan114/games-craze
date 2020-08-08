import csv
import time
import threading
import signal


#time limit in seconds
time_limit = 40

def character_getter():
    character_list = []
    with open('characters.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0]:
                    character_list.append(row[0])
                    line_count += 1
    # print(character_list)
    import random
    n = random.randint(0,len(character_list)-1)
    return character_list[n]

class pointsKeeper:
    player_dict = None
    def __init__(self):
        self.player_dict = {}
    def set_player_count(self, n):
        for i in range(n):
            self.player_dict[i] = {}
    def set_player_info(self):
        for i in range(len(self.player_dict)):
            self.player_dict[i]['name'] = input('Enter the name of player {}: '.format(i+1))
            self.player_dict[i]['score'] = 0
        print(self.player_dict)
    def get_player_stats(self):
        return self.player_dict

def buzzer():
    wait_for_input = input('Buzzer me if player guessed correctly\n')

class TimeOutException(Exception):
    def __init__(self, message, errors=None):
        super(TimeOutException, self).__init__(message)
        self.errors = errors

def signal_handler(signum, frame):
    raise TimeOutException("Times Up!")

def guesser():
    try:
        foo = input('Buzzer me if player guessed correctly\n')
        return True
    except:
        return False

def dumsharades():
    print('################################################################################')
    print('\t\t\t\tWelcome to Dumsharades')
    print('################################################################################')
    n = int(input('Enter number of players: '))
    points_keeper = pointsKeeper()
    points_keeper.set_player_count(n)
    points_keeper.set_player_info()
    round_no = 0
    while True:
        print('################################################################################')
        print('\t\t\t\tRound: {}'.format(round_no+1))
        print('################################################################################')
        stats = points_keeper.get_player_stats()
        for players in stats:
            character = character_getter()
            print('Character generated for {}: {}'.format(stats[players]['name'], character))
            input('Press any key to start the round\n')
            guessed = False
            try:
                guessed = False
                start_time = time.time()
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(time_limit)
                guessed = guesser()
            except Exception as exc:
                print(exc)
                print("Sorry time is up")
            finally:
                if not guessed:
                    print('Times Up!')
                else:
                    elapsed_time = float(time.time() - start_time)
                    elapsed_time = round(elapsed_time, 2)
                    print('You took {} seconds'.format(elapsed_time))
                    points = (time_limit - elapsed_time)/10
                    stats[players]['score'] = stats[players]['score'] + points
                    print('You got {} points'.format(points))
                input()
                print('--------------------------------------------------------------------------')
                signal.alarm(0)
        points_string = ''
        print('SCORE:')
        for players in stats:
            points_string = points_string + stats[players]['name'] + ': ' + str(stats[players]['score']) + '\n'
        print(points_string)
        round_no = round_no + 1

dumsharades()