from random import choice

class SquareWithFilling(object):
    """
    This class models a virtual square to be filled by lines moving with random speeds along its edges.
    """
            
    def __init__(self, x, y, size):
        """
        pos --> coordinate of the square's upper left corner
        size --> square's width and height size
        p1, p2 --> filling lines positions placed on the edges
        p1_edge, p2_edge --> edges where p1 and p2 are placed
        p1_edge_percent, p2_edge_percent --> considering the start as 0 and the end as 1, this holds the percentual the point had already moved along the edge
        p1_speed, p2_speed --> how fast the point will move over the edges
        """
        self.pos = PVector(x, y) 
        self.size = size
        self.p1, self.p1_edge, self.p1_edge_percent = self.get_random_edge_position()
        self.p2, self.p2_edge, self.p2_edge_percent = self.get_random_edge_position()
        self.p1_speed = random(0.001, 0.01) # this is not Python's random module, but a Processing's method 
        self.p2_speed = random(0.001, 0.01) # given a range of values, it returns a random value between the range

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
        
    def get_random_edge_position(self):
        """
        Return a PVector object placed on an edge
        """
        edge = choice(self.edges)
        percent = random(1)
        return PVector.lerp(edge[0], edge[1], percent), edge, percent

    def get_subsequent_edge(self, edge):
        """
        Given an edge, returns the subsequent edge starting in the edge's end
        """
        index = self.edges.index(edge)
        next_index = (index + 1) % len(self.edges)
        return self.edges[next_index]

    def update(self):
        """
        This function is responsible to move the filling.
        To do this we increase the point's edge_percent by the point speed
        So, with a new percent, we calculate the PVector corresponding to that edge's percent
        If the new percent is greater than 1, it means that the point had already covered all the edge
        In that case, it means the point now has to be placed in the beginning of the next edge 
        """
        
        # move P1
        self.p1_edge_percent += self.p1_speed
        if self.p1_edge_percent > 1:
            self.p1_edge_percent = 0
            self.p1_edge = self.get_subsequent_edge(self.p1_edge)
            
        edge = self.p1_edge
        self.p1 = PVector.lerp(edge[0], edge[1], self.p1_edge_percent)

        # move P2
        self.p2_edge_percent += self.p2_speed
        if self.p2_edge_percent >= 1:
            self.p2_edge_percent = 0
            self.p2_edge = self.get_subsequent_edge(self.p2_edge)
            
        edge = self.p2_edge
        self.p2 = PVector.lerp(edge[0], edge[1], self.p2_edge_percent)            

    def display(self):
        """
        Renders the filling
        """
        p1, p2 = self.p1, self.p2
        stroke(27)
        line(p1.x, p1.y, p2.x, p2.y)


square_with_filling = SquareWithFilling(100, 100, 700)
def setup():
    size(900, 900)
    background(242)
    
def draw():
    square_with_filling.update()
    square_with_filling.display()
