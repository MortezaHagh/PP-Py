import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class Plotter:
    def __init__(self, model) -> None:
        self.model = model
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.axis("off")
        self.ax.axis('equal')
        self.ax.axis([model.map.x_min-1, model.map.x_max+1,
                      model.map.y_min-1, model.map.y_max+1])
        self.plot_model()

    def plot_model(self):
        # start
        self.ax.plot(self.model.robot.xs, self.model.robot.ys, marker='^', markersize=10,
                     markeredgecolor='g', markerfacecolor='g', label="Start")
        # target
        self.ax.plot(self.model.robot.xt, self.model.robot.yt, marker='v', markersize=10,
                     markeredgecolor='r', markerfacecolor='r', label="Destination")

        # # Obstacles
        # theta = np.linspace(0, 2*np.pi, 50)
        # for i in range(0, model.obsts.count):
        #     ax.fill([model.obsts.x[i] + model.obsts.r*np.cos(t) for t in theta],
        #             [model.obsts.y[i] + model.obsts.r*np.sin(t) for t in theta], 'b', edgecolor='b')
        self.ax.plot(self.model.obsts.x, self.model.obsts.y, 'o',  markersize=5,
                     markeredgecolor='k', markerfacecolor='k')

        # Walls
        lx = self.model.map.x_max-self.model.map.x_min + 1
        ly = self.model.map.y_max-self.model.map.y_min + 1
        rect = patches.Rectangle((self.model.map.x_min-0.5, self.model.map.y_min-0.5),
                                 lx, ly, linewidth=2, edgecolor='k', facecolor='none')
        self.ax.add_patch(rect)

    def plot_solution(self, sol):
        self.ax.plot(sol.x, sol.y, 'b', linewidth=1)
        self.ax.plot(sol.x, sol.y, 'o', markersize=4,
                     markeredgecolor='b', markerfacecolor='b')

    def init_anim(self, sol):
        self.sol = sol
        self.path_len = len(sol.x)

        line = [0, 0]
        line[0], = self.ax.plot(sol.x[0], sol.y[0], 'o',
                                markerfacecolor='green', markeredgecolor='green', markersize=5)
        line[1], = self.ax.plot(sol.x[0:2], sol.y
                                [0:2], color='green', linewidth=2)
        self.line = line

    def ani_init(self):  # only required for blitting to give a clean slate.
        self.line[0].set_data([], [])
        self.line[1].set_data([], [])
        return self.line

    def ani_update(self, i):
        if i < self.path_len:
            x = self.sol.x[i]
            y = self.sol.y[i]
            self.line[0].set_data(x, y)
            xx = self.sol.x[i-1:i+1]
            yy = self.sol.y[i-1:i+1]
            self.line[1].set_data(xx, yy)
        return self.line

    def animate(self):
        self.anim = animation.FuncAnimation(
            self.fig, self.ani_update, init_func=self.ani_init, frames=self.path_len, repeat=False, interval=500, blit=True)
