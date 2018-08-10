# width, height = 1920+7, 1080+4
width, height = 1280+5, 720+3

cover_x, cover_y = 1280-20, 20
cover_w, cover_h = 300, 300*9/16

axis_l, axis_r = 100, width-cover_w-30
axis_b, axis_t = 100, 600

date_axis_segs = 200

video_view_threshold = 1e6
video_star_threshold = 5e6

total_hits = 0

level_counter = ['', 0]

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

def logisticX(base=2, val=0, offset=0, ratio=1):
    # map [0, +∞] to [0, 1]
    return 2*(1/(1+base**(-(val-offset)/ratio))-0.5)

def logistic(base=2, val=0, offset=0, ratio=1):
    # map [-∞, +∞] to [0, 1]
    return 1/(1+base**(-(val-offset)/ratio))

def escchar(texstr):
    # char_macro = ['~', '^', '\\']
    texstr = texstr.replace('\\','\\textbackslash ')
    # Put all after backslash
    texstr = texstr.replace('~','\\textasciitilde ')
    texstr = texstr.replace('^','\\textasciicircum ')

    char_slash = ['&', '%', '$', '#', '_', '{', '}']
    for char in char_slash:
        texstr = texstr.replace(char, '\\'+char+' ')

    return texstr