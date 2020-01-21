from matplotlib.patches import Rectangle

class PlaneZone:
    
    def __init__(self, top, bottom, left=None, right=None):
        
        #plate is 17 inches
        #ball is 3 inches
        
        half_plate = 17/2/12
        half_ball = 3/2/12
        
        if left is None:
            left = -1 * half_plate
        if right is None:
            right = half_plate
        
        self.bottom = bottom - half_ball
        self.top = top + half_ball
        self.left = left - half_ball
        self.right = right + half_ball
        
    def is_pitch_in_zone(self, plate_x, plate_z):
        return (self.left <= plate_x <= self.right and self.top >= plate_z >= self.bottom)
    
    def get_patch(self):
        width = self.right * 2
        height = self.top - self.bottom
        return Rectangle((self.left, self.bottom), width, height, linewidth=1, edgecolor='r', facecolor='none')
    
    def extended_zone(self):
        # width of a baseball
        width = 3/12.0
        
        bottom = self.bottom - width
        top = self.top + width
        left = self.left - width
        right = self.right + width
        return PlaneZone(top, bottom, left, right)
    
    def __repr__(self):
        return f"top={self.top:.2f},bottom={self.bottom:.2f},left={self.left:.2f},right={self.right:.2f}"
    
    
def eye_good_result(row):
    """ returns a True if the following criteria are met:
        # if the batter let the pitch go
        * ball
        * called strike
        
        # if the batter saw the pitch as hittable and made good contact
        * hit into play with strong contact
        
        # if the batter is protecting with 2 strikes
        * foul if 2 strikes
    """
    if "ball" in row.description:
        return True
    if "called_strike" in row.description:
        return True
    if row.estimated_woba_using_speedangle > 0.4:
        return True
    if row.strikes == 2 and row.description == "foul":
        return True
    
    return False
    