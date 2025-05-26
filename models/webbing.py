import numpy as np

from models.model_exception import StretchCurveException, WebbingException


class StretchCurve:
    def __init__(self, stretches: [float], forces: [float]):
        self.stretch = np.array(stretches)
        self.force = np.array(forces)

        if len(self.force) != len(self.stretch):
            raise StretchCurveException("Stretch Values and Forces have to be float lists of the same length")
        if len(self.force) < 2:
            raise StretchCurveException("A stretch curve needs at least 2 points")
        if self.force[0] != 0 or self.stretch[0] != 0:
            raise StretchCurveException("A stretch curve starts from point (0,0)")
        if not np.all(np.diff(self.force) > 0):
            raise StretchCurveException("Forces in a stretch curve have to be increasing")
        if not np.all(np.diff(self.stretch) > 0):
            raise StretchCurveException("Stretches in a stretch curve have to be increasing")


class Webbing:
    def __init__(self, name: str, stretches: list[float], forces: list[float], linear_weight: float):
        if linear_weight <= 0:
            raise WebbingException("weight of webbing has to be positive")
        if name.strip() == "":
            raise WebbingException("Name should not be empty")
        self.stretch_curve = StretchCurve(stretches, forces)
        self.linear_weight = linear_weight
        self.name = name

    def calculate_webbing_weight(self, length: float) -> dict:
        """
        Calculate the total weight of a webbing from JSON data
        
        Args:
            webbing_data (WebbingData): Webbing data from JSON
            length (float): Length of the webbing in meters
            
        Returns:
            dict: Dictionary containing weight information
            
        Raises:
            WebbingException: If webbing data or length is invalid
        """
        try:
            # Validate length
            if length <= 0:
                raise WebbingException("Length must be positive")
            
            # Validate webbing data (similar to Webbing constructor)
            if self.linear_weight <= 0:
                raise WebbingException("Linear weight must be positive")
            if self.name.strip() == "":
                raise WebbingException("Name should not be empty")
            
            # Validate stretch curve data
            stretches = self.stretch_curve.stretch
            forces = self.stretch_curve.force
            
            if len(forces) != len(stretches):
                raise StretchCurveException("Stretch values and forces must have the same length")
            if len(forces) < 2:
                raise StretchCurveException("A stretch curve needs at least 2 points")
            if forces[0] != 0 or stretches[0] != 0:
                raise StretchCurveException("A stretch curve starts from point (0,0)")
            
            # Calculate total weight
            total_weight = self.linear_weight * length
            
            return {
                "webbing_name": self.name,
                "length": length,
                "linear_weight": self.linear_weight,
                "total_weight": round(total_weight, 2),
                "unit": "grams"  # Assuming linear_weight is in g/m
            }
            
        except (WebbingException, StretchCurveException) as e:
            raise WebbingException(f"Invalid webbing data: {str(e)}")
        except Exception as e:
            raise WebbingException(f"Error calculating weight: {str(e)}")


