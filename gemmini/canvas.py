from gemmini.misc import *
from gemmini.d2 import Geometry2D, Line2D

class Canvas:
    def __init__(
        self,
        figsize:Tuple[float, float]=(5,5),
        fontsize:int=10,
        scale:float = 1.0,
        draw_grid:bool = True,
        major_ticks:bool = True,
        minor_ticks:bool = True
    ):
        self.figsize = figsize
        self.fontsize = fontsize
        self.scale = scale
        self.draw_grid = draw_grid
        self.draw_major = major_ticks
        self.draw_minor = minor_ticks
        self.gems = list()

    def plot(self):
        plt.rc('font', family='DejaVu Sans', size=self.fontsize)
        fig=plt.figure(figsize=self.figsize)
        ax=fig.add_axes([0,0,1,1])

        cx, cy, box_size = map(int, [0]*3)
        
        gem_configs = sorted(self.gems, key=lambda f: isinstance(f['fig'], Line2D))

        for i, g_config in enumerate(gem_configs):
            g = g_config['fig']

            if isinstance(g, Line2D):
                plt.axline(
                    xy1=g.p1,
                    xy2=g.p2,
                    slope=g.slope,
                    linewidth = g_config['opt_s'],
                    color = g_config['opt_c'],
                    linestyle = g_config['opt_m'],
                    zorder = i
                )

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
                xs, ys = g.coordsXY()
                plt.scatter(
                    xs, 
                    ys, 
                    s = g_config['opt_s'],
                    c = g_config['opt_c'],
                    marker = g_config['opt_m'],
                    zorder=i
                )

                x_min, y_min, x_max, y_max = g.bounding_box()

                ncx = (min(x_min, cx-box_size) + max(x_max, cx + box_size))/2
                ncy = (min(y_min, cy-box_size) + max(y_max, cy + box_size))/2
                nbs = max(
                    max(x_max, cx + box_size) - min(x_min, cx-box_size),
                    max(y_max, cy + box_size) - min(y_min, cy-box_size)
                )/2

                cx, cy, box_size = ncx, ncy, nbs

        _u = int(log10(max(1, 2*box_size*self.scale)))
        _u = 10 ** _u
        _v = (2*box_size*self.scale)//_u + 2
        canvas_size = _v * _u 
        lb, rb = cx - canvas_size/2, cx + canvas_size/2
        bb, tb = cy - canvas_size/2, cy + canvas_size/2

        ax.set_xlim([lb, rb])
        ax.set_ylim([bb, tb])

        _tu = _u*((_v-1)//2)

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
            ax.grid(which='both', color='#BDBDBD', linestyle='--', linewidth=1)
        else :
            plt.tick_params(left = False, right = False, labelleft = False, 
                labelbottom = False, bottom = False) 

        plt.show()

    def add(
        self, 
        gem:Union[Geometry2D, Line2D], 
        dot_size:int = 25,
        line_width:int = 2,
        marker_color:str = None,
        dot_style:str = 'o',
        line_style:str = '-',
        draw_edges:bool = False,
        draw_interior:bool = False
    ) -> None:
        if isinstance(gem, Geometry2D):
            fig_config = {
                'fig':gem, 
                'opt_s':dot_size, 
                'opt_c':marker_color, 
                'opt_m':dot_style,
                'opt_e':draw_edges,
                'opt_i':draw_interior
            }

            self.gems.append(fig_config)
        elif isinstance(gem, Line2D):
            fig_config = {
                'fig':gem, 
                'opt_s':line_width, 
                'opt_c':marker_color, 
                'opt_m':line_style
            }

            self.gems.append(fig_config)
        else :
            raise ValueError("[Error] Canva: the input geometry should be either Geometry2D or Line2D object")

    def remove(self, gem:Geometry2D) -> None:
        for i in range(len(self.gems)):
            if hash(self.gems[i]['fig']) == hash(gem):
                del self.gems[i]
                return
            
        warnings.warn("[WARN] Canvas: no such geometry exists on the figure list")

    def __len__(self) -> int:
        return len(self.gems)

    def __getitem__(self, item:int) -> Geometry2D:
        if len(self.gems) >= item:
            raise IndexError("[Error] Canvas: index out of bound")

        return self.gems[item]['fig']



    