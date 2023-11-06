"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# I know my functions aren't very efficient but they are readable...
# may optimize later if I can.


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    o_hours, o_mins = open(control_dist_km)
    open_t = brevet_start_time.replace(hour =+ o_hours, minute =+ o_mins)
    return open_t
    #return arrow.now()




def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    c_hours, c_mins = close(control_dist_km)
    close_t = brevet_start_time.replace(hour =+ c_hours, minute =+ c_mins)
    return close_t
    #return arrow.now()


def ctrl_time(dist, speed):
  total = dist / speed
  hours = math.floor(total)
  mins = round((total % 1)*60)
  return hours, mins

def add_times(times_list):
  hours = 0
  mins = 0
  for i in times_list:
    h, m = i
    mins = mins + m
    hours = hours + h
  while mins >= 60:
    hours += 1
    mins = mins - 60
  return hours, mins

def open(ctrl_loc):
  hours, mins = 0, 0
  speed = 34
  d = 200
  while ctrl_loc > 0:
    print(f"ctrl_loc = {ctrl_loc}")
    
    dist = min(d, ctrl_loc)
    print(f"dist = {dist}")
    print(f"speed = {speed}")

    h, m = ctrl_time(dist, speed)
    times = [(hours, mins), (h, m)]
    hours, mins = add_times(times)
    speed -= 2
    if speed < 28:
      ctrl_loc -= 400
    else:
      ctrl_loc -= 200
    if speed <30:
      d = 400

    
  return hours, mins

def close(ctrl_loc):
  speed = 15
  d = min(600, ctrl_loc)  
  h, m = ctrl_time(d, speed)
  ctrl_loc -= d
  if ctrl_loc > 0:
    speed = 11.428
    d = min(1000, ctrl_loc)
    h1, m1 = ctrl_time(d, speed)
    ctrl_loc -= d
    h, m = add_times([(h, m), (h1, m1)])
    if ctrl_loc > 0:
      speed = 13.333
      d = min(1300, ctrl_loc)
      h2, m2 = ctrl_time(d, speed)
      ctrl_loc -= d
      h, m = add_times([(h, m), (h2, m2)])
  return h, m

    

