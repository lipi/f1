
from f1 import TireSet


def test_print_tires():
    ts = TireSet()
    for lap in range(1,71):
        print(f'{lap:02d} {ts.current_tire} {ts.lap_time():.3f} {ts.pit_lap()}')
    assert(True)


if __name__ == '__main__':
    test_print_tires()