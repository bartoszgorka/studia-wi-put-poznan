from piro2.attendance_list import AttendanceList

def ocr(path, debug=False):
    attendance_list = AttendanceList(path, debug)
    return list(attendance_list.entries())
