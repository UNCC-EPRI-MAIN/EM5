import signal
from xbox360controller import Xbox360Controller


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))

def triggered():
    print("trig")

def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

def apress(button):
    print("a")
def bpress(button):
    print("b")
def ypress(button):
    print("y")
def xpress(button):
    print("x")

try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_a.when_pressed = apress
        controller.button_a.when_released = on_button_released
                # Button b events
        controller.button_b.when_pressed = bpress
        controller.button_b.when_released = on_button_released
                # Button y events
        controller.button_y.when_pressed = ypress
        controller.button_y.when_released = on_button_released
                # Button x events
        controller.button_x.when_pressed = xpress
        controller.button_x.when_released = on_button_released

        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved

        signal.pause()
except KeyboardInterrupt:
    pass