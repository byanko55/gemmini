from gemmini.misc import *
from gemmini.calc.coords import dist, gradient
from gemmini.d2._gem2D import Geometry2D
from gemmini.d2.line2D import Line2D
from gemmini.d2.polar2D import Curve2D
from gemmini.d2.point2D import Pointcloud2D, Point2D

import itertools
import matplotlib.pyplot as plt


THEMES = {
    'light': {
        'facecolor':'#F9F9F9', 
        'tickcolor':'#000000',
        'dotcolor':'#26272D',
        'edgecolor':'#5794DE',
        'figcolor':itertools.cycle([
            '#D52753', '#23974A', '#DF631C', '#275FE4', '#823FF1', 
            '#27618D', '#FF6480', '#3CBC66', '#C5A332', '#0099E1',
            '#CE33C0', '#6D93BB'
        ]),
        'textcolor':'#26272D'
    }
}

class Canvas:
    def __init__(
        self,
        theme:str = 'light',
        window_size:Tuple[float, float]=(5,5),
        fontsize:int=10,
        scale:float = 1.0,
        draw_grid:bool = True,
        major_ticks:bool = True,
        minor_ticks:bool = True,
        **kwargs
    ) -> None:
        """
        Class for rendering geometric figures on matplotlib canvas.

        Args:
            theme (str) : name of a color theme to be applied on the canvas.
            window_size (float, float): canvas dimension (width, height) in inches.
            fontsize (int): tick label font size in points.
            scale (float): scaling factor for the view box.
            draw_grid (bool): if `False`, the canvas does not show ticks and grid.
            major_ticks (bool): whether to draw the respective major ticks.
            minor_ticks (bool): whether to draw the respective minor ticks.
        """
        self.window_size = window_size
        self.fontsize = fontsize
        self.scale = scale
        self.draw_grid = draw_grid
        self.draw_major = major_ticks
        self.draw_minor = minor_ticks
        self.gems = list()

        self.theme = THEMES.get(theme)

        if type(self.theme) == type(None):
            raise(" \
                [ERROR] Canvas: Can't find a canvas theme named `%s`. \
                "%(theme)
            )

    def plot(self) -> None:
        """
        Plot all geometric object that the canvas holds.
        """
        plt.rc('font', family='DejaVu Sans', size=self.fontsize)
        fig=plt.figure(figsize=self.window_size, facecolor=self.theme['facecolor'])
        gem_configs = sorted(self.gems, key=lambda f: isinstance(f['fig'], Line2D))

        _, canvas_size = self._draw_ticks(fig, gem_configs)

        for g_config in gem_configs:
            gem = g_config['fig']

            if isinstance(gem, Line2D):
                plt.axline(
                    xy1=gem.p1,
                    xy2=gem.p2,
                    slope=gem.slope,
                    linewidth = g_config['opt_s'],
                    color = g_config['opt_c'],
                    linestyle = g_config['opt_m'],
                    zorder = g_config['zorder']
                )
            else :
                xs, ys = gem.coordsXY()

                plt.scatter(
                    xs, 
                    ys, 
                    s = g_config['opt_s'],
                    c = g_config['opt_c'],
                    marker = g_config['opt_m'],
                    zorder = g_config['zorder']
                )

                # Display centroid
                if g_config['opt_dc']:
                    xc, yc = gem.center()
                    plt.scatter(
                        [xc], [yc], c = self.theme['dotcolor'], zorder = g_config['zorder'] + 1
                    )
                    
                    plt.text(
                        xc, 
                        yc + canvas_size/25,
                        "(%.2f, %.2f)"%(xc, yc),
                        bbox=dict(facecolor=self.theme['facecolor'], alpha=0.7, edgecolor='none'),
                        ha='center',
                        va='center',
                        weight='bold'
                    )
                    
                # Display radius
                if g_config['opt_dr']:
                    xc, yc = gem.center()
                    max_d = 0
                    p = 0
                    
                    _c = gem.coords()
                    
                    for i, (_x, _y) in enumerate(_c):
                        _d = dist((xc, yc), (_x, _y))
                        
                        if dist((xc, yc), (_x, _y)) > max_d :
                            max_d = _d
                            p = i
                            
                    _g = gradient((xc, yc), _c[p], radian=True) 
                            
                    plt.plot([xc, _c[p][0]], [yc, _c[p][1]], c=self.theme['edgecolor'])
                    plt.text(
                        (xc + _c[p][0])/2 + cos(_g + 3*pi/2) * canvas_size/10,
                        (yc + _c[p][1])/2 + sin(_g + 3*pi/2) * canvas_size/30, 
                        "%s = %.2f"%('r' if isinstance(gem, Curve2D) else 'd', max_d),
                        bbox=dict(facecolor=self.theme['facecolor'], alpha=0.7, edgecolor='none'),
                        ha='center',
                        va='center',
                        weight='bold'
                    )
                    
                # Display edges
                if g_config['opt_de']:
                    edges = gem.exterior()
                    
                    for i in range(len(edges)):
                        plt.plot(
                            [edges[i][0], edges[(i+1)%len(edges)][0]], 
                            [edges[i][1], edges[(i+1)%len(edges)][1]], 
                            c=self.theme['edgecolor'],
                            zorder=-1
                        )
                
                # Display interior
                if g_config['opt_di']:
                    interior = gem.interior()
                    xs, ys = interior[:, 0], interior[:, 1]

                    plt.scatter(
                        xs, 
                        ys, 
                        s = g_config['opt_s'],
                        c = g_config['opt_c'],
                        marker = g_config['opt_m'],
                        zorder= g_config['zorder']
                    )
                    
                # Display dimension
                if g_config['opt_dd']:
                    x_min, y_min, x_max, y_max = gem.bounding_box()
                    
                    plt.plot(
                        [x_min - canvas_size/128, x_max + canvas_size/128], 
                        [y_max + canvas_size/32, y_max + canvas_size/32], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.plot(
                        [x_min - canvas_size/128, x_min - canvas_size/128], 
                        [y_max + canvas_size/64, y_max + 3*canvas_size/64], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.plot(
                        [x_max + canvas_size/128, x_max + canvas_size/128], 
                        [y_max + canvas_size/64, y_max + 3*canvas_size/64], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.text(
                        (x_min + x_max)/2,
                        y_max + 3*canvas_size/64,
                        "%.2f"%(x_max-x_min),
                        bbox=dict(facecolor=self.theme['facecolor'], alpha=0.6, edgecolor='none'),
                        ha='center',
                        weight='bold'
                    )
                    
                    plt.plot(
                        [x_max + canvas_size/32, x_max + canvas_size/32], 
                        [y_min - canvas_size/128, y_max + canvas_size/128], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.plot(
                        [x_max + canvas_size/64, x_max + 3*canvas_size/64], 
                        [y_min - canvas_size/128, y_min - canvas_size/128], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.plot(
                        [x_max + canvas_size/64, x_max + 3*canvas_size/64], 
                        [y_max + canvas_size/128, y_max + canvas_size/128], 
                        c=self.theme['edgecolor']
                    )
                    
                    plt.text(
                        x_max + 3*canvas_size/64, 
                        (y_min + y_max)/2,
                        "%.2f"%(y_max-y_min),
                        bbox=dict(facecolor=self.theme['facecolor'], alpha=0.6, edgecolor='none'),
                        va='center',
                        weight='bold'
                    )

        plt.show()

    def _draw_ticks(self, fig:object, gem_configs:dict) -> Tuple[float, float]:
        ax=fig.add_axes([0,0,1,1])
        cx, cy, box_size = map(int, [0]*3)

        for g_config in gem_configs:
            g = g_config['fig']
            
            if isinstance(g, Line2D):
                if box_size == 0:
                    cx, cy = g.p1
                    box_size = 1
                    continue
                
                ox, oy = g.orthog_point((cx, cy))
                ncx, ncy, nbx, nby = cx, cy, box_size, box_size 

                if ox > cx + box_size:
                    ncx = (cx - box_size + ox)/2
                    nbx = (ox - cx + box_size)/2

                if ox < cx - box_size:
                    ncx = (cx + box_size + ox)/2
                    nbx = (cx + box_size - ox)/2

                if oy > cy + box_size:
                    ncy = (cy - box_size + oy)/2
                    nby = (oy - cy + box_size)/2

                if oy < cy - box_size:
                    ncy = (cy + box_size + oy)/2
                    nby = (cy + box_size - oy)/2

                cx, cy, box_size = ncx, ncy, max(nbx, nby)
            else :
                if box_size == 0:
                    cx, cy = g.center()
                
                x_min, y_min, x_max, y_max = g.bounding_box()

                ncx = (min(x_min, cx-box_size) + max(x_max, cx + box_size))/2
                ncy = (min(y_min, cy-box_size) + max(y_max, cy + box_size))/2
                nbs = max(
                    max(x_max, cx + box_size) - min(x_min, cx-box_size),
                    max(y_max, cy + box_size) - min(y_min, cy-box_size)
                )/2

                cx, cy, box_size = ncx, ncy, nbs

        box_size = max(0.01, 2*box_size*self.scale)
        _u = floor(log10(box_size))
        _u = 10 ** _u
        _v = int(box_size//_u) + 1
        canvas_size = _v * _u 
        lb, rb = cx - canvas_size/2, cx + canvas_size/2
        bb, tb = cy - canvas_size/2, cy + canvas_size/2

        ax.set_xlim([lb, rb])
        ax.set_ylim([bb, tb])

        _tu = _u*(_v//2)

        if self.draw_major:
            tick_lb, tick_rb = _tu*(lb//_tu + 1), _tu*(rb//_tu)
            tick_bb, tick_tb = _tu*(bb//_tu + 1), _tu*(tb//_tu)
            ax.set_xticks(np.linspace(tick_lb, tick_rb, int((tick_rb-tick_lb)//_tu + 1)))
            ax.set_yticks(np.linspace(tick_bb, tick_tb, int((tick_tb-tick_bb)//_tu + 1)))

        if self.draw_minor:
            mtick_lb, mtick_rb = (_tu/2)*(lb//(_tu/2) + 1), (_tu/2)*(rb//(_tu/2))
            mtick_bb, mtick_tb = (_tu/2)*(bb//(_tu/2) + 1), (_tu/2)*(tb//(_tu/2))
            ax.set_xticks(np.linspace(mtick_lb, mtick_rb, int((mtick_rb-mtick_lb)//(_tu/2) + 1)), minor=True)
            ax.set_yticks(np.linspace(mtick_bb, mtick_tb, int((mtick_tb-mtick_bb)//(_tu/2) + 1)), minor=True)

        if self.draw_grid:
            ax.grid(which='both', color='#BDBDBD', linestyle='--', linewidth=1, zorder=-1)
        else :
            plt.tick_params(left = False, right = False, labelleft = False, 
                labelbottom = False, bottom = False)
            
        ax.tick_params(axis='x', colors=self.theme['tickcolor'])
        ax.tick_params(axis='y', colors=self.theme['tickcolor'])
        ax.patch.set_facecolor(self.theme['facecolor'])
            
        return ax, canvas_size

    def _add_point(
        self,
        point:Point2D,
        dot_color:str = None,
        dot_size:int = 25,
        dot_style:str = 'o',
        display_coord:bool = True,
        zorder:int = 2,
        **kwargs
    ):
        """
        Reserve a given Geometry2D object for drawing it on canvas.

        Args:
            gem (Geometry2D): geometry to be displayed on canvas.
            dot_color (str): color of the pixels.
            dot_size (int): size of a pixel.
            dot_style (str): marker style.
                {'.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'}
            display_coord (bool): if True, display text that represents (x, y) coordinates of the point.
            zorder (int): lower zorder values are drawn first.
        """
        fig_config = {
            'fig':point, 
            'opt_s':dot_size, 
            'opt_c':dot_color, 
            'opt_m':dot_style,
            'opt_de':False,
            'opt_di':False,
            'opt_dr':False,
            'opt_dd':False,
            'opt_dc':display_coord,
            'zorder':zorder
        }

        self.gems.append(fig_config)
        
    def _add_gem(
        self, 
        gem:Geometry2D, 
        dot_color:str = None,
        dot_size:int = 25,
        dot_style:str = 'o', 
        draw_edges:bool = False,
        draw_interior:bool = False,
        draw_radius:bool = False,
        draw_dimension:bool = False,
        draw_center:bool = False,
        zorder:int = 1,
        **kwargs
    ):
        """
        Reserve a given Geometry2D object for drawing it on canvas.

        Args:
            gem (Geometry2D): geometry to be displayed on canvas.
            dot_color (str): color of the pixels.
            dot_size (int): size of a pixel.
            dot_style (str): marker style.
                {'.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'}
            draw_edges (bool): whether draw path enclosing the given geometry.
            draw_interior (bool): whether fill pixels in the interior of the geometry.
            draw_radius (bool): whether display a radius vector and its length.
            draw_dimension (bool) : whether display a height/width of the geometry.
            draw_center (bool): if True, display text that represents (x, y) coordinates of the centroid.
            zorder (int): lower zorder values are drawn first.
        """
        if isinstance(gem, Pointcloud2D) and draw_edges:
            warnings.warn(" \
                [WARN] Canvas: `Pointcloud` object does not support drawing edges. \
            ")

            draw_edges = False

        fig_config = {
            'fig':gem, 
            'opt_s':dot_size, 
            'opt_c':dot_color, 
            'opt_m':dot_style,
            'opt_de':draw_edges,
            'opt_di':draw_interior,
            'opt_dr':draw_radius,
            'opt_dd':draw_dimension,
            'opt_dc':draw_center,
            'zorder':zorder
        }

        self.gems.append(fig_config)

    def _add_line(
        self, 
        line:Line2D, 
        line_color:str = None,
        line_width:int = 2,
        line_style:str = '-',
        zorder:int = 1,
        **kwargs
    ):
        """
        Reserve a given Line2D object for drawing it on canvas.

        Args:
            line (Line2D): line to be displayed on canvas.
            line_color (str): color of the line.
            line_width (int): thickness for the line.
            line_style (str): linestyle.
                {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            zorder (int): lower zorder values are drawn first.
        """
        fig_config = {
            'fig':line,
            'opt_s':line_width,
            'opt_c':line_color, 
            'opt_m':line_style,
            'zorder':zorder
        }

        self.gems.append(fig_config)

    def add(
        self, 
        gem:Any, 
        color:str = None,
        **kwargs
    ) -> None:
        """
        Reserve a given figure for drawing it on canvas

        Args:
            gem (Geometry2D | Line2D | Point2D | tuple): figure to be displayed on canvas.
            color (str): color of a pixel/line.
            tickness (int): scale of a point/width of a line.
            draw_style (str): marker/line style.
                for line object: {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
                for other geometry: {'.', 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'}
            draw_edges (bool): whether draw path enclosing the given geometry.
            draw_interior (bool): whether fill pixels in the interior of the geometry.
            draw_radius (bool): whether display a radius vector and its length.
            draw_dimension (bool) : whether display a height/width of the geometry.
            draw_center (bool): if True, display text that represents (x, y) coordinates of the centroid.
            zorder (int): lower zorder values are drawn first.
        """
        if not isinstance(gem, (list, tuple)) or isPoint(gem):
            gem = [gem]

        for g in gem:
            if isPoint(g) or isinstance(g, Point2D):
                c = color if color != None else self.theme['dotcolor']
            else :
                c = color if color != None else next(self.theme['figcolor'])
                
            size = kwargs.get('tickness')
            style = kwargs.get('draw_style')
            
            if type(size) != type(None):
                del kwargs['tickness']
                
            if type(style) != type(None):
                del kwargs['draw_style']
            
            if isPoint(g):
                self._add_point(
                    Point2D(g[0], g[1]),
                    c,
                    dot_size=size,
                    dot_style=style,
                    **kwargs
                )
            elif isinstance(g, Point2D):
                self._add_point(
                    g, 
                    c,
                    dot_size=size,
                    dot_style=style,
                    **kwargs
                )
            elif isinstance(g, Geometry2D):
                self._add_gem(
                    g, 
                    c,
                    dot_size=size,
                    dot_style=style,
                    **kwargs
                )
            elif isinstance(g, Line2D):
                self._add_line(
                    g, 
                    c, 
                    line_width=size,
                    line_style=style,
                    **kwargs
                )
            else :
                raise ValueError(" \
                    [ERROR] Canva: the input geometry should be either Geometry2D or Line2D object. \
                ")

    def remove(self, gem:Union[Geometry2D, Line2D]) -> None:
        """
        Remove a given geometric object from the drawing queue.

        Args:
            gem (Geometry2D | Line2D): figure to be removed.
        """
        for i in range(len(self.gems)):
            if hash(self.gems[i]['fig']) == hash(gem):
                del self.gems[i]
                return
            
        warnings.warn(" \
            [WARN] Canvas: No such geometry exists on the figure list. \
        ")
            
    def __len__(self) -> int:
        return len(self.gems)

    def __getitem__(self, item:int) -> Geometry2D:
        if len(self.gems) >= item:
            raise IndexError(" \
                [ERROR] Canvas: Index out of bound. \
            ")

        return self.gems[item]['fig']


def plot(gem:Any, **kwargs) -> None:
    """
    Draw a geometry instance on a canvas.

    Args:
        gem (Geometry2D | Line2D | Point2D | tuple): figure to be displayed on canvas.
    """
    canva = Canvas(**kwargs)
    canva.add(gem, **kwargs)
    canva.plot()

    del canva