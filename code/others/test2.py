def split_time(time_with_date, newspaper):
    if newspaper == 'delfi':
        s_time = time_with_date.split('T')
        date = s_time[0]
        s_time = s_time[1].split('+')
        time = s_time[0]
    
    return date, time

date,time = split_time("2020-09-23T18:59:24+0300", 'delfi')
print(date)
print(time)