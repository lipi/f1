
import sys
from collections import defaultdict
import cProfile

LAPS = 70

base_slow=81.564
base_fast=81.545

increase_slow=0.0614
increase_fast=0.0435

'''
Driver B pit lap:             1         2
                     12345678901234567890
A driver pit lap: 01 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
A driver pit lap: 02 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
'''

class FastTire():
    
    def __init__(self) -> None:
        self.laps = 0
        
    def __str__(self) -> str:
        return 'Fast'
        
    def lap_time(self):
        self.laps += 1
        return base_fast + self.laps * increase_fast

class SlowTire():
    
    def __init__(self) -> None:
        self.laps = 0

    def __str__(self) -> str:
        return 'Slow'  
    
    def lap_time(self):
        self.laps += 1
        return base_slow + self.laps * increase_slow


class TireSet():
    
    def __init__(self, tires={ 
            0: FastTire(),
            20: SlowTire(),
            40: FastTire()
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
    tires_a=TireSet({0: FastTire(), 20: SlowTire(), 40: FastTire()}),
    tires_b=TireSet({0: SlowTire(), 30: FastTire(), 50: FastTire()}),
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
            leader = 'B'
        if race_time_a < race_time_b:
            leader = 'A'

        if debug:
            pit_a = ['  ', 'P:'][tires_a.pit_lap()]
            pit_b = ['  ', 'P:'][tires_b.pit_lap()]
            print(f'{lap} : {lap_time_a:.3f} {lap_time_b:.3f} -- {pit_a} {race_time_a:.3f}  {pit_b} {race_time_b:.3f} {leader}')

    return leader

def check_all(debug=False):
    results = defaultdict(dict)
    for pit_lap_a in range(1,LAPS+1):
        if debug:
            print(f'Driver A pit lap: {pit_lap_a:02d} ', end='')
        for pit_lap_b in range(1, LAPS+1):
            winner = race(
                TireSet({0: FastTire(), pit_lap_a: SlowTire()}),
                TireSet({0: SlowTire(), pit_lap_b: FastTire()}))
            if debug:
                print(winner, end='')
            results[pit_lap_a][pit_lap_b] = winner
        if debug:
            print()
    
    return results
            

if __name__ == '__main__':
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except IndexError:
        check_all(debug=True)
        exit()
        
    winner = race(a, b)
    print(f"Winner: {winner}")
    
    '''
Driver B pit lap:             1         2
                     12345678901234567890
A driver pit lap: 01 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
A driver pit lap: 02 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    
    '''