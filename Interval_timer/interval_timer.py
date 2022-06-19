import time
# from threading import Timer
# Need a timer to show overall time
# need a timer for warmups and cooldowns
# remaining time and elapse time

# variables for interval timers
starting_countdown = int(input('Countdown: '))
number_of_sets = int(input('number of sets: '))
seconds_per_set = int(input('Seconds: '))
seconds_of_rest = int(input('Rest: '))

# variables to count time
sets_done = 0
elapsed_time = sets_done * seconds_per_set + seconds_of_rest
remaining_time = (seconds_per_set + seconds_of_rest) * number_of_sets / elapsed_time
# audio
sound = [3500, 500]

# Simple starting countdown will need to test for other use case statements and value errors
for number in reversed(range(0, starting_countdown)):
    time.sleep(1)
    if number > 0:
        print(f'Timer will start in {number}')
    else:
        print('GO!')

# Looping through the number of sets within the workout

for sets in range(number_of_sets):
    for number in range(seconds_per_set):
        # doing this to account for our 0 index
        time.sleep(1)
        print(f'exercise {number + 1}')
        print(sets_done)

    sets_done = sets_done + 1

    if sets + 1 == number_of_sets:
        print('Done')
        break
    else:
        print('Rest')
        for number in range(seconds_of_rest):
            time.sleep(1)
            print(f'rest: {number + 1}')
