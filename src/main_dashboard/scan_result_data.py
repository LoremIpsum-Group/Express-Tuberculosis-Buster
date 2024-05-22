class ScanResultData: 
    def __init__(self, result, percentage, orig_img, preproc_img, gradcam_img, notes):
        self.result = result
        self.percentage = percentage
        self.orig_img = orig_img
        self.preproc_img = preproc_img
        self.gradcam_img = gradcam_img
        self.notes = notes
    