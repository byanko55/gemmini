from gemmini.misc import *

def plot(gem:List[Any]) -> None:
    """
    Draw a geometry instance on a canvas
    """
    plt.rc('font', family='DejaVu Sans', size=10)
    fig=plt.figure(figsize=(5, 5))
    ax=fig.add_axes([0,0,1,1])

    xs, ys = gem.coordsXY()
    x_min, y_min, x_max, y_max = gem.bounding_box()
    x_mean, y_mean = gem.center()

    canvas_size = 10 ** (int(log10(max(1, max(x_max-x_min, y_max-y_min)))) + 1)
    lb, rb = int(x_mean) - canvas_size//2, int(x_mean) + canvas_size//2
    bb, tb = int(y_mean) - canvas_size//2, int(y_mean) + canvas_size//2

    ax.set_xlim([lb, rb])
    ax.set_ylim([bb, tb])
    ax.set_xticks(list(range(lb, rb + 1, canvas_size//5)))
    ax.set_yticks(list(range(bb, tb + 1, canvas_size//5)))
    ax.set_xticks(range(lb, rb + 1, canvas_size//10), minor=True)
    ax.set_yticks(range(bb, tb + 1, canvas_size//10), minor=True)
    ax.grid(which='both', color='#BDBDBD', linestyle='--', linewidth=1)

    plt.scatter(xs, ys, zorder=10)
    plt.show()