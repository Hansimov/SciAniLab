# * MIDI文件格式解析 | 码农家园 
# ** https://www.codenong.com/js59d74800b43b/

# * 读书笔记——MIDI文件结构简介 - 哔哩哔哩 
# ** https://www.bilibili.com/read/cv1753143/

# * MIDI文件格式分析──理论篇 - Midifan：我们关注电脑音乐 
# ** https://m.midifan.com/article_body.php?id=901

# * Standard MIDI file format, updated 
# ** http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA2_

with open("abc.mid","rb") as rf:
    bytes_L = ["{:02x}".format(b) for b in rf.read()]

hexchr = "0123456789abcdef"
# ptr = 0

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

def get_delta_time(ptr):
    """ return (int, int) : (pointer offset, num of tick) """
    # * Variable Length Values 
    # ** http://www.ccarh.org/courses/253/handout/vlv/    hex_str = get_bytes(ptr)
    bin_str = "{:08b}".format(hex2dec(hex_str))
    if bin_str[0]=="0":
        return bin2dec(bin_str[1:]), ptr+1

    bin_str = bin_str[1:]
    ptr += 1
    tmp_str = get_bytes(ptr)
    while tmp_str[0]!="0":
        bin_str+=tmp_str[1:]
        ptr+=1
    bin_str+=tmp_str[1:]
    ptr+=1
    return ptr, bin2dec(bin_str)

def get_event(ptr):
    """ return event string """

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
            print("Track name: {trk_name}")
            ptr+=txt_len
            return ptr, True
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
            dd = hex2dec(2**get_bytes(ptr+1))
            cc = hex2dec(get_bytes(ptr+2))
            bb = hex2dec(get_bytes(ptr+3))
            print(f"nn:{nn}, dd:{dd}, cc:{cc}, bb:{bb}")
            ptr+=4
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
            print(f"sf:{sf},mi:{mi}")
            ptr+=2
            return ptr, (sf,mi)
        elif byte=="51":
        # Set Tempo: FF 51 03 tttttt
        # (ms per MIDI quarter-note)
            if get_bytes(ptr+1) != "03":
                print("x Invalid set tempo byte length!")
                return ptr, False
            ptr+=2
            tttttt = hex2dec(get_bytes(ptr,ptr+3))
            print(f"tttttt: {tttttt}")
            ptr+=3
            return ptr, tttttt
        elif byte=="2f":
            if get_bytes(ptr+1) != "00":
                print("x Invalid end notation!")
                return ptr, False
            print("=== End of track ===")
            ptr+=2
            return ptr, True
        else:
            print(f"x Unknown bytes of Meta-Event after {byte}!")
            return ptr, False
    elif byte=="4d":
        if get_bytes(ptr+1)=="54":
            ptr+=2
            if get_bytes(ptr,ptr+2)=="6864":
                print("=== MThd ===")
                # to add chunk length
                # return ptr+2
            elif get_bytes(ptr,ptr+2)=="726b":
                print("\n=== MTrk ===")
                ptr+=2
                mtrk_chunk_len = hex2dec(get_bytes(ptr,ptr+4))
                print(f"MTrk chunk length: {mtrk_chunk_len}")
                ptr+=4
                return ptr,mtrk_chunk_len
            else:
                print(f"x Unknown bytes after {byte}!")
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
            note_num = hex2dec(get_bytes(ptr+1))
            note_vel = hex2dec(get_bytes(ptr+2))
            print(f"Chan {chan_num} note {note_num} {switch}, velocity: {note_vel}"})
            ptr+=3
            return ptr, switch
        else:
            print("x Invalid chan num of note {switch}!")
            return ptr, False
    elif byte[0]=="b":
        # * MIDI Control Table 
        # ** http://www33146ue.sakura.ne.jp/staff/iz/formats/midi-cntl.html
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            byte = get_bytes(ptr+1)
            # if hex2dec(byte) >= hex2dec("62") and hex2dec(byte) <= hex2dec("79"):
            #     ctrl_str = "undefined"
            #     ptr+=2
            # else:
            #     ctrl_str = "<UNDEFINED>"
            print(f"Chan {chan_num+1} control mode change to {hex2dec(byte)}")
            ptr+=3
            return ptr, True
        else:
            print("x Invalid chan num of control!")
            return ptr, False
    elif byte[0]=="c":
        if byte[1] in hexchr:
            chan_num = hexchr.index(byte[1])
            inst_num = hex2dec(get_bytes(ptr+1))
            print(f"Channel {chan_num+1} program change to instrument {inst_num}")
            ptr+=2
            return ptr,inst_num
        else:
            print("x Invalid chan num to change instrument!")
            return ptr, False
    else:
        print(f"x Unknown bytes after {byte}")
        return ptr, False


def parse_midi():
    if get_bytes(0,4) == "4d546864":
        print("MThd ...")
    else:
        print("x Cannot parse MThd!")
        return 

    MTHD_CHK_LEN = hex2dec(get_bytes(4,8))
    print(f"MThd Chunk Length: {MTHD_CHK_LEN} (bytes)")

    TRK_FMT = hex2dec(get_bytes(8,10))
    print(f"Track Format: {TRK_FMT}")

    TRK_NUM = hex2dec(get_bytes(10,12))
    print(f"Track Number: {TRK_NUM}")

    TPQN = hex2dec(get_bytes(12,14))
    print(f"Ticks Per Quarter-Note: {TPQN}")

    if get_bytes(14,18) == "4d54726b":
        print("\nMTrk ...")
    else:
        print("x Cannot parse MTrk")
        return 

    MTRK_CHK_LEN = hex2dec(get_bytes(18,22))
    print(f"MTrk Chunk Length: {MTRK_CHK_LEN}")

    ptr = 22
    ptr,dt = get_delta_time(ptr)

    print(dt)

if __name__ == '__main__':
    parse_midi()