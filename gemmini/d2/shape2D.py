from gemmini.misc import *
from gemmini.d2._gem2D import *
from gemmini.calc.coords import rotate_2D
from gemmini.d2.polygon2D import RegularPolygon

class Star(Geometry2D):
    def __init__(
        self,
        s:float = None,
        nD:int = None,
        nV:int = None, 
        **kwargs
    ):
        """
        A star polygon without intersecting edges.
        
        Args:
            s | size (float): distance between centroid and sharp corner of the star
            nD | num_dot (int): number of dots consisting of a edge
            nV | num_vertex (int): number of vertex
        """
        
        gem_type = self.__class__.__name__

        self.uS, self.nD, self.nV = assignArg(
            gem_type, 
            [s, nD, nV], 
            ['size', 'num_dot', 'num_vertex'], 
            kwargs
        )

        if self.nV < 3 :
            raise ValueError("[ERROR] %s should have at least 3 vertices"%(gem_type))

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side must have at least 2 dots"%(gem_type))

        super().__init__(gem_type=gem_type, **kwargs)

    def _base_coords(self) -> np.ndarray:
        ang = pi/self.nV
        orD = self.uS * sin(ang) / (cos(2*ang)*cos(ang) + sin(2*ang)*sin(ang))
        irD = self.uS / (cos(ang) + sin(ang)*tan(2*ang))

        coord_ss = self._draw_substar(orD)
        coord_ip = self.drawPolygon(irD, self.nD)

        coord = np.concatenate((coord_ss, coord_ip), axis=0)

        return coord
    
    def _draw_substar(self, orD):
        coord = []

        for v in range(self.nV):
            for e in reversed(range(self.nD-1)):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = -orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D(dx, dy, v*2*pi/self.nV)
                coord.append([rx, ry])
            for e in range(1, self.nD-1):
                dx = self.uS - orD*sin(2*pi/self.nV)*e/(self.nD-1)
                dy = orD*cos(2*pi/self.nV)*e/(self.nD-1)
                
                rx, ry = rotate_2D(dx, dy, v*2*pi/self.nV)
                coord.append([rx, ry])

        coord = np.array(coord)

        return coord

    def _draw_polygon(self, irD, inD):
        fig = RegularPolygon(size=irD, num_vertex=self.nV, num_dot=inD)
        fig.rotate(180/self.nV)

        return fig.get_subcoord()

    def __len__(self) -> int:
        return self.nV*(3*self.nD-4)
    
class WaveForm(Geometry2D):
    def __init__(
        self, 
        a:float = None,
        w:float = None,
        prd:float = None,
        nD:int = None,
        **kwargs
    ):
        """
        [파형]
        참고: WaveForm(Amplitude256-Width768-Period256-numDot96).png
        
        Args:
            amplitude (int): 진폭 (세로 높이)
            width (int): 너비
            period (int): 주기
            num_dot (int): 점의 수
        """
        
        self.aP = amplitude
        self.w = width
        self.prd = period
        self.nD = num_dot
        
        if period < 1 :
            raise InvalidParamError("[ERROR] 파형 그리기: 주기의 크기는 1 이상!")
        
        super().__init__(geom_type="파형", **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD)
        rad = self.aP * np.sin(theta * self.w/self.prd)
        
        x = np.linspace(-self.w/2, self.w/2, self.nD)
        coord = np.stack((x, rad), axis=1)

        return coord

    def num_pixels(self):
        return self.nD

class Parabola(Shape):
    def __init__(
        self,
        width:int, 
        height:int,
        num_dot:int,
        **kwargs
    ):
        """
        [포물선]
        참고: Parabola(width384-height512-numDot32).png

        Args:
            width (int): 너비
            height (int): 높이
            num_dot (int): 점의 수
        """
        self.w = width
        self.h = height
        self.nD = num_dot
        
        super().__init__(geom_type="포물선", **kwargs)

    def get_subcoord(self):
        dx = np.linspace(-self.w/2, self.w/2, self.nD)
        dy = 4*self.h*np.power(dx, 2)/pow(self.w, 2) - self.h/2
        coord = np.stack((dx, dy), axis=1)

        return coord

    def num_pixels(self):
        return self.nD


