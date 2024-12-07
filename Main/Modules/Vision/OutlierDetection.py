import numpy as np

class CalibrationOutlierDetection():
    def mad_based_outlier(self, points, threshold=3.5):
        """
        Detect outliers in 2D points using Median Absolute Deviation (MAD).
        
        Args:
        points (list of tuples): A list of (x, y) coordinates.
        threshold (float): The threshold to identify outliers. Default is 3.5.
        
        Returns:
        inliers (list): List of inliers (points that are not outliers).
        outliers (list): List of outliers.
        """
        
        # Convert points to numpy array
        points_array = np.array(points)
        
        # Calculate the centroid (median of x and y coordinates)
        centroid = np.median(points_array, axis=0)
        
        # Compute the Euclidean distance of each point to the centroid
        distances = np.linalg.norm(points_array - centroid, axis=1)
        
        # Compute the Median Absolute Deviation (MAD)
        median_distance = np.median(distances)
        mad = np.median(np.abs(distances - median_distance))
        
        # Avoid division by zero if MAD is zero
        if mad == 0:
            return points, []  # No outliers if all distances are essentially the same
        
        # Compute modified Z-scores using MAD
        modified_z_scores = 0.6745 * (distances - median_distance) / mad
        
        inliers = [points[i] for i in range(len(points)) if np.abs(modified_z_scores[i]) <= threshold]
        outliers = [points[i] for i in range(len(points)) if np.abs(modified_z_scores[i]) > threshold]
        
        return inliers, outliers

    def detect_outliers_in_data(self, data, threshold=3.5):
        """
        Detect outliers at the array level for a list of 2D point arrays using MAD.
        
        Args:
        data (list of lists of tuples): A list where each element is a list of four (x, y) tuples (points).
        threshold (float): The threshold to identify outliers. Default is 3.5.
        
        Returns:
        clean_data (list): List of arrays without outliers.
        arrays_with_outliers (list): List of arrays that contain outliers.
        """
        
        clean_data = []  # Arrays without outliers
        arrays_with_outliers = []  # Arrays containing outliers

        for points in data:
            inliers, outliers = self.mad_based_outlier(points, threshold=threshold)
            if outliers:
                arrays_with_outliers.append(points)  # Flag this array as containing outliers
            else:
                clean_data.append(points)  # This array has no outliers
        
        return clean_data, arrays_with_outliers
