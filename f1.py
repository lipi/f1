
import sys

from collections import defaultdict

LAPS = 70

base_slow=81.564
base_fast=81.545

increase_slow=0.0614
increase_fast=0.0435

def lap_time(lap, fast=True):
    if fast:
        return base_fast + lap * increase_fast        
    else:
        return base_slow + lap * increase_slow

class Tire():
    
    def __init__(self, fast=True) -> None:
        self.fast = fast
        self.laps = 0
        
    def lap_time(self):
        self.laps += 1
        return lap_time(self.laps, self.fast)

def race(pit_lap_a, pit_lap_b, debug=False):
    """
    Parameters: pit laps for each driver
    
    Dirver A starts with fast tire, Driver B starts with slow tire. At pit stops they change to different tire.
    
    For each lap the drivers lap time is calculated, and the total race time is recorded.
    
    The leader can not be overtaken, i.e. the follower can't have better race time than the leader.
    
    The follower can only overtake when the leader takes a pit stop.
    
    Print the lap times, race times for each player at each lap. Mark the leader. Mark pit stops.
    
    Return the winner (who was the leader in the last lap).
    """
    race_time_a = 0
    race_time_b = 0
    
    has_a_pitted = False
    has_b_pitted = False
    
    leader = 'A'
    
    driver_a_tire = Tire(fast=True)
    driver_b_tire = Tire(fast=False)
    
    for lap in range(1, LAPS+1):
        lap_time_a = driver_a_tire.lap_time()
        lap_time_b = driver_b_tire.lap_time()
        
        race_time_a += lap_time_a
        race_time_b += lap_time_b
        
        # leader can not be overtaken
        if leader == 'A':
            race_time_b = max(race_time_b, race_time_a)
        if leader == 'B':
            race_time_a = max(race_time_b, race_time_a)
        
        # who pitted?
        if lap == pit_lap_a:
            race_time_a += 20
            driver_a_tire = Tire(fast=False)
            
        if lap == pit_lap_b:
            race_time_b += 20
            driver_b_tire = Tire(fast=True)
        
        # leader changed?
        if race_time_a > race_time_b:
            leader = 'B'
        if race_time_a < race_time_b:
            leader = 'A'

        if debug:
            pit_a = ['  ', 'P:'][(lap == pit_lap_a)]
            pit_b = ['  ', 'P:'][(lap == pit_lap_b)]
            print(f'{lap} : {lap_time_a:.3f} {lap_time_b:.3f} -- {pit_a} {race_time_a:.3f}  {pit_b} {race_time_b:.3f} {leader}')

    return leader

def check_all():
    results = defaultdict(dict)
    for pit_lap_a in range(1,LAPS+1):
        print(f'Driver A pit lap: {pit_lap_a:02d} ', end='')
        for pit_lap_b in range(1, LAPS+1):
            winner = race(pit_lap_a, pit_lap_b)
            print(winner, end='')
            results[pit_lap_a][pit_lap_b] = winner
        print()
    
    return results
            

if __name__ == '__main__':
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except IndexError:
        check_all()
        exit()
        
    winner = race(a, b, debug=True)
    print(f"Winner: {winner}")
    
    '''
Driver B pit lap:             1         2
                     12345678901234567890
A driver pit lap: 01 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
A driver pit lap: 02 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
    '''