class Polygontile(Geometry2D):
    def __init__(
        self,
        s:float = None,
        nD:int = None,
        nV:int = None,
        **kwargs
    ):
        """
        A pattern where the a polygon that placed in center is surrounded by another polygon shapes.

        Args:
            s | size (float): length of each side
            nD | num_dot (int): number of dots consisting of a edge
            nV | num_vertex (int): number of vertex
        """
        
        gem_type = self.__class__.__name__

        self.uS, self.nD, self.nV = assignArg(
            gem_type, 
            [s, nD, nV], 
            ['size', 'num_dot', 'num_vertex'], 
            kwargs
        )

        if self.nV < 3 :
            raise ValueError("[ERROR] %s should have at least 3 vertices"%(gem_type))

        if self.nD < 2 :
            raise ValueError("[ERROR] %s: each side must have at least 2 dots"%(gem_type))
        
        super().__init__(gem_type=gem_type, **kwargs)
        
    def _base_coords(self) -> np.ndarray:
        irD = 2 * tan(pi/self.nV) * self.uS / (2 + 1/cos(pi/self.nV))
        fa = RegularPolygon(size=irD, num_dot=self.nD, num_vertex=self.nV)
        res = fa.clone()
        
        for i in range(self.nV):
            angle = (270 + 360*i//self.nV)*pi/180
            mx, my = 0, irD/tan(pi/self.nV)
            dx, dy = rotate_2D(mx, my, 2*i*pi/self.nV)
            fb = fa.clone()
            fb.rotate(360*i/self.nV + 180)
            fb.translate(int(dx), int(dy))
            res = union(res, fb)
        
        coord = np.array(res[:])

        return coord
        
    def __len__(self) -> int:
        return self.nV*(self.nV+1)*(self.nD-1) - self.nD * self.nV
    
class LogSpiral(Geometry2D):
    def __init__(
        self, 
        size:int,
        num_rot:float,
        num_vertex:int,
        **kwargs
    ):
        """
        [로그 나선]

        Args:
            size (int): 지름
            num_rot (float): 나선 회전 수
            num_vertex (int): 날개의 수
        """
        
        self.rD = size
        self.nR = num_rot
        self.nV = num_vertex

        if self.nR < 1 :
            raise InvalidParamError("[ERROR] 로그나선 그리기: 회전 수는 1 이상!")
        
        if self.nV < 3 :
            raise InvalidParamError("[ERROR] 로그나선 그리기: 꼭짓점 개수는 3 이상!")

        super().__init__(geom_type="로그나선", **kwargs)

    def get_subcoord(self):
        coord = np.array([[self.drawVertex(j, i) for j in range(self.nR)] for i in range(self.nV)])
        coord = coord.reshape(-1, coord.shape[-1])
        return coord

    def num_pixels(self):
        return self.nR*self.nV
        
    def r_x(self, x, y, angle):
        a = angle/360 * 2*pi
        return cos(a)*x - sin(a)*y
    
    def r_y(self, x, y, angle):
        a = angle/360 * 2*pi
        return sin(a)*x + cos(a)*y

    def drawVertex(self, r, v):
        size = self.rD*r/self.nR
        e = exp(1)
        pitch = 90*(self.nV - 2)/self.nV * 2*pi/360
        
        a = 1
        b = 1/tan(pitch)
        s = self.rD - size
        t = log(b*s/(a*sqrt(1+b**2)))/b
        
        gr = a*pow(e, (b*t))
        
        x = gr*cos(t)
        y = gr*sin(t)

        rx = floor(self.r_x(x, y, v*360/self.nV + self.iA))
        ry = floor(self.r_y(x, y, v*360/self.nV + self.iA))

        return rx, ry
    
class Crossroad(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        num_vertex:int, 
        width_rate:float=1.0, 
        **kwargs
    ):
        """
        [교차로]
        참고: Crossroad(size256-numDot8-numVertex6).png
        
        Args:
            size (int): 크기
            num_dot (int): 한 변당 점의 수
            num_vertex (int): 꼭짓점 수
            width_rate (float): 교차로 폭 비율 \
            (값이 낮을수록 폭이 좁습니다)
        """
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex
        self.sD = 1/width_rate
        
        if num_vertex < 4 or num_vertex%2 != 0:
            raise InvalidParamError("[ERROR] 교차로 그리기: 별의 꼭짓점 수는 최소 4개 이상 AND 2의 배수")

        if self.nD < 2 :
            raise InvalidParamError("[ERROR] 교차로 그리기: 한 변당 점 개수는 2 이상!")
        
        super().__init__(geom_type="교차로", **kwargs)

    def get_subcoord(self):
        coord = []

        for e in range(self.nD):
            irD = self.rD * tan(2*pi/self.nV)/2 + self.rD * e/self.nD

            for v in range(self.nV):
                cx = self.rD * cos(2*v*pi/self.nV)/2
                cy = self.rD * sin(2*v*pi/self.nV)/2
                
                dx_1 = cx + self.sD*irD*cos(2*v*pi/self.nV - pi/2)
                dy_1 = cy + self.sD*irD*sin(2*v*pi/self.nV - pi/2)
                coord.append([dx_1, dy_1])

                dx_2 = cx + self.sD*irD*cos(2*v*pi/self.nV + pi/2)
                dy_2 = cy + self.sD*irD*sin(2*v*pi/self.nV + pi/2)
                coord.append([dx_2, dy_2])

        coord = np.array(coord)/(self.sD*(1 + tan(2*pi/self.nV)/2))

        return coord

    def num_pixels(self):
        return 2*self.nD*self.nV
    
class WindmillA(Shape):
    def __init__(
        self, 
        size:int,
        num_dot:int,
        num_vertex:int,
        wheel_length=1.25, 
        **kwargs
    ):
        """
        [바람개비 A] \
        참고: WindmillA(size256-numDot6-numVertex6).png

        Args:
            size (int): 크기
            num_dot (int): 날개 하나당 점의 수
            num_vertex (int): 날개의 수
            wheel_length (float, optional): 날개 축의 길이 배율 \
            (높을 수록 날이 더 길어집니다.)
        """
        
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex
        self.sD = wheel_length
        
        if num_vertex < 3 :
            raise InvalidParamError("[ERROR] 바람개비 그리기: 꼭짓점 수는 최소 3개 이상!")

        if self.nD < 2 :
            raise InvalidParamError("[ERROR] 바람개비 그리기: 한 변당 점 개수는 2 이상!")
        
        super().__init__(geom_type="바람개비", **kwargs)

    def get_subcoord(self):
        irD = self.rD * cos(2*pi/self.nV)/cos(pi/self.nV)
        erD = self.rD * sin(2*pi/self.nV) - irD * sin(pi/self.nV)

        def drawVertex(e, v):
            cx = irD * cos(2*v*pi/self.nV)
            cy = irD * sin(2*v*pi/self.nV)
            
            dx = cx + self.sD*erD*cos(pi/2 + (2*v-1)*pi/self.nV)*e/self.nD
            dy = cy + self.sD*erD*sin(pi/2 + (2*v-1)*pi/self.nV)*e/self.nD
            
            return dx, dy

        coord = np.array([[drawVertex(i+1, j) for j in range(self.nV)] for i in range(self.nD)])
        coord = coord.reshape(-1, coord.shape[-1])

        return coord

    def num_pixels(self):
        return self.nD*self.nV
    
    
class WindMill2(Shape):
    def __init__(
        self, 
        size:int,
        num_dot:int,
        num_vertex:int,
        wheel_length=2, 
        **kwargs
    ):
        """
        [바람개비 B]
        참고: WindmillB(size400-numDot8-numVertex6).png

        Args:
            size (int): 크기
            num_dot (int): 날개 하나당 점의 수
            num_vertex (int): 날개의 수
            wheel_length (int, optional): 날개 축의 길이 배율 \
            (높을 수록 날이 더 길어집니다.)
        """
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex
        self.sD = wheel_length
        
        if self.nV < 3 :
            raise InvalidParamError("[ERROR] 바람개비 B 그리기: 꼭짓점 수는 최소 3개 이상!")

        if self.nD < 2 :
            raise InvalidParamError("[ERROR] 바람개비 B 그리기: 한 변당 점 개수는 2 이상!")
        
        if self.sD <= 0 :
            raise InvalidParamError("[ERROR] 바람개비 B 그리기: 날개축 길이 관련 인자(wheel_length)는 0보다 커야합니다.")
        
        super().__init__(geom_type="바람개비 B", **kwargs)

    def get_subcoord(self):
        irD = self.rD / (2*cos(pi/2 - pi/self.nV))

        def drawVertex(e, v):
            cx = irD * cos(2*v*pi/self.nV)
            cy = irD * sin(2*v*pi/self.nV)
            
            dx = cx/self.sD + self.rD*cos(pi/2 + (2*v+1)*pi/self.nV)*e/self.nD
            dy = cy/self.sD + self.rD*sin(pi/2 + (2*v+1)*pi/self.nV)*e/self.nD
            
            return dx, dy

        coord = np.array([[drawVertex(i+1, j) for j in range(self.nV)] for i in range(self.nD)])
        coord = coord.reshape(-1, coord.shape[-1])

        return coord

    def num_pixels(self):
        return self.nD*self.nV
    
class BoomerangB(Shape):
    def __init__(
        self, 
        size:int,
        num_dot:int,
        num_vertex:int, 
        **kwargs
    ):
        """
        [부메랑 B]
        참고: BoomerangB(size400-numDot96-numVertex3).png

        Args:
            size (int): 크기
            num_dot (int): 전체 점의 수
            num_vertex (int): 날개의 수
        """
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex

        if self.nD < 1 :
            raise InvalidParamError("[ERROR] 부메랑 B 그리기: 점 개수는 1 이상!")

        if self.nV < 2 :
            raise InvalidParamError("[ERROR] 부메랑 B 그리기: 꼭짓점 개수는 2 이상!")
        
        super().__init__(geom_type="부메랑 B", polar=True, **kwargs)
        
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*((self.nV+1)*np.cos(np.cos(self.nV*theta)) + np.sin(np.sin(self.nV*theta)))/(self.nV+2)

        coord = polar_pixels(rad, theta)
        return coord

    def num_pixels(self):
        return self.nD
    
    
class Cotton(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        num_vertex:int, 
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [뭉게구름]
        Epicycloid에서 beta 값만 1로 준것과 동일합니다 \
        참고: Cotton(size300-numDot256-numVertex6).png
        
        Args:
            size (int): 크기
            num_dot (int): 전체 점의 수
            num_vertex (int): 꼭짓점 수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex

        if self.nV < 3 :
            raise InvalidParamError("[ERROR] 뭉게구름 그리기: 꼭짓점 개수는 3 이상!")
        
        super().__init__(geom_type="뭉게구름", polar=True,  density=density, fill=fill, **kwargs)

    def get_subcoord(self):
        fig = Epicycloid(size=self.rD, num_dot=self.nD, alpha=self.nV, beta=1)

        return np.array(fig[:])

    def num_pixels(self):
        return self.nD
    
    
class ButterFly(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [나비]
        참고: ButterFly(size300-numDot128)
        
        Args:
            size (int): 크기
            num_dot (int): 전체 점의 수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot
        
        super().__init__(geom_type="나비", polar=True, density=density, fill=fill, **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*(1.35 - np.cos(theta - np.pi/3) * np.sin(3*(theta - np.pi/3)))

        leftside = np.where(
            (theta >= np.pi/2) &
            (theta <= 3*np.pi/2)
        )

        rad[leftside] = self.rD*(1.35 - np.cos(2*np.pi/3 - theta[leftside]) * np.sin(3*(2*np.pi/3 - theta[leftside])))

        coord = polar_pixels(rad, theta)/1.35
        return coord

    def num_pixels(self):
        return self.nD


class ShurikenA(Shape):
    def __init__(
        self, 
        long_side:int,
        short_side:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [수리검A]
        메이플스토리에서 도적 기본 표창(수비표창)으로 주는 거 생각하시면 될듯 \
        참고: ShurikenA(long_side300-short_side150-numDot8).png

        Args:
            long_side (int): 수리검의 지름
            short_side (int): 수리검의 안쪽 지름(안쪽으로 패인 곳) \
            여러번 그려보면 대충 뭔지 감 오실듯??
            num_dot (int): 한 변의 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.lS = long_side
        self.sS = short_side
        self.nD = num_dot
        
        if self.nD < 2 :
            raise InvalidParamError("[ERROR] 수리검A 그리기: 한 변당 점 개수는 2 이상!")
        
        super().__init__(geom_type="수리검A", density=density, fill=fill, **kwargs)
        
    def drawEdge(self):
        i = np.arange(self.nD)
        lb = self.sS *sqrt(2)/2
        
        x_a = self.lS - (self.lS - lb)*i/(self.nD - 1)
        y_a = lb * i/(self.nD - 1)
        coord_a = np.vstack((x_a, y_a)).T
        
        j = np.arange(1, self.nD-1)[::-1]
        x_b = lb * j/(self.nD - 1)
        y_b = self.lS - (self.lS - lb) * j/(self.nD - 1)
        coord_b = np.vstack((x_b, y_b)).T
        
        coord = np.concatenate((coord_a, coord_b), axis=0)
        return coord

    def get_subcoord(self):
        edge_right = self.drawEdge()
        
        edge_up = rotate_ndarray(edge_right, pi/2)
        edge_left = rotate_ndarray(edge_right, pi)
        edge_down = rotate_ndarray(edge_right, 3*pi/2)
        
        coord = np.concatenate((edge_right, edge_up, edge_left, edge_down), axis=0)

        return coord

    def num_pixels(self):
        return 8*(self.nD - 1)
    

class Heart(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [하트]
        
        Args:
            size (int): 크기
            num_dot (int): 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot
        
        if self.nD < 1 :
            raise InvalidParamError("[ERROR] 하트 그리기: 점 개수는 1 이상!")
        
        super().__init__(geom_type="하트", density=density, fill=fill, polar=True, **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*(2 - 2.3*np.sin(theta) + 0.4*np.cos(2*theta) + (1.3*np.sin(theta) * np.sqrt(np.power(np.abs(np.cos(theta)), 1.3)))/(np.sin(theta) + 1.7))/3

        coord = polar_pixels(rad, theta)
        return coord

    def num_pixels(self):
        return self.nD
    
    
class Moon(Shape):
    def __init__(
        self, 
        size:int,
        num_dot:int,
        breadth:float,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [초승달]
        참고: Moon(size720-numDot48-breadth0.5).png

        Args:
            size (int): 원의 지름
            num_dot (int): 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot
        self.bR = breadth
        
        if breadth <= 0 or breadth >= 1:
            raise InvalidParamError("[ERROR] 초승달 그리기: breadth 인자의 범위는 0 < x < 1!")

        super().__init__(geom_type="초승달", density=density, fill=fill, polar=True, **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*np.ones_like(theta)/2

        coord = polar_pixels(rad, theta)
        fliped_idx = np.where(coord[:, 0] <= -self.bR*self.rD/2)
        coord[fliped_idx, 0] = -self.bR*self.rD - coord[fliped_idx, 0]

        return coord

    def num_pixels(self):
        return self.nD
    
    
class Yinyang(Shape):
    def __init__(
        self, 
        size:int,
        num_dot:int,
        **kwargs
    ):
        """
        [태극]
        참조: Yinyang(size400-numDot90).png
        
        Args:
            size (int): 지름
            num_dot (int): 점의 개수
        """
        self.rD = size
        self.nD = num_dot
        
        super().__init__(geom_type="태극", polar=True, **kwargs)
        
    def __getRad1__(self, ang):
        return self.rD*np.ones_like(ang)
    
    def __getRad2__(self, ang):
        return self.rD * (-np.cos(ang + np.sin(ang)) + 1)/2
    
    def __getRad3__(self, ang):
        return self.rD * (np.cos(ang + np.sin(ang)) - 1)/2
    
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD)
        
        rad1 = self.__getRad1__(theta)
        rad2 = self.__getRad2__(theta[:self.nD//3])
        rad3 = self.__getRad3__(theta[:self.nD//3])
        
        coord = []
        
        for i in range(self.nD):
            if i%2 == 0:
                coord.append(polar_pixels(rad1[i//2], theta[i//2])[0])
                coord.append(polar_pixels(rad1[i//2 + self.nD//2], theta[i//2 + self.nD//2])[0])
            if i%3 == 0:
                coord.append(polar_pixels(rad2[i//3], theta[i//3])[0])
                coord.append(polar_pixels(rad3[i//3], theta[i//3])[0])
                
        return np.array(coord)

    def num_pixels(self):
        return self.nD
    
class Spring(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        num_rot:int, 
        **kwargs
    ):
        """
        [용수철]
        참고: Spring(size128-numDot96-numRot3).png

        Args:
            size (int): 지름
            num_dot (int): 점의 개수
            num_rot (int): 회전 수
        """
        
        self.rD = size
        self.nD = num_dot
        self.nR = num_rot

        super().__init__(geom_type="용수철", **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, self.nR*2*np.pi, self.nD)
        height = np.linspace(0, self.nR, self.nD)
        rad = self.rD*np.ones_like(theta)
        coord = np.stack((rad*np.cos(theta), -rad*(np.sin(theta) + height)), axis=1)

        return coord

    def num_pixels(self):
        return self.nD
    
    
class FlowerA(Shape):
    def __init__(
        self,
        size:int,
        num_leaf:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [꽃잎A]
        참고: FlowerA(size300-numVertex6-numDot144).png
        
        Args:
            size (int): 크기
            num_leaf (int): 꽃잎 수
            num_dot (int): 전체 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nV = num_leaf
        self.nD = num_dot
        
        if self.nV < 1:
            raise InvalidParamError("[ERROR] 꽃잎A 그리기: 꼭짓점 개수는 1 이상!")
        
        super().__init__(geom_type="꽃잎A", density=density, fill=fill, polar=True, **kwargs)
        
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*(2 - np.power(np.sin(self.nV*theta), 3))/3
        
        coord = polar_pixels(rad, theta)
        return coord

    def num_pixels(self):
        return self.nD
    

class FlowerB(Shape):
    def __init__(
        self,
        size:int,
        num_leaf:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [꽃잎B]
        참고: FlowerB(size300-numLeaf5-numDot25).png

        Args:
            size (int): 크기
            num_leaf (int): 꽃잎 수
            num_dot (int): 전체 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        self.rD = size
        self.nV = num_leaf
        self.nD = num_dot
        
        if self.nV < 2 :
            raise InvalidParamError("[ERROR] 꽃잎B 그리기: 꽃잎 수는 2 이상!")
        
        super().__init__(geom_type="꽃잎B", density=density, fill=fill, **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, np.pi/self.nV, self.nD+2)[1:-1]
        rad = 300 *np.sin(self.nV*theta)
        
        coord_oneside = polar_pixels(rad, theta)
        coord = np.copy(coord_oneside)
        
        for i in range(1, self.nV):
            coord = np.concatenate((coord, rotate_ndarray(coord_oneside, 2*i*pi/self.nV)), axis=0)

        return coord

    def num_pixels(self):
        return self.nD
    

class FlowerC(Shape):
    def __init__(
        self,
        size:int,
        num_leaf:int,
        num_dot:int,
        **kwargs
    ):
        """
        [꽃잎C]
        참고: FlowerC(size384-numLeaf5-numDot120).png

        Args:
            size (int): 크기
            num_leaf (int): 꽃잎 수
            num_dot (int): 전체 점의 개수
        """
        self.rD = size
        self.nV = num_leaf
        self.nD = num_dot
        
        if self.nV < 2 or self.nV%2 == 0:
            raise InvalidParamError("[ERROR] 꽃잎C 그리기: 꽃잎 수는 2 이상의 홀수!")
        
        super().__init__(geom_type="꽃잎C", **kwargs)

    def get_subcoord(self):
        theta = np.linspace(0, 4*np.pi, self.nD+1)[:-1]
        rad = self.rD * (2 + np.cos(self.nV*theta/2))/3
            
        coord = polar_pixels(rad, theta)
        return coord

    def num_pixels(self):
        return self.nD
    
    
class FlowerD(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        num_leaf:int,
        **kwargs
    ):
        """
        [꽃잎D]
        코스모스처럼 생긴 꽃잎입니다.
        참고: FlowerD(size384-numLeaf5-numDot9).png

        Args:
            size (int): 크기
            num_leaf (int): 꽃잎 수
            num_dot (int): 꽃잎당 점의 개수
        """
        
        self.rD = size
        self.nD = num_dot
        self.nV = num_leaf

        if self.nD < 3 :
            raise InvalidParamError("[ERROR] 꽃잎D 그리기: 점 개수는 3 이상!")
        
        super().__init__(geom_type="꽃잎D", **kwargs)
        
    def get_subcoord(self):
        if self.nD%2 == 0 :
            theta = np.linspace(0, 4*np.pi, 12*(self.nD+1)+1)[:-1]
        else :
            theta = np.linspace(0, 4*np.pi, 24*(self.nD//2 + 1)+1)[:-1]
            
        rad = self.rD * np.cos(3*theta/2)
        coord = polar_pixels(rad, theta)
        one_leaf = sqrt(2)*np.concatenate((coord[self.nD+2:3*self.nD//2+2], coord[9*self.nD//2+5:5*self.nD+5]), axis=0)
            
        res = one_leaf.copy()
        
        for i in range(1, self.nV):
            tp = rotate_ndarray(one_leaf, 2*pi*i/self.nV)
            res = np.concatenate((res, tp), axis=0)

        return res

    def num_pixels(self):
        return self.nD*self.nV

class ConcaveStar(Shape):
    def __init__(
        self,
        size:int,
        num_vertex:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [볼록별]
        참고: ConcaveStar(size256-numVertex5-numDot144).png

        Args:
            size (int): 크기
            num_vertex (int): 꼭짓점 수
            num_dot (int): 전체 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        self.rD = size
        self.nV = num_vertex
        self.nD = num_dot
        
        if self.nV < 3:
            raise InvalidParamError("[ERROR] 볼록별 그리기: 꼭짓점 개수는 3 이상!")
        
        super().__init__(geom_type="볼록별", density=density, fill=fill, polar=True, **kwargs)
        
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = self.rD*(1.5 - np.power(np.sin(self.nV*theta/2)/2 + np.cos(self.nV*theta/2)/2, 2))
        
        coord = polar_pixels(rad, theta)
        return coord

    def num_pixels(self):
        return self.nD
    

class CrossA(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [십자가 A]
        참고: CrossA(size256-numDot64).png

        Args:
            size (int): 크기
            num_dot (int): 전체 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot

        if self.nD < 1 :
            raise InvalidParamError("[ERROR] 십자가 A 그리기: 점 개수는 1 이상!")
        
        super().__init__(geom_type="십자가 A", density=density, fill=fill, **kwargs)
        
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = 15/(16*np.abs(np.sin(2*theta)))
        rad = np.power(rad, 0.5)
        rad = self.rD * np.minimum(rad/1.5, np.ones_like(theta))
        
        coord = polar_pixels(rad, theta)

        return coord

    def num_pixels(self):
        return self.nD
    

class CrossB(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        """
        [십자가 B]
        참고: CrossA(size256-numDot64).png

        Args:
            size (int): 크기
            num_dot (int): 전체 점의 개수
            density (int, optional): 해상도를 결정하는 수치입니다. \
                값이 높을수록 해상도와 품질이 떨어집니다 (계단 현상↑).
            fill (bool):
                False = 도형의 테두리만 그린다
                True = 도형 내부까지 채운다
        """
        
        self.rD = size
        self.nD = num_dot

        if self.nD < 1 :
            raise InvalidParamError("[ERROR] 십자가 B 그리기: 점 개수는 1 이상!")
        
        super().__init__(geom_type="십자가 B", density=density, fill=fill, **kwargs)
        
    def get_subcoord(self):
        theta = np.linspace(0, 2*np.pi, self.nD+1)[:-1]
        rad = 15/(16*np.abs(np.sin(2*theta)))
        rad = np.power(rad, 2.5)
        rad = self.rD * np.minimum(rad/1.5, np.ones_like(theta))
        
        coord = polar_pixels(rad, theta)

        return coord

    def num_pixels(self):
        return self.nD
            
            
    

class UnknownB(Shape):
    def __init__(
        self,
        size:int,
        num_dot:int,
        num_vertex:int,
        density:int = 1,
        fill:bool = False,
        **kwargs
    ):
        self.rD = size
        self.nD = num_dot
        self.nV = num_vertex

        if self.nD < 1 :
            raise InvalidParamError("[ERROR] 십자가 B 그리기: 점 개수는 1 이상!")
        
        super().__init__(geom_type="십자가 B", density=density, fill=fill, **kwargs)
        
    def get_subcoord(self):
        nL = self.nV if self.nV%2 == 0 else self.nV + 1
        
        if nL%4 == 0:
            theta = np.linspace(0, 6*np.pi, 24*self.nD)[:-1]
            rad = self.rD * np.cos(nL*theta/(nL - 1))
        
        
        theta = np.linspace(0, 2*(nL - 1)*np.pi, 2*nL*(nL//2 - 1)*self.nD+1)[:-1]
        rad = self.rD * np.cos(nL*theta/(nL - 1))
        #theta = np.linspace(0, 2*(nL//2 - 1)*np.pi, 2*nL*(nL//2 - 1)*self.nD+1)[:-1]
        #rad = self.rD * np.cos((nL//2)*theta/(nL//2 - 1))
        #theta = np.linspace(0, 4*np.pi, self.nD+1)[:-1]
        #rad = self.rD * np.cos(3*theta/2)
        
        coord = polar_pixels(rad, theta)
        irD = sqrt(coord[self.nD][0]**2 + coord[self.nD][1] ** 2)
        inner = np.where(coord[:, 0]**2 + coord[:, 1]**2 <= irD**2 + 0.1)
        coord = coord[inner]
        
        coord = np.unique(coord, axis=0)
        
        return coord

    def num_pixels(self):
        return self.nD
    
            
def _extract_pixels(pix, size, c):
    rw, rh, _ = pix.shape
    coord = np.column_stack(
        np.where(
            (pix[:,:,c] == 255) &
            (pix[:,:,(c+1)%3] == 0) &
            (pix[:,:,(c+2)%3] == 0)
        )
    )

    coord[:, 0] = np.round(size/rw * coord[:, 0])
    coord[:, 1] = np.round(size/rh * coord[:, 1])
    coord = coord - (size/2)
    
    return coord
    
def ImageFig(size, file_name, style='rgb', density=32, **kwargs):
    if style == 'rgb':
        img = im.open(file_name).convert("RGB")
        pix = np.array(img)
        
        f_r = CustomFig(coord = _extract_pixels(pix, size, 0), density=density, **kwargs)
        f_g = CustomFig(coord = _extract_pixels(pix, size, 1), density=density, **kwargs)
        f_b = CustomFig(coord = _extract_pixels(pix, size, 2), density=density, **kwargs)
        
        if len(f_g) != 0 :
            f_g = sub(f_g, f_r, 32)
        if len(f_b) != 0 :
            f_b = sub(f_b, [f_r, f_g], 32)
        
        return f_r, f_g, f_b
    else :
        img = im.open(file_name).convert("RGBA")
        rw, rh = img.size
        pix = np.array(img)
        
        trans_mask = pix[:,:,3] == 0
        pix[trans_mask] = [255, 255, 255, 255]
        pix = np.dot(pix[...,:3], [0.299, 0.587, 0.114])
        
        coord = np.column_stack(np.where(pix < 128))
        coord[:, 0] = np.round(size/rw * coord[:, 0])
        coord[:, 1] = np.round(size/rh * coord[:, 1])
        coord = coord - (size/2)
        
        return CustomFig(coord=coord, **kwargs)