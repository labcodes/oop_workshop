from random import choice
from abc import ABCMeta, abstractmethod


class SquareWithFilling(object):
    """
    This class models a virtual square to be filled by lines moving with random speeds along its edges.
    """
            
    def __init__(self, x, y, size, filling):
        """
        pos --> coordinate of the square's upper left corner
        size --> square's width and height size
        filling --> object responsible to render and control the square filling
        """
        self.pos = PVector(x, y) 
        self.size = size
        self.filling = filling
        self.filling.configure(self.edges)

    @property
    def vertices(self):
        """
        Vertices visual positions:
            
        v1 --- v2
         |      |
         |      |
        v4 --- v3
        """
        w, h = self.size, self.size
        return [
            self.pos,  # v1
            self.pos + PVector(w, 0),  # v2
            self.pos + PVector(w, h),  # v3
            self.pos + PVector(0, h),  # v4
        ]        
            
    @property
    def edges(self):
        """
        Returns a list of tuples representing (edge_start, edge_end)
        """
        v = self.vertices
        return [(v[i - 1], v[i]) for i in range(4)]
          
    def update(self):
        self.filling.update()
    
    def display(self):
        self.filling.display()
        
        
class BaseShapeFilling(object):
    __metaclass__ = ABCMeta
    NUM_VERTEX = None  # should be defined by child classes as well
    
    @abstractmethod
    def display(self):
        pass
    
    def __init__(self, stroke_color=None):
        self.edges, self.vertices = [], []
        self.stroke_color = stroke_color or color(27, 27, 27)
        
    def configure(self, edges):
        self.edges = edges
        self.vertices = []
        for i in range(self.NUM_VERTEX):
            edge = choice(self.edges)
            self.vertices.append(FillingVertex(edge))
            
    def get_subsequent_edge(self, edge):
        """
        Given an edge, returns the subsequent edge starting in the edge's end
        """
        index = self.edges.index(edge)
        next_index = (index + 1) % len(self.edges)
        return self.edges[next_index]
    
    def get_previous_edge(self, edge):
        """
        Given an edge, returns the subsequent edge starting in the edge's end
        """
        index = self.edges.index(edge)
        return self.edges[index - 1]
    
    def update(self):
        """
        This function is responsible to move the filling.
        To do this we have to check if the point is able to move and, if not, place it on a new edge
        If the point has a reverse direction, we have to get the previous edge and, if not, the next one 
        """
        
        for filling_vertex in self.vertices:
            if not filling_vertex.can_move_on_edge():
                edge = filling_vertex.edge
                if filling_vertex.reverse_direction:
                    new_edge = self.get_previous_edge(edge)
                else:
                    new_edge = self.get_subsequent_edge(edge)
                filling_vertex.place_on_new_edge(new_edge)
            else:
                filling_vertex.move()

        
class LinesShapeFilling(BaseShapeFilling):
    NUM_VERTEX = 2
            
    def display(self):
        """
        Renders the filling
        """
        p1, p2 = self.vertices
        stroke(self.stroke_color)
        line(p1.x, p1.y, p2.x, p2.y)
        
                 
class TriangleShapeFilling(BaseShapeFilling):
    NUM_VERTEX = 3
                
    def display(self):
        """
        Renders the filling
        """
        p1, p2, p3 = self.vertices
        stroke(self.stroke_color)
        noFill()
        triangle(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)         


class FillingVertex(object):
    """
    Class to model a vertex moving along an edge
    """
    
    def __init__(self, edge):
        """
        edge --> current edge on which the vertex is placed
        speed --> how fast the point will move
        walked_percent --> to measure how far the point is from the edge start
        reverse_direction --> flag to control on which direction the vertex should move 
        """
        self.edge = edge
        self.speed = random(0.001, 0.01)
        self.walked_percent = random(1)
        self.reverse_direction = choice([True, False])
        
    @property
    def pos(self):
        """
        Property to compute the current position of the vertex on the edge
        If the vertex has a reverse direction, the percent should be applied from the edge end to its start
        Returns a PVector object
        """
        start, end = self.edge
        if self.reverse_direction:
            start, end = end, start
        return PVector.lerp(start, end, self.walked_percent)
        
    @property
    def x(self):
        return self.pos.x
           
    @property
    def y(self):
        return self.pos.y
        
    def can_move_on_edge(self):
        """
        The walked percent is incremented by the vertex speed
        If the sum is LEQ than 1, it means that the next position is still contained in the current edge
        """
        return self.walked_percent + self.speed <= 1
        
    def move(self):
        """
        Now to move a point is just a matter of to increase the walked_percent by a rate of the vertex's speed 
        """
        if not self.can_move_on_edge():
            return
        
        self.walked_percent += self.speed
        
    def place_on_new_edge(self, edge):
        """
        When a vertex transpass the edge line (can_move_on_edge returns False) it should be placed at the begining of a new edge
        This means we have to change the current edge and also set the walked percent to 0 so it can start to walk on the edge from its beginning
        """
        self.edge = edge
        self.walked_percent = 0


square_with_filling = SquareWithFilling(100, 100, 700, LinesShapeFilling())
def setup():
    size(900, 900)
    background(242)
    
def draw():
    square_with_filling.update()
    square_with_filling.display()
    
    
def keyPressed():
    global square_with_filling
    
    background(242)
    if key == 'l':
        square_with_filling = SquareWithFilling(100, 100, 700, LinesShapeFilling())
    elif key == 't':
        square_with_filling = SquareWithFilling(100, 100, 700, TriangleShapeFilling())
