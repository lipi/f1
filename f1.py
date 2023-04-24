
import sys
from collections import defaultdict
import numpy as np
import itertools
import pickle
from tqdm import tqdm

LAPS = 70

base_soft=81.564
base_medium=81.545

increase_soft=0.0614
increase_medium=0.0435

'''
Driver B pit lap:             1         2
                     12345678901234567890
A driver pit lap: 01 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
A driver pit lap: 02 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
'''

class MediumTire():
    
    def __init__(self) -> None:
        self.laps = 0
        
    def __str__(self) -> str:
        return 'M'
        
    def lap_time(self):
        self.laps += 1
        return base_medium + self.laps * increase_medium

class SoftTire():
    
    def __init__(self) -> None:
        self.laps = 0

    def __str__(self) -> str:
        return 'S'  
    
    def lap_time(self):
        self.laps += 1
        return base_soft + self.laps * increase_soft


class TireSet():
    
    def __init__(self, tires={ 
            0: MediumTire(),
            20: SoftTire(),
            40: MediumTire()
        }) -> None:
        '''
        Tireset with pit laps and tires
        
        tires: dictionary of pit laps as keys and tire instances as values
        '''
        self.tires = tires
        self.laps = 0
        self.current_tire = self.tires[self.laps]
        
    def lap_time(self):
        '''
        Return lap time based on the current tire.
        Change to new tire at end of lap if there is a pit stop.
        '''
        time = self.current_tire.lap_time()
        self.laps += 1
        
        # see if tire change is needed
        try:
            self.current_tire = self.tires[self.laps]
        except KeyError:
            # current tire remains as is
            pass
        return time
    
    def pit_lap(self):
        '''Return true if current lap is a pit lap'''
        return self.laps in self.tires.keys()

def race(
    tires_a=TireSet({0: MediumTire(), 20: SoftTire(), 40: MediumTire()}),
    tires_b=TireSet({0: SoftTire(), 30: MediumTire(), 50: MediumTire()}),
    debug=False):
    """
    Parameters: tire set for each driver
    
    Dirvers start with first tire in their set. At pit stops they change to a new tire.
    
    For each lap the drivers lap time is calculated, and the total race time is recorded.
    
    The leader can not be overtaken, i.e. the follower can't have better race time than the leader.
    
    The follower can only overtake when the leader takes a pit stop.
    
    Print the lap times, race times for each player at each lap. Mark the leader. Mark pit stops.
    
    Return the winner (who was the leader in the last lap).
    """
    race_time_a = 0
    race_time_b = 0
    
    leader = 'A'
    
    if debug:
        print('lap  lap_A      lap_B           total_A     total_B  leader')
        print('-----------------------------------------------------------')
    for lap in range(1, LAPS+1):
        lap_time_a = tires_a.lap_time()
        lap_time_b = tires_b.lap_time()
        
        race_time_a += lap_time_a
        race_time_b += lap_time_b
        
        # leader can not be overtaken
        if leader == 'A':
            race_time_b = max(race_time_b, race_time_a)
        if leader == 'B':
            race_time_a = max(race_time_b, race_time_a)
        
        # who pitted?
        if tires_a.pit_lap():
            race_time_a += 20
            
        if tires_b.pit_lap():
            race_time_b += 20
        
        # leader changed?
        if race_time_a > race_time_b:
            leader = ' B'
        if race_time_a < race_time_b:
            leader = 'A '

        if debug:
            a = str(tires_a.current_tire)
            b = str(tires_b.current_tire)
            pit_a = ['  ', 'P:'][tires_a.pit_lap()]
            pit_b = ['  ', 'P:'][tires_b.pit_lap()]
            print(f'{lap:2d} : {lap_time_a:6.3f} ({a}) {lap_time_b:6.3f} ({b})  {pit_a} {race_time_a:8.3f}  {pit_b} {race_time_b:8.3f} {leader}')

    return leader
        
def check_all(debug=False):
    results = np.zeros((LAPS, LAPS, LAPS, LAPS), dtype=np.bool)
    numbers = range(1,LAPS)
    pit_stops_a = itertools.combinations(numbers, 2)
    pit_stops_b = itertools.combinations(numbers, 2)
    total = int(len(numbers)**2 * (len(numbers)-1)**2 / 4)
    quads = itertools.product(pit_stops_a, pit_stops_b)
    for quad in tqdm(quads, total=total):
        (a,b),(c,d) = quad
        winner = race(
            TireSet({0: MediumTire(), a: SoftTire(), b: MediumTire()}),
            TireSet({0: SoftTire(), c: MediumTire(), d: MediumTire()}))
        if debug:
            print(f'Driver A pit laps: {a:2d} {b:2d}  Driver B pit laps: {c:2d} {d:2d} winner: {winner}')
        results[a, b, c, d] = ('A' in winner)
    
    return results

if __name__ == '__main__':
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        c = int(sys.argv[3])
        d = int(sys.argv[4])
    except IndexError:
        results = check_all(debug=False)
        pickle.dump( results, open( "results.p", "wb" ) )
        exit()
        
    winner = race(
        TireSet({0: MediumTire(), a: SoftTire(), b: MediumTire()}),
        TireSet({0: SoftTire(), c: MediumTire(), d: MediumTire()}),
        debug=True)
    print(f"Winner: {winner}")
    
    '''
Driver B pit lap:             1         2
                     12345678901234567890
A driver pit lap: 01 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
A driver pit lap: 02 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
    '''