import datetime

from main_dashboard.maindash_py_files.scan_result_data import ScanResultData as SRD

srd = SRD()
srd.results = 'Non-TB'
print(srd.results)

scan_date = datetime.datetime.now().strftime("%Y-%m-%d") 
print(scan_date)