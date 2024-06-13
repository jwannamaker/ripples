from collections import deque

import pyglet
from pyglet.window import key, mouse


class Ripple:
    """ A series of Arcs that get larger, thinner, and darker. """
     # OR [255, 64, 16, 4, 1]

    def __init__(self, x, y, batch):
        self.thickness_delta = deque([10, 6, 3, 2, 1])
        self.radius_delta = deque([10, 28, 77, 216, 600])
        self.color_delta = deque([(255, 255, 255), (191, 191, 191), (128, 128, 128), (64, 64, 64), (0, 0, 0)])

        self.shape = pyglet.shapes.Arc(x, y, self.radius_delta.popleft(),
                                       segments=100,
                                       thickness=self.thickness_delta.popleft(),
                                       color=self.color_delta.popleft(),
                                       batch=batch)

        pyglet.clock.schedule_interval_for_duration(self.update, 1, 5)
        
    def update(self, dt):
        self.shape.radius = self.radius_delta.popleft()
        self.shape.thickness = self.thickness_delta.popleft()
        self.shape.color = self.color_delta.popleft()
        
class RipplesWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__()

        self.ripple_batch = pyglet.graphics.Batch()
        self.ripples = deque(maxlen=4)
        self.label = pyglet.text.Label('Makin ripples in the animation scene Whoop!')

    def on_mouse_press(self, x, y, button, modifiers):
        if mouse.LEFT:
            self.label.text = f'ripple @ {x, y}'
            self.ripples.append(Ripple(x, y, self.ripple_batch))
    
    def on_draw(self):
        self.clear()
        self.label.draw()
        self.ripple_batch.draw()

if __name__ == '__main__':
    window = RipplesWindow()
    pyglet.app.run()