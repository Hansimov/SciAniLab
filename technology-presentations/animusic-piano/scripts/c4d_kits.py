from __future__ import division, print_function
import c4d
import re
from math import pi, sin, cos, sqrt, floor, ceil
# c4d.CallCommand(13957) # Clear Console

# Must add the line below when importing this module, otherwise:
#   "NameError: Global Name `doc` is not defined"
doc = c4d.documents.GetActiveDocument()

start_undo = doc.StartUndo
end_undo   = doc.EndUndo
add_undo   = doc.AddUndo
event_add = c4d.EventAdd

def clear_console():
    c4d.CallCommand(13957) # Clear Console

def return_true(obj):
    return True

def get_bros(obj, next_only=False, with_obj=True, condition=return_true):
    bro_list = []

    # next brothers
    bro = obj.GetNext()
    while bro != None:
        if condition(bro):
            bro_list.append(bro)
        bro = bro.GetNext()

    # append obj itself
    if with_obj:
        if condition(obj):
            bro_list.append(obj)

    # previous brothers
    if next_only == False:
        bro = obj.GetPred()
        while bro != None:
            if condition(bro):
                bro_list.append(bro)
            bro = bro.GetPred()

    return bro_list

def find_obj_in_root(name, root="", case_insensitive=[True,True], use_regex=[True,True]):
    # doc = c4d.documents.GetActiveDocument()
    first_obj = doc.GetFirstObject()
    if first_obj == None:
        return []

    stack, obj_list = [], []

    # Get first level parents
    if type(root) == str:
    # root is name of object
        if root == "":
        # root is world, get all level 1 objects as parents
            stack.extend(get_bros(first_obj))
        else:
        # root is name of level 1 object(s)
            def is_name_equal_root(ele):
                root_name, ele_name = root, ele.GetName()
                if case_insensitive[1]:
                    ele_name, root_name = ele_name.lower(), root_name.lower()
                if use_regex[1]:
                    if re.match(root_name+"\Z", ele_name):
                        return True
                else:
                    if root_name == ele_name:
                        return True
                return False

            stack.extend(get_bros(first_obj, condition=is_name_equal_root))
    else:
    # root is a specified object
        stack.extend([root])

    # Depth First Search
    while stack != []:
        obj = stack.pop()
        obj_name = obj.GetName()
        if case_insensitive[0]:
            name, obj_name = name.lower(), obj_name.lower()
        # print(obj.GetName())
        if use_regex[0]:
            if re.match(name+"\Z", obj_name):
                obj_list.append(obj)
        else:
            if name == obj_name:
                obj_list.append(obj)

        for child in obj.GetChildren()[::-1]:
            stack.append(child)

    return obj_list

def rad2deg(rad):
    return rad/pi*180
def deg2rad(deg):
    return deg/180*pi

def rot_vec_in_deg(h,p,b):
    # h,p,b are in degrees
    return c4d.Vector(deg2rad(h),deg2rad(p),deg2rad(b))

# def get_abs_rot(obj):
#     abs_rot = obj.GetAbsRot()
#     h,p,b = abs_rot[0], abs_rot[1], abs_rot[2]
#     # vector is in degrees
#     

def get_arf_psr(arf,psr,obj):
    # return c4d.Vector(x,y,z)

    arf, psr = arf.lower(), psr.lower()
    # arf: abs, rel, frozen
    # psr: pos, scale, rot

    if psr == "pos":
        if arf == "abs":
            xyz = obj.GetAbsPos()
        elif arf == "rel":
            xyz = obj.GetRelPos()
        else: # arf == "frozen"
            xyz = obj.GetFrozenPos()
        x,y,z = xyz[0],xyz[1],xyz[2]
        return c4d.Vector(x,y,z)

    elif psr == "rot":
        if arf == "abs":
            hpb = obj.GetAbsRot()
        elif arf == "rel":
            hpb = obj.GetRelRot()
        else: # arf == "frozen"
            hpb = obj.GetFrozenRot()
        h,p,b = hpb[0], hpb[1], hpb[2]
        return c4d.Vector(*list(map(rad2deg,[h,p,b])))

    else: # psr == "scale"
        if arf == "abs":
            xyz = obj.GetAbsScale()
        elif arf == "rel":
            xyz = obj.GetRelScale()
        else: # arf == "frozen"
            xyz = obj.GetFrozenScale()
        x,y,z = xyz[0],xyz[1],xyz[2]
        return c4d.Vector(x,y,z)

def set_arf_psr(arf,psr,obj,xyz):
    arf, psr = arf.lower(), psr.lower()
    # xyz can be list, tuple, c4d.Vector, ...
    # arf: abs, rel, frozen
    # psr: pos, scale, rot
    x,y,z = xyz[0],xyz[1],xyz[2]
    c4d_vec_xyz = c4d.Vector(x,y,z)

    if psr == "pos":
        if arf == "abs":
            obj.SetAbsPos(c4d_vec_xyz)
        elif arf == "rel":
            obj.SetRelPos(c4d_vec_xyz)
        else: # arf == "frozen"
            obj.SetFrozenPos(c4d_vec_xyz)

    elif psr == "rot":
        hpb_in_rad = list(map(deg2rad,[x,y,z]))
        if arf == "abs":
            obj.SetAbsRot(c4d.Vector(*hpb_in_rad))
        elif arf == "rel":
            obj.SetRelRot(c4d.Vector(*hpb_in_rad))
        else: # arf == "frozen"
            obj.SetFrozenRot(c4d.Vector(*hpb_in_rad))

    else: # psr == "scale"
        if arf == "abs":
            obj.SetAbsScale(c4d_vec_xyz)
        elif arf == "rel":
            obj.SetRelScale(c4d_vec_xyz)
        else: # arf == "frozen"
            obj.SetFrozenScale(c4d_vec_xyz)


ARF = ["abs","rel","frozen"]
PSR = ["pos","rot","scale"]

def_set_arf_psr = "def set_{0}_{1}(obj,xyz): set_arf_psr(\"{0}\",\"{1}\",obj,xyz)"
def_get_arf_psr = "def get_{0}_{1}(obj): return get_arf_psr(\"{0}\",\"{1}\",obj)"

def get_world_pos(obj):
    return obj.GetMg().off

# Be careful to use this!
def set_world_pos(obj,xyz):
    mg = obj.GetMg()
    v1,v2,v3 = mg.v1,mg.v2,mg.v3
    off_new = c4d.Vector(xyz[0],xyz[1],xyz[2])
    c4d_mat_mg = c4d.Matrix(off_new,v1,v2,v3)
    obj.SetMg(c4d_mat_mg)

for arf in ARF:
    for psr in PSR:
        exec(def_set_arf_psr.format(arf,psr))
        exec(def_get_arf_psr.format(arf,psr))
