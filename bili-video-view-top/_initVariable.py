# width, height = 1920+7, 1080+4
width, height = 1280+5, 720+3

cover_x, cover_y = 920, 50
cover_w, cover_h = 350, 350*9/16

axis_l, axis_r = 100, cover_x-50
axis_b, axis_t = 100, 600

date_axis_segs = 200

def compareDate(date1, date2):
    # -1 A before B
    #  0 A equal  B
    #  1 A after  B
    if   date1['year'] < date2['year']:
        return -1
    elif date1['year'] > date2['year']:
        return  1
    else:
        if   date1['month'] < date2['month']:
            return -1
        elif date1['month'] > date2['month']:
            return  1
        else:
            if   date1['day'] < date2['day']:
                return -1
            elif date1['day'] > date2['day']:
                return  1
            else:
                if   date1['hour'] < date2['hour']:
                    return -1
                elif date1['hour'] > date2['hour']:
                    return  1
                else:
                    if   date1['minute'] < date2['minute']:
                        return -1
                    elif date1['minute'] > date2['minute']:
                        return  1
                    else:
                        return  0