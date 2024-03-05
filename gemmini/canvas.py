from gemmini.misc import *
from gemmini.calc.coords import dist, gradient
from gemmini.d2._gem2D import Geometry2D
from gemmini.d2.line2D import Line2D
from gemmini.d2.polar2D import Curve2D
from gemmini.d2.point2D import PointSet2D, Point2D

import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


DIM_MAX = 1e9
ORDER_MAX = 1e6
BASE_ORDER = 2


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
    },
    'ura': {
        'facecolor':'#FEFFEE', 
        'tickcolor':'#000000',
        'dotcolor':'#000000',
        'edgecolor':'#26272D',
        'figcolor':itertools.cycle([
            '#C21B6F', '#6FC21B', '#C26F1B', '#1B6FC2', '#6F1BC2', 
            '#1BC26F'
        ]),
        'textcolor':'#26272D'
    },
    'tomorrow': {
        'facecolor':'#FFFFFF', 
        'tickcolor':'#000000',
        'dotcolor':'#000000',
        'edgecolor':'#26272D',
        'figcolor':itertools.cycle([
            '#C82828', '#718C00', '#EAB700', '#4171AE', '#8959A8', 
            '#3E999F'
        ]),
        'textcolor':'#26272D'
    },
    'solarized': {
        'facecolor':'#FDF6E3', 
        'tickcolor':'#002B36',
        'dotcolor':'#002B36',
        'edgecolor':'#586E75',
        'figcolor':itertools.cycle([
            '#DC322F', '#859900', '#B58900', '#268BD2', '#D33682', 
            '#2AA198', '#CB4B16', '#6C71C4'
        ]),
        'textcolor':'#002B36'
    },
    'rose': {
        'facecolor':'#FAF4ED', 
        'tickcolor':'#002B36',
        'dotcolor':'#002B36',
        'edgecolor':'#9893A5',
        'figcolor':itertools.cycle([
            '#B4637A', '#56949F', '#EA9D34', '#286983', '#907AA9', 
            '#D7827E', '#575279'
        ]),
        'textcolor':'#002B36'
    },
    'horizon': {
        'facecolor':'#FDF0ED', 
        'tickcolor':'#16161C',
        'dotcolor':'#1A1C23',
        'edgecolor':'#666666',
        'figcolor':itertools.cycle([
            '#DA103F', '#1EB980', '#F6661E', '#26BBD9', '#EE64AE', 
            '#1D8991'
        ]),
        'textcolor':'#1A1C23'
    },
    'gruvbox': {
        'facecolor':'#FBF1C7', 
        'tickcolor':'#7C6F64',
        'dotcolor':'#3C3836',
        'edgecolor':'#7C6F64',
        'figcolor':itertools.cycle([
            '#CC241D', '#98971A', '#D79921', '#458588', '#B16286', 
            '#689D6A'
        ]),
        'textcolor':'#3C3836'
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

        ax, canvas_size = self._draw_ticks(fig, gem_configs)

        for g_config in gem_configs:
            gem = g_config['fig']

            if isinstance(gem, Line2D):
                self._plot_line(gem, g_config)
                continue

            # Other geometry
                    
            # Display edges
            if g_config['opt_de'] or g_config['opt_da']:
                self._plot_edges(gem, g_config)

            # Draw pixels
            self._plot_gem(gem, g_config)

            # Display interior
            if g_config['opt_di'] and gem._planar:
                self._plot_interior(gem, g_config, ax)

            # Display dimension
            if g_config['opt_dd']:
                self._plot_dimension(gem, canvas_size)

            # Display area
            if g_config['opt_da']:
                self._plot_area(gem, canvas_size)
                self._plot_interior(gem, g_config, ax, opaque=True)

            # Display centroid
            if g_config['opt_dc']:
                self._plot_center(gem, canvas_size)
                    
            # Display radius
            if g_config['opt_dr']:
                self._plot_radius(gem, canvas_size)

        plt.show()

    def _plot_line(self, gem:Line2D, g_config:dict) -> None:
        plt.axline(
            xy1=gem.p1,
            xy2=gem.p2,
            slope=gem.slope,
            linewidth = g_config['opt_s'],
            color = g_config['opt_c'],
            linestyle = g_config['opt_m'],
            zorder = g_config['zorder']
        )

    def _plot_gem(self, gem:Geometry2D, g_config:dict) -> None:
        xs, ys = gem.coordsXY()

        plt.scatter(
            xs, 
            ys, 
            s = g_config['opt_s'],
            c = g_config['opt_c'],
            marker = g_config['opt_m'],
            zorder = g_config['zorder']
        )

    def _plot_center(self, gem:Geometry2D, canvas_size:float) -> None:
        xc, yc = gem.center()

        plt.scatter(
            [xc], [yc], c = self.theme['dotcolor'], zorder = ORDER_MAX
        )
        
        plt.text(
            xc, 
            yc + canvas_size/25,
            "(%.2f, %.2f)"%(xc, yc),
            bbox=dict(facecolor=self.theme['facecolor'], alpha=0.7, edgecolor='none'),
            ha='center',
            va='center',
            weight='bold',
            zorder = ORDER_MAX
        )

    def _plot_radius(self, gem:Geometry2D, canvas_size:float) -> None:
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
            weight='bold',
            zorder = ORDER_MAX
        )

    def _plot_edges(self, gem:Geometry2D, g_config:dict) -> None:
        for edges in gem._outers:
            for i in range(len(edges)-1):
                plt.plot(
                    [gem[edges[i]][0], gem[edges[i+1]][0]], 
                    [gem[edges[i]][1], gem[edges[i+1]][1]], 
                    c=self.theme['edgecolor'],
                    zorder = g_config['zorder']
                )

        for edges in gem._inners:
            for i in range(len(edges)-1):
                plt.plot(
                    [gem[edges[i]][0], gem[edges[i+1]][0]], 
                    [gem[edges[i]][1], gem[edges[i+1]][1]], 
                    c=self.theme['edgecolor'],
                    zorder = g_config['zorder']
                )

    def _plot_interior(self, gem:Geometry2D, g_config:dict, ax:object, opaque:bool=False) -> None:
        for edges in gem._outers:
            color = self.theme['edgecolor'] if opaque else g_config['opt_c']
            alpha = 0.5 if opaque else 1

            g = Polygon(
                gem[edges],
                facecolor = color,
                alpha = alpha,
                zorder = g_config['zorder']
            )

            ax.add_patch(g)

        for edges in gem._inners:
            g = Polygon(
                gem[edges],
                facecolor = self.theme['facecolor'],
                zorder = g_config['zorder']
            )

            ax.add_patch(g)

    def _plot_dimension(self, gem:Geometry2D, canvas_size:float) -> None:
        x_min, y_min, x_max, y_max = gem.bounding_box()
                
        plt.plot(
            [x_min - canvas_size/128, x_max + canvas_size/128], 
            [y_max + canvas_size/32, y_max + canvas_size/32], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.plot(
            [x_min - canvas_size/128, x_min - canvas_size/128], 
            [y_max + canvas_size/64, y_max + 3*canvas_size/64], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.plot(
            [x_max + canvas_size/128, x_max + canvas_size/128], 
            [y_max + canvas_size/64, y_max + 3*canvas_size/64], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.text(
            (x_min + x_max)/2,
            y_max + 3*canvas_size/64,
            "%.2f"%(x_max-x_min),
            bbox=dict(facecolor=self.theme['facecolor'], alpha=0.6, edgecolor='none'),
            ha='center',
            weight='bold',
            zorder = ORDER_MAX
        )
        
        plt.plot(
            [x_max + canvas_size/32, x_max + canvas_size/32], 
            [y_min - canvas_size/128, y_max + canvas_size/128], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.plot(
            [x_max + canvas_size/64, x_max + 3*canvas_size/64], 
            [y_min - canvas_size/128, y_min - canvas_size/128], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.plot(
            [x_max + canvas_size/64, x_max + 3*canvas_size/64], 
            [y_max + canvas_size/128, y_max + canvas_size/128], 
            c=self.theme['edgecolor'],
            zorder = ORDER_MAX
        )
        
        plt.text(
            x_max + 3*canvas_size/64, 
            (y_min + y_max)/2,
            "%.2f"%(y_max-y_min),
            bbox=dict(facecolor=self.theme['facecolor'], alpha=0.6, edgecolor='none'),
            va='center',
            weight='bold',
            zorder = ORDER_MAX
        )

    def _plot_area(self, gem:Geometry2D, canvas_size:float) -> None:
        xc, yc = gem.center()
        a = gem.area()

        plt.text(
            xc, 
            yc - canvas_size/25,
            "(Area = %.2f)"%(a),
            bbox=dict(facecolor=self.theme['facecolor'], alpha=0.7, edgecolor='none'),
            ha='center',
            weight='bold',
            zorder = ORDER_MAX
        )

    def _draw_ticks(self, fig:object, gem_configs:dict) -> Tuple[float, float]:
        ax=fig.add_axes([0,0,1,1])

        mx, Mx, my, My = DIM_MAX, -DIM_MAX, DIM_MAX, -DIM_MAX
        cx, cy, box_size = map(int, [0]*3)

        for g_config in gem_configs:
            g = g_config['fig']
            
            if isinstance(g, Line2D):
                cx, cy = (mx+Mx)/2, (my+My)/2
                _, _ = g.orthog_point((cx, cy))

                mx, Mx, my, My = min(mx, cx), max(Mx, cx), min(my, cy), max(My, cy)
            else :
                x_min, y_min, x_max, y_max = g.bounding_box()
                mx, Mx, my, My = min(mx, x_min), max(Mx, x_max), min(my, y_min), max(My, y_max)

        box_size = max(0.01, max(Mx-mx, My-my)*self.scale)
        cx, cy = (Mx+mx)/2, (My+my)/2

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

        ax.set_axisbelow(True)

        if self.draw_grid:
            ax.grid(which='both', color='#BDBDBD', linestyle='--', linewidth=1)
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
        dot_size:int = 8,
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
            'opt_da':False,
            'zorder':zorder + BASE_ORDER
        }

        self.gems.append(fig_config)
        
    def _add_gem(
        self, 
        gem:Geometry2D, 
        dot_color:str = None,
        dot_size:int = 25,
        dot_style:str = 'o', 
        fill:bool = False,
        show_edges:bool = False,
        show_radius:bool = False,
        show_size:bool = False,
        show_center:bool = False,
        show_area:bool = False,
        zorder:int = 0,
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
            fill (bool): whether fill pixels in the interior of the geometry.
            show_edges (bool): whether draw path enclosing the given geometry.
            show_radius (bool): whether display a radius vector and its length.
            show_size (bool) : whether display a height/width of the geometry.
            show_center (bool): if True, display text that represents (x, y) coordinates of the centroid.
            show_area (bool): if True, display the area of the geometry.
            zorder (int): lower zorder values are drawn first.
        """
        if isinstance(gem, PointSet2D) and show_edges:
            warnings.warn(" \
                [WARN] Canvas: `Pointcloud` object does not support drawing edges. \
            ")

            show_edges = False

        if not gem._planar and show_area:
            warnings.warn(" \
                [WARN] Canvas: `%s` class does not support displaying its area. \
                "%(gem.gem_type)
            )

            show_area = False

        fig_config = {
            'fig':gem, 
            'opt_s':dot_size, 
            'opt_c':dot_color, 
            'opt_m':dot_style,
            'opt_de':show_edges,
            'opt_di':fill,
            'opt_dr':show_radius,
            'opt_dd':show_size,
            'opt_dc':show_center,
            'opt_da':show_area,
            'zorder':zorder + BASE_ORDER
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
            'zorder':zorder + BASE_ORDER
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
            fill (bool): whether fill pixels in the interior of the geometry.
            show_edges (bool): whether draw path enclosing the given geometry.
            show_radius (bool): whether display a radius vector and its length.
            show_size (bool) : whether display a height/width of the geometry.
            show_center (bool): if True, display text that represents (x, y) coordinates of the centroid.
            show_area (bool): if True, display the area of the geometry.
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