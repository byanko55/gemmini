from gemmini.misc import *
from gemmini.d2 import Line2D
from gemmini.d2._gem2D import Geometry2D

def plot(gem:List[Any]) -> None:
    """
    Draw a geometry instance on a canvas
    """
    plt.rc('font', family='DejaVu Sans', size=10)
    fig=plt.figure(figsize=(5, 5))
    ax=fig.add_axes([0,0,1,1])

    if isinstance(gem, Line2D):
        plt.axline(xy1=gem.p1, xy2=gem.p2, slope=gem.slope)

    if isinstance(gem, Geometry2D):
        xs, ys = gem.coordsXY()
        x_min, y_min, x_max, y_max = gem.bounding_box()
        x_mean, y_mean = gem.center()
        
        _u = int(log10(max(1, max(x_max-x_min, y_max-y_min))))
        _u = 10 ** _u
        _v = max(x_max-x_min, y_max-y_min)//_u + 2
        canvas_size = _v * _u
        lb, rb = x_mean - canvas_size/2, x_mean + canvas_size/2
        bb, tb = y_mean - canvas_size/2, y_mean + canvas_size/2

        _tu = _u*((_v-1)//2)

        tick_lb, tick_rb = _tu*(lb//_tu + 1), _tu*(rb//_tu)
        tick_bb, tick_tb = _tu*(bb//_tu + 1), _tu*(tb//_tu)
        
        mtick_lb, mtick_rb = (_tu/2)*(lb//(_tu/2) + 1), (_tu/2)*(rb//(_tu/2))
        mtick_bb, mtick_tb = (_tu/2)*(bb//(_tu/2) + 1), (_tu/2)*(tb//(_tu/2))

        print(lb, rb, bb, tb, _u, _v, _u*(lb//_u), _u*(rb//_u), _u*(bb//_u), _u*(tb//_u))
        print((tick_rb-tick_lb)//_u + 1, (tick_tb-tick_bb)//_u + 1)

        ax.set_xlim([lb, rb])
        ax.set_ylim([bb, tb])
        ax.set_xticks(np.linspace(tick_lb, tick_rb, int((tick_rb-tick_lb)//_tu + 1)))
        ax.set_yticks(np.linspace(tick_bb, tick_tb, int((tick_tb-tick_bb)//_tu + 1)))
        ax.set_xticks(np.linspace(mtick_lb, mtick_rb, int((mtick_rb-mtick_lb)//(_tu/2) + 1)), minor=True)
        ax.set_yticks(np.linspace(mtick_bb, mtick_tb, int((mtick_tb-mtick_bb)//(_tu/2) + 1)), minor=True)
        ax.grid(which='both', color='#BDBDBD', linestyle='--', linewidth=1)

        plt.scatter(xs, ys, zorder=10)

    plt.show()