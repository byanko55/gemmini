
from gemplib.misc import *

class Geometry:
    def __init__(
        self,
        gem_type:str,
        **kwargs
    ) -> None:
        """
        Basic structure of gemplib geometry instance
        It also includes a collection of transformation operations.

        All subclasses should overwrite 
            1) `coords`, a list of (x, y) coordinates of vertices.
            2) `size`, indicating the diameter (or the longest distance between two different pixels).
            3) `__len__`, which is expected to return the diameter of the given geometry.
            4) `__getitem__`, supporting fetching a pixel point for a given index.

        Args:
            gem_type (str): explicit type of a geometric object
        """
        self.gem_type = gem_type

    def plot(self) -> None:
        """
        Draw a geometry instance on a canvas
        """
        plt.rc('font', family='DejaVu Sans', size=10)
        fig=plt.figure(figsize=(5, 5))
        ax=fig.add_axes([0,0,1,1])

        xs, ys = self.x_and_y()
        x_min, y_min, x_max, y_max = bounding_box(self)
        x_mean, y_mean = centroid(self)

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

    def x_and_y(self) -> Tuple[Any, Any]:
        """
        Returns the list of pixel position on x axis and y axis, respectively  
        """
        cd = self.coords()
        return cd[:, 0], cd[:, 1]

    def coords(self) -> np.ndarray:
        """
        Returns a list of (x, y) coordinates for the pixels
        """
        raise NotImplementedError

    def size(self) -> float:
        """
        Returns the diameter
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """
        Returns the number of pixels
        """
        raise NotImplementedError

    def __getitem__(self, item:int) -> Tuple[Any, Any]:
        raise NotImplementedError

        
def bounding_box(gem:Geometry) -> Tuple[float, float, float, float]:
    """
    border's coordinates on the X and Y axes that enclose a geometric object

    Returns:
        (x_min, y_min, x_max, y_max): the minimum/maximum position of x, y axes
    """
    xs, ys = gem.x_and_y()

    return min(xs), min(ys), max(xs), max(ys)

def centroid(gem:Geometry) -> Tuple[float, float]:
    """
    The center (x, y) coordinate of a geometric object

    Returns:
        (x_mean, y_mean): the average x and y coordinate
    """
    xs, ys = gem.x_and_y()

    return np.mean(xs), np.mean(ys)
