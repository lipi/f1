
import sys

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
    
    for lap in range(1, LAPS+1):
        lap_time_a = lap_time(lap, fast=(not has_a_pitted))
        lap_time_b = lap_time(lap, fast=has_b_pitted)
        
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
            
        if lap == pit_lap_b:
            race_time_b += 20
        
        # leader changed?
        if race_time_a > race_time_b:
            leader = 'B'
        else:
            leader = 'A'

        if debug:
            pit_a = ['  ', 'P:'][(lap == pit_lap_a)]
            pit_b = ['  ', 'P:'][(lap == pit_lap_b)]
            print(f'{lap} : {lap_time_a:.3f} {lap_time_b:.3f} -- {pit_a} {race_time_a:.3f}  {pit_b} {race_time_b:.3f} {leader}')

    return leader

if __name__ == '__main__':
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except IndexError:
        print(f'Usage: {sys.argv[0]} <pit_lap_A> <pit_lap_B>')
        exit()
        
    winner = race(a, b, debug=True)
    print(f"Winner: {winner}")