import re


# tm = '3 h 35 min'

def correct_time(tm):
    if re.findall(r'\d h \d\d min', tm):
        hour = tm[0:1].strip()
        mins = tm[4:6].strip()
        time = '0' + hour + ':' + mins + ':' + '00'
    elif re.findall(r'\d\d:\d\d:\d\d', tm):
        time = tm
    elif re.findall(r'\d:\d\d:\d\d', tm):
        time = '0' + tm
    else:
        time = tm

    return(time)

# correct_time(tm)