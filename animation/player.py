"""Control buttons and progress bar for the animation."""

import matplotlib.animation as animation
import mpl_toolkits.axes_grid1
import matplotlib.widgets


class Player(animation.FuncAnimation):
    """Animation player."""
    def __init__(self, fig, update_func, fargs=None, mini=0, maxi=100, **kwargs):
        self.fig = fig
        self.update_func = update_func
        self.min = mini
        self.max = maxi
        self.runs = True
        self.i = 0

        self.setup()
        animation.FuncAnimation.__init__(self, self.fig, self.update_slider, frames=self.run(), fargs=fargs, **kwargs)

    def run(self):
        """Generates the animation frames."""
        while self.runs:
            self.i += 1
            if self.max >= self.i >= self.min:
                yield self.i
            else:
                self.play_pause()
                yield self.i - 1

    def play_pause(self, event=None):
        """Pauses if the animation is playing or plays if the animation is paused."""
        if self.runs:
            self.runs = False
            self.event_source.stop()
            self.button_play_pause.label.set_text('$\u25B6$')
        else:
            self.runs = True
            self.event_source.start()
            self.button_play_pause.label.set_text('||')

    def oneforward(self, event=None):
        """Travels one frame forward."""
        self.onestep()

    def onebackward(self, event=None):
        """Travels one frame backwards."""
        self.onestep(forwards=False)

    def onestep(self, forwards=True):
        """One frame in either direction based on the "forwards" boolean argument.
        True for forward travel False for backward travel.
        """
        if self.max > self.i > self.min:
            self.i = self.i + forwards - (not forwards)
        elif self.i == self.min and forwards:
            self.i += 1
        elif self.i == self.max and not forwards:
            self.i -= 1
        self.update_func(self.i)
        self.slider.set_val(self.i)
        self.fig.canvas.draw_idle()

    def setup(self):
        """Creates the Buttons and the slider and assigns them to their event functions"""
        playerax = self.fig.add_axes([0.125, 0.92, 0.709, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)
        ppax = divider.append_axes("right", size="100%", pad=0.05)
        ofax = divider.append_axes("right", size="100%", pad=0.05)
        sliderax = divider.append_axes("right", size="2000%", pad=0.07)

        self.button_oneback = matplotlib.widgets.Button(playerax, label='$\u29CF$')
        self.button_play_pause = matplotlib.widgets.Button(ppax, label='||')
        self.button_oneforward = matplotlib.widgets.Button(ofax, label='$\u29D0$')
        self.slider = matplotlib.widgets.Slider(sliderax, '', self.min, self.max, valinit=self.i)
        self.slider.valtext.set_visible(False)

        self.button_oneback.on_clicked(self.onebackward)
        self.button_play_pause.on_clicked(self.play_pause)
        self.button_oneforward.on_clicked(self.oneforward)
        self.slider.on_changed(self.update_frame)

    def update_frame(self, i):
        """Updates the animation frame based on the value of the slider"""
        self.i = int(i)
        self.update_func(self.i)

    def update_slider(self, i):
        """Updates the position of the slider"""
        self.slider.set_val(i)
