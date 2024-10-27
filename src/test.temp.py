from constants import DESTINATION_TOWER, SOURCE_TOWER
from towers_of_hanoi import Move
from utils import Queue

# was sind "Types"
class Type:
    def __init__(self):
        pass

wert = Type()

variable: Type = wert

# int -> integer -> ganze Zahl
x: int = 1
y: int = 2.5

move: Move = Move(SOURCE_TOWER, DESTINATION_TOWER)




# erstelle eine `Move` Warteschlange
move_queue: Queue[Move] = Queue()

def animate(move: Move):
    pass

# bis die Move Warteschlange leer ist
while not move_queue.empty():
    # hole den nächsten Move aus der Warteschlange
    next_move = move_queue.dequeue()
    # animiere den Move (vereinfacht)
    animate(next_move)

