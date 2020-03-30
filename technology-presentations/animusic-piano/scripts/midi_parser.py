# encoding: utf-8
from __future__ import print_function, division

# * MIDI文件格式解析 | 码农家园 
# ** https://www.codenong.com/js59d74800b43b/

# * 读书笔记——MIDI文件结构简介 - 哔哩哔哩 
# ** https://www.bilibili.com/read/cv1753143/

# * MIDI文件格式分析──理论篇 - Midifan：我们关注电脑音乐 
# ** https://m.midifan.com/article_body.php?id=901

# * Standard MIDI file format, updated 
# ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

# * Note names, MIDI numbers and frequencies 
# ** https://newt.phys.unsw.edu.au/jw/notes.html


# with open("abc.mid","rb") as rf:
# with open("secret1.mid","rb") as rf:
#     bytes_L = ["{:02x}".format(b) for b in rf.read()]

bytes_L = []

hexchr = "0123456789abcdef"

TPQN = -1   # ticks per quarter-note
USPQN = -1  # us per quarter-note
chan_inst_L = [] # channel num <-> instrument num
NUME, DENO = -1, -1


def get_bytes(start,end=None):
    if end == None:
        end = start+1
    return "".join(bytes_L[start:end]).lower()

def hex2dec(hex_str,signed=False):
    if signed == False:
        return int(hex_str,16)
    else:
        sign = 1 if hex_str[0]==0 else -1
        return sign*int(hex_str[1:],16)

def bin2dec(bin_str):
    return int(bin_str,2)

def hex2bin(hex_str):
    bit_num = len(hex_str)*4 
    return "{val:0{width}b}".format(val=hex2dec(hex_str),width=bit_num)


def parse_delta_time(ptr):
    """ return (int, int) : (pointer offset, num of tick) """
    # * Variable Length Values 
    # ** http://www.ccarh.org/courses/253/handout/vlv/
    byte = get_bytes(ptr)
    bin_str = hex2bin(byte)
    if bin_str[0]=="0":
        pass
    else:
        bin_str = bin_str[1:]
        ptr+=1
        tmp_str = hex2bin(get_bytes(ptr))
        while tmp_str[0]!="0":
            bin_str+=tmp_str[1:]
            ptr+=1
        bin_str+=tmp_str[1:]
    dt = bin2dec(bin_str)
    ptr+=1
    # print("dt: {} (ticks)".format(dt))
    return ptr, dt


def parse_event(ptr):
    """ return ptr, (event vars) """
    global USPQN, NUME, DENO
    byte = get_bytes(ptr)

    if byte == "ff":
    # Meta Event
    # * Standard MIDI file format, updated
    # ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BM3_1
        ptr += 1
        byte = get_bytes(ptr)

        if byte=="03":
            txt_len = hex2dec(get_bytes(ptr+1))
            ptr+=2
            trk_name = get_bytes(ptr,ptr+txt_len)
            print("Track name: {}".format(trk_name))
            ptr+=txt_len
            return ptr, trk_name

        elif byte=="2f":
            if get_bytes(ptr+1) != "00":
                print("x Invalid end notation!")
                return ptr, False
            print("=== End of track ===")
            ptr+=2
            return ptr, "EOT"

        elif byte=="51":
        # Set Tempo: FF 51 03 tttttt
        # (us per MIDI quarter-note)
            if get_bytes(ptr+1) != "03":
                print("x Invalid set tempo byte length!")
                return ptr, False
            ptr+=2
            USPQN = hex2dec(get_bytes(ptr,ptr+3))
            print("USPQN: {} (\u03BCs per quarter-note)".format(USPQN))
            ptr+=3
            return ptr, USPQN

        elif byte=="58":
        # Time Signature: FF 58 04 nn dd cc bb
        #   nn: numerator
        #   dd: denominator (2**dd)
        #   cc: num of MIDI clocks per metronome click
        #   bb: num of notated 32nd-notes in a MIDI quarter-note (24 MIDI clocks)
            if get_bytes(ptr+1) != "04":
                print("x Invalid time signature byte length!")
                return ptr, False
            ptr+=2
            nn = hex2dec(get_bytes(ptr))
            dd = 2**hex2dec(get_bytes(ptr+1))
            cc = hex2dec(get_bytes(ptr+2))
            bb = hex2dec(get_bytes(ptr+3))
            print("nn:{}, dd:{}, cc:{}, bb:{}".format(nn,dd,cc,bb))
            ptr+=4
            NUME,DENO = nn, dd
            return ptr,(nn,dd,cc,bb)

        elif byte=="59":
        # Key Signature: FF 59 02 sf mi 
        #   sf = -7:  7 flats
        #      = -1:  1 flat
        #      =  0:  key of C
        #      =  1:  1 sharp
        #      =  7:  7 sharps
        #   mi =  0:  major key
        #      =  1:  minor key
            if get_bytes(ptr+1) != "02":
                print("x Invalid key signature byte length!")
                return ptr, False
            ptr+=2
            sf = hex2dec(get_bytes(ptr),signed=True)
            mi = hex2dec(get_bytes(ptr+1),signed=True)
            print("sf:{}, mi:{}".format(sf,mi))
            ptr+=2
            return ptr, (sf,mi)

        else:
            print("x Unknown bytes of Meta-Event after {}!".format(byte))
            return ptr, False

    elif byte=="4d":
        if get_bytes(ptr+1)=="54":
            ptr+=2
            if get_bytes(ptr,ptr+2)=="726b":
                print("\n=== MTrk ===")
                ptr+=2
                mtrk_chk_len = hex2dec(get_bytes(ptr,ptr+4))
                print("MTrk chunk length: {} (bytes)".format(mtrk_chk_len))
                ptr+=4
                return ptr, mtrk_chk_len
            else:
                print("x Unknown bytes {} after 4d54 at ptr {}!".format(get_bytes(ptr),ptr))
                return ptr, False

    elif byte[0] in "89":
        # * MIDI Event Table
        # ** http://www33146ue.sakura.ne.jp/staff/iz/formats/midi-event.html
        # * Standard MIDI file format, updated 
        # ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA1_1
        if byte[0] == "8":
            switch = "OFF"
        else:
            switch = "ON"
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            pit_hex = get_bytes(ptr+1)
            pit_dec = hex2dec(pit_hex)
            velocity = hex2dec(get_bytes(ptr+2))
            # print("Chan {} note {} {:>3}, velocity: {:>2}".format(chan_num,pit_dec,switch,velocity))
            ptr+=3
            return ptr, (switch,chan_num,pit_dec,velocity)
        else:
            print("x Invalid chan num {} of note {}!".format(byte[1],switch))
            return ptr, False

    elif byte[0]=="b":
        # * MIDI Control Table 
        # ** http://www33146ue.sakura.ne.jp/staff/iz/formats/midi-cntl.html
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            byte = get_bytes(ptr+1)
            mode_num = hex2dec(byte)
            # print("Chan {} control mode change to 0x{}".format(chan_num,get_bytes(ptr+1,ptr+3)))
            # ignore control commands (3 bytes)
            ptr+=3
            return ptr, (chan_num, mode_num)
        else:
            print("x Invalid chan num {} of control!".format(byte[1]))
            return ptr, False

    elif byte[0]=="c":
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            inst_num = hex2dec(get_bytes(ptr+1))
            print("Chan {} program change to instrument {}".format(chan_num,inst_num))
            ptr+=2
            chan_inst_L.append([chan_num,inst_num])
            return ptr,(chan_num,inst_num)
        else:
            print("x Invalid chan num to change instrument!")
            return ptr, False
    else:
        print("x Unknown bytes {} at ptr {}!".format(byte,ptr))
        return ptr, False

