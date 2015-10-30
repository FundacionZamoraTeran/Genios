from sugar3.activity import activity
from genios import MainClass
from sugargame.canvas  import PygameCanvas

class GenioActivity(activity.Activity):

    def __init__(self, handle):
        super(GenioActivity, self).__init__(handle)

        # Build the activity toolbar.
        #self.build_toolbar()

        # Create the game instance.
        self.game = MainClass()

        # Build the Pygame canvas.
        self._pygamecanvas = PygameCanvas(self)
        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

        # Start the game running.
        self._pygamecanvas.run_pygame(self.game.main)

    #def read_file(self, path):
    #    self.game.read_file(path, use_sugar=True):

    #def write_file(self, path):
    #    self.game.write_file(path, use_sugar=True):
