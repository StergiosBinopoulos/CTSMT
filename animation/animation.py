"""Animation for the simulation using matplotlib"""

import matplotlib.pyplot as plt
import matplotlib.widgets
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle
import matplotlib.animation as animation
import numpy as np

from .player import Player

def removeaxis(pltobject):
    pltobject.axes.get_xaxis().set_visible(False)
    pltobject.axes.get_yaxis().set_visible(False)
    pltobject.spines['right'].set_visible(False)
    pltobject.spines['bottom'].set_visible(False)
    pltobject.spines['left'].set_visible(False)
    pltobject.spines['top'].set_visible(False)


class AnimateSimulation:
    def __init__(self, env, states, delta_t=0.05, standing_bounds=False, collision_lines=False, standing_spots=False):
        plt.rcParams['toolbar'] = 'None'
        self.standing_bounds = standing_bounds
        self.collision_lines = collision_lines
        self.env = env
        self.walls = self.env.walls
        self.standing_boundaries = env.standing_boundaries
        self.standing_spots_visible = standing_spots
        self.standing_spots = np.asarray([[spot.x, spot.y] for spot in env.standing_spots])
        self.states = states
        self.seats = env.seat_list
        self.dimensions = env.dimensions
        self.obstacle_objects = env.obstacle_objects
        self.doors = env.doors
        self.delta_t = delta_t
        self.fig, self.ax = plt.subplots(dpi=120, facecolor='w', edgecolor='k')  # 120 dpi h 180
        self.cases = False
        self.passengers_scatter = None
        self.source_cases_scatter = None
        self.info_text = None
        self.colorbar = None
        self.frame_number = None
        self.p_data = self.data_from_states()
        self.c = self.p_data['probabilities']

    def animation(self):
        self.set_fig_size()
        self.show_passengers()
        self.show_source_cases()


        if self.standing_bounds:
            self.show_standing_boundaries()
        if self.collision_lines:
            self.show_walls()
        if self.standing_spots_visible:
            self.show_standing_spots()

        self.show_objects()
        self.show_seats()
        self.show_doors()
        self.show_base()
        self.annotations()
        self.show_frame_number()
        self.show_info_text()
        self.show_colorbar()
        removeaxis(self.ax)
        ani = Player(self.fig, self.update, maxi=len(self.c) - 1, interval=self.delta_t*1000, save_count=(len(self.c) - 1))


        blank = self.fig.add_axes([0.82, 0.08, 0.2, 0.83])
        removeaxis(blank)
        blank.set_visible(False)
        legend = self.fig.add_axes([0.81, 0.3, 0.1, 0.5])
        removeaxis(legend)
        legend.set_visible(False)
        legend.scatter([1, 1, 1, 1, 1], [0, 1, 2, 3, 4], c=['white', 'blue', 'yellow', 'green', 'white'], s=200,
                       marker='o',
                       zorder=3, ec=['white', 'black', 'black', 'black', 'white'])
        legend.text(1.03, 1, 'Uninfected', fontsize=8, va='center', color='black')
        legend.text(1.03, 2, 'Infected', fontsize=8, va='center', color='black')
        legend.text(1.03, 3, 'Source Cases', fontsize=8, va='center', color='black')

        def change_data(event=None):
            if self.cases:
                self.c = self.p_data['probabilities']
                self.cases = False
                ani.onebackward()
                ani.oneforward()
                blank.set_visible(False)
                legend.set_visible(False)
                toggle.label.set_text('Probability of Infection')

            else:
                self.cases = True
                self.c = self.p_data['infected']
                ani.onebackward()
                ani.oneforward()
                blank.set_visible(True)
                legend.set_visible(True)
                toggle.label.set_text('Example of Possible Trasmission')

        title_button = self.fig.add_axes([0.3, 0.042, 0.4, 0.04], zorder=6)
        title_button.set_frame_on(False)
        toggle = matplotlib.widgets.Button(title_button, label='Probability of Infection', color='white')
        toggle.on_clicked(change_data)
        plt.show()

    def update(self, i):
        # Set x and y data...
        self.passengers_scatter.set_offsets(np.column_stack((self.p_data['x'][i], self.p_data['y'][i])))
        self.source_cases_scatter.set_offsets(np.column_stack((self.p_data['source_x'][i], self.p_data['source_y'][i])))
        # Set colors..
        self.passengers_scatter.set_array(np.asarray(self.c[i]))
        # Set probabilities and std
        t = self.stats(self.p_data['probabilities'][i], i)
        self.info_text.set_text('n = {:.0f}\nμ = {:.3f}\nσ = {:.3f}\np̄ = {:.3f}'.format(t[0], t[1], t[2], t[3]))
        self.frame_number.set_text('{:.2f} s'.format(i*self.delta_t))
        return self.passengers_scatter

    def stats(self, prbs, i):
        n = sum(self.p_data['infected'][i])
        std = np.sqrt(sum([p * (1 - p) for p in prbs]))
        mean_p = sum(prbs) / len(prbs)
        mean = mean_p * len(prbs)
        return n, mean, std, mean_p

    def data_from_states(self):
        x = []
        y = []
        source_x = []
        source_y = []
        probabilities = []
        infected = []

        for state in self.states:
            source_cases_id = state[:, 3] == 2

            x.append(state[:, 0][~source_cases_id])
            y.append(state[:, 1][~source_cases_id])
            probabilities.append(state[:, 2][~source_cases_id])
            infected.append(state[:, 3][~source_cases_id])

            source_x.append(state[:, 0][source_cases_id])
            source_y.append(state[:, 1][source_cases_id])

        p_data = {'x': x, 'y': y, 'source_x': source_x, 'source_y': source_y,
                  'probabilities': probabilities, 'infected': infected}

        return p_data

    def set_fig_size(self):
        size = 3
        min_passenger_y = min(self.p_data['y'][0])
        size_y = 1.2 * max((self.dimensions[1] - min_passenger_y), self.dimensions[1])
        self.fig.set_size_inches(self.dimensions[0] * size / self.dimensions[1], size_y)

    def show_walls(self):
        for w in self.walls:
            walls = plt.plot(w[:, 0], w[:, 1], zorder=7, linewidth=3, color='brown')

    def show_info_text(self):
        self.info_text = self.fig.text(0.032, 0.4, '', fontsize=10, va='bottom', color='white',
                                       bbox=dict(boxstyle='round', ec='k', fc='k', alpha=1))

    def show_frame_number(self):
        font = {'weight': 'normal', 'size': 12}
        self.frame_number = self.fig.text(0.85, 0.935, '', fontsize=12, va='center', color='black', font=font)

    def show_passengers(self):
        self.passengers_scatter = self.ax.scatter(self.p_data['x'][0], self.p_data['y'][0], c=self.c[0], s=200,
                                                  marker='o', cmap='plasma', vmin=0, vmax=max(self.c[-1])+0.0001,
                                                  zorder=3, ec='k')

    def show_standing_spots(self):
        spots = self.ax.scatter(self.standing_spots[:, 0], self.standing_spots[:, 1], c='red', s=100, zorder=4)

    def show_source_cases(self):
        self.source_cases_scatter = self.ax.scatter(self.p_data['source_x'][0], self.p_data['source_y'][0], c='green',
                                                    s=200, marker='o', zorder=4, ec='k')

    def show_colorbar(self):
        self.colorbar = self.fig.colorbar(self.passengers_scatter, fraction=0.046, pad=0.04)

    def show_standing_boundaries(self):
        sb = np.vstack(self.standing_boundaries)
        plt.plot(sb[:, 0], sb[:, 1], zorder=7)

    def show_seats(self):
        for seat in self.seats:
            xl = seat.dimensions[0]/2
            yl = seat.dimensions[1]/2
            w = 0.05
            h = 2*yl
            xo = seat.x-xl*np.cos(seat.rotation*np.pi/180) +yl*np.sin(seat.rotation*np.pi/180)
            yo = seat.y-yl*np.cos(seat.rotation*np.pi/180) -xl*np.sin(seat.rotation*np.pi/180)

            o = Rectangle((xo, yo), w, h, angle=seat.rotation,
                          ec='k', fc='gray', zorder=5, linewidth=0.7)

            s = Rectangle((xo, yo), xl*2, yl*2, angle=seat.rotation,
                          ec='k', fc='gray', zorder=2, linewidth=0.7)

            self.ax.add_patch(o)
            self.ax.add_patch(s)

    def show_base(self):
        rnd = 0.3
        p_bbox = FancyBboxPatch((0.3, 0.3), self.dimensions[0]-2*rnd, self.dimensions[1]-2*rnd,
                                boxstyle='round,pad=0.3', ec='k', fc='lightgray',  zorder=1, linewidth=3)
        self.ax.add_patch(p_bbox)

    def show_objects(self):
        if self.obstacle_objects:
            for obs in self.obstacle_objects:
                obstacle = Polygon(obs['xy'], zorder=5, **obs['kwargs'])
                self.ax.add_patch(obstacle)

    def show_doors(self):
        if self.doors:
            for door in self.doors:
                xdoor= door[0]
                doorwidth = door[1]
                doorshape = FancyBboxPatch((xdoor - doorwidth/2, 0), doorwidth, 0.02, boxstyle='round,pad=0.03',
                                           ec='k', fc='k', zorder=5, linewidth=2)
                self.ax.add_patch(doorshape)

    def annotations(self):
        annot = self.ax.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points', zorder=5, color='white',
                                 bbox=dict(boxstyle='round', fc='black', ec='none',), arrowprops=dict(arrowstyle='-'))
        annot.set_visible(False)

        def update_annot(ind):
            pos = self.passengers_scatter.get_offsets()[ind['ind'][0]]
            prob = self.passengers_scatter.get_array()[ind['ind'][0]]
            annot.xy = pos
            text = '{:.3f}'.format(prob)
            annot.set_text(text)
            annot.get_bbox_patch().set_facecolor('black')
            annot.get_bbox_patch().set_alpha(0.6)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == self.ax:
                cont, ind = self.passengers_scatter.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        self.fig.canvas.draw_idle()

        self.fig.canvas.mpl_connect('motion_notify_event', hover)