active_note_L = []
played_note_L = []

def insert_note(abs_t,res):
    # played_note: start (tick), dura (tick), chan_num, pit_dec, velocity
    global active_note_L, played_note_L
    chan_num, pit_dec, velocity = res[1:4]
    if res[0] == "ON":
    # on_note: start (tick), chan_num, pit_dec, velocity
        active_note_L.append([abs_t,chan_num, pit_dec, velocity])
    elif res[0] == "OFF":
    # off_note: end (tick), chan_num, pit_dec, velocity
        for idx,note in enumerate(active_note_L):
            if pit_dec == note[2]:
                dura = abs_t - note[0]
                active_note_L[idx].insert(1,dura)
                played_note_L.append(active_note_L.pop(idx))
                break

def parse_mthd():
    global TPQN
    ptr = 0
    if get_bytes(ptr,ptr+4) == "4d546864":
        print("=== MThd ===")
    else:
        print("x Cannot parse MThd!")
        return ptr, False

    ptr+=4
    mthd_chk_len = hex2dec(get_bytes(ptr,ptr+4))
    print("MThd chunk length: {} (bytes)".format(mthd_chk_len))

    ptr+=4
    trk_fmt = hex2dec(get_bytes(ptr,ptr+2))
    print("Track Format: {}".format(trk_fmt))

    ptr+=2
    trk_num = hex2dec(get_bytes(ptr,ptr+2))
    print("Track Number: {}".format(trk_num))

    ptr+=2
    TPQN = hex2dec(get_bytes(ptr,ptr+2))
    print("TPQN: {} (ticks per quarter-note)".format(TPQN))

    ptr+=2
    return ptr, True

def parse_mtrk(ptr):
    ptr, res = parse_event(ptr)
    abs_t = 0
    while res != False:
        ptr, dt = parse_delta_time(ptr)
        abs_t += dt
        ptr, res = parse_event(ptr)

        if res == "EOT":
            if get_bytes(ptr) == "":
                print("\n>>> End of file <<<\n")
                return ptr, "EOF"
            else:
                return ptr, "EOT"
        elif type(res)==tuple:
            if res[0] in ["ON","OFF"]:
                insert_note(abs_t,res)
        else:
            pass

def process_midi(filename):
    global bytes_L, played_note_L
    # with open("abc.mid","rb") as rf:
    with open(filename,"rb") as rf:
        # Note: py2:ord(b) || py3:b
        bytes_L = ["{:02x}".format(ord(b)) for b in rf.read()]

    ptr, res = parse_mthd()
    while res != "EOF":
        ptr,res = parse_mtrk(ptr)
    played_note_L = sorted(played_note_L,key=lambda l:l[0])
    # for played_note in played_note_L:
    #     print(played_note)
    print(TPQN, USPQN, NUME, DENO, chan_inst_L)

if __name__ == '__main__':
    # process_midi("abc.mid")
    process_midi("secret1.mid")

