class ScanResultData: 
    """
        A class that stores information about results of scanned X-ray 
        for database storage 
    """

    def __init__(self):
        self.results = None 
        self.percentage = None 
        self.orig_img = None 
        self.preproc_img = None
        self.gradcam_img = None 
        self.notes = None 
    
