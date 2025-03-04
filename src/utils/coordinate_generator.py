import pyproj
import math

class CoordinateConverter:
    def __init__(self, projection='WGS84'):
        self.transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
    
    def lat_lon_to_xy(self, latitude, longitude):
        """
        Convert latitude and longitude to X, Y coordinates
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
        
        Returns:
            tuple: (x, y) coordinates in meters
        """
        x, y = self.transformer.transform(longitude, latitude)
        return x, y
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two lat/lon points
        
        Args:
            lat1 (float): Latitude of first point
            lon1 (float): Longitude of first point
            lat2 (float): Latitude of second point
            lon2 (float): Longitude of second point
        
        Returns:
            float: Distance in kilometers
        """
        x1, y1 = self.lat_lon_to_xy(lat1, lon1)
        x2, y2 = self.lat_lon_to_xy(lat2, lon2)
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / 1000  # Convert to kilometers
        return distance