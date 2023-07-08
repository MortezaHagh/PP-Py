import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_model(model):
    fig, ax = plt.subplots(1, 1)
    ax.axis("off")
    ax.axis('equal')
    ax.axis([model.map.x_min-1, model.map.x_max+1,
            model.map.y_min-1, model.map.y_max+1])

    # start
    ax.plot(model.robot.xs, model.robot.ys, marker='^', markersize=10,
            markeredgecolor='g', markerfacecolor='g', label="Start")
    # target
    ax.plot(model.robot.xt, model.robot.yt, marker='v', markersize=10,
            markeredgecolor='r', markerfacecolor='r', label="Destination")

    # # Obstacles
    # theta = np.linspace(0, 2*np.pi, 50)
    # for i in range(0, model.obsts.count):
    #     ax.fill([model.obsts.x[i] + model.obsts.r*np.cos(t) for t in theta],
    #             [model.obsts.y[i] + model.obsts.r*np.sin(t) for t in theta], 'b', edgecolor='b')
    ax.plot(model.obsts.x, model.obsts.y, 'o',  markersize=5,
            markeredgecolor='k', markerfacecolor='k')

    # Walls
    lx = model.map.x_max-model.map.x_min + 1
    ly = model.map.y_max-model.map.y_min + 1
    rect = patches.Rectangle((model.map.x_min-0.5, model.map.y_min-0.5),
                             lx, ly, linewidth=2, edgecolor='k', facecolor='none')
    ax.add_patch(rect)

    return fig, ax


if __name__ == '__main__':
    from create_model_base import CreateBaseModel
    model = CreateBaseModel()
    plot_model(model)
    plt.show()
