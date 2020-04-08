# encoding: utf-8
from __future__ import division, print_function
import c4d
import re
from math import pi,sin,cos,asin,acos,sqrt,floor,ceil
from operator import add,sub,mul,div

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

def activate_none():
    doc.SetActiveObject(None,c4d.SELECTION_NEW)

def activate(obj,mode=c4d.SELECTION_NEW):
    doc.SetActiveObject(obj,mode)

def return_true(obj):
    return True

def sign(num):
    return int(num>0)-int(num<0)

def sum_abs(num_L):
    return sum(list(map(abs,num_L)))

def max_abs(num_L,weights=[]):
    return max(list(map(abs,num_L)))

def sort_abs(num_L,weights=[]):
    abs_num_L = list(map(abs,num_L))
    return sorted(abs_num_L,reverse=True)

def cmp_angle_delta_L(L1,L2):
    L1 = [L1[0],sum(L1[1:])]
    L2 = [L2[0],sum(L2[1:])]
    for i,j in zip(L1,L2):
        if i>j:
            return 1
        elif i==j:
            continue
        else:
            return -1
    return 0

def frm2bt(frm):
    return c4d.BaseTime(frm,doc.GetFps())

def get_fps():
    return doc.GetFps()

def get_current_frm():
    return doc.GetTime().GetFrame(doc.GetFps())

def get_bros(obj, next_only=False, with_obj=True, condition=return_true):
    """ c4d.BaseObject list """
    bro_L = []

    # next brothers
    bro = obj.GetNext()
    while bro != None:
        if condition(bro):
            bro_L.append(bro)
        bro = bro.GetNext()

    # append obj itself
    if with_obj:
        if condition(obj):
            bro_L.append(obj)

    # previous brothers
    if next_only == False:
        bro = obj.GetPred()
        while bro != None:
            if condition(bro):
                bro_L.append(bro)
            bro = bro.GetPred()

    return bro_L

def find_obj(name, root="", case_insensitive=[True,True], use_regex=[True,True]):
    """ c4d.BaseObject list """
    # doc = c4d.documents.GetActiveDocument()
    first_obj = doc.GetFirstObject()
    if first_obj == None:
        return []

    stack, obj_L = [], []

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
                obj_L.append(obj)
        else:
            if name == obj_name:
                obj_L.append(obj)

        for child in obj.GetChildren()[::-1]:
            stack.append(child)

    return obj_L

def rad2deg(rad):
    return rad/pi*180
def deg2rad(deg):
    return deg/180*pi

def rot_vec_in_deg(h,p,b):
    # h,p,b are in degrees
    return c4d.Vector(deg2rad(h),deg2rad(p),deg2rad(b))


def rot_to_vec(rot):
    rot = deg2rad(rot)
    vec = c4d.Vector(cos(rot),0,sin(rot))
    return vec

def is_rot_reachable(rot1_old,rot2,rot1_new):
    vec1_old,vec2,vec1_new = list(map(rot_to_vec,[rot1_old,rot2,rot1_new]))
    return is_vec_reachable(vec1_old,vec2,vec1_new)

def is_vec_reachable(vec1_old,vec2,vec1_new):
    if (vec1_new.Cross(-vec1_old)).Dot(vec1_new.Cross(vec2)) <=0 \
        and vec1_new.Dot(vec2-vec1_old) >= 0:
        return False
    else:
        # Note: if vec1_new == -vec1_old,
        #       rotation direction should be chosen carefully!
        return True

def get_arf_psr(arf,psr,obj,dim=-1):
    # return c4d.Vector(x,y,z) or float

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

        if dim == -1:
            return c4d.Vector(x,y,z)
        else:
            return xyz[dim]

    elif psr == "rot":
        if arf == "abs":
            hpb = obj.GetAbsRot()
        elif arf == "rel":
            hpb = obj.GetRelRot()
        else: # arf == "frozen"
            hpb = obj.GetFrozenRot()
        h,p,b = hpb[0], hpb[1], hpb[2]

        if dim == -1:
            return c4d.Vector(*list(map(rad2deg,[h,p,b])))
        else:
            return rad2deg(hpb[dim])

    else: # psr == "scale"
        if arf == "abs":
            xyz = obj.GetAbsScale()
        elif arf == "rel":
            xyz = obj.GetRelScale()
        else: # arf == "frozen"
            xyz = obj.GetFrozenScale()
        x,y,z = xyz[0],xyz[1],xyz[2]

        if dim == -1:
            return c4d.Vector(x,y,z)
        else:
            return xyz[dim]

def set_arf_psr(arf,psr,obj,xyz,dim=-1):
    arf, psr = arf.lower(), psr.lower()
    # xyz can be list, tuple, c4d.Vector, float, ...
    # arf: abs, rel, frozen
    # psr: pos, scale, rot

    old_xyz = get_arf_psr(arf,psr,obj)

    if dim==-1:
        new_xyz = [None,None,None]
        for i in range(3):
            new_xyz[i] = xyz[i] if xyz[i]!=None else old_xyz[i]
        c4d_vec_xyz = c4d.Vector(*new_xyz)
    else:
        c4d_vec_xyz = old_xyz
        if xyz != None:
            c4d_vec_xyz[dim] = xyz

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

# ARF = ["abs","rel","frozen"]
# PSR = ["pos","rot","scale"]

# def_set_arf_psr = "def set_{0}_{1}(obj,xyz): set_arf_psr(\"{0}\",\"{1}\",obj,xyz)"
# def_get_arf_psr = "def get_{0}_{1}(obj): return get_arf_psr(\"{0}\",\"{1}\",obj)"

# for arf in ARF:
#     for psr in PSR:
#         exec(def_set_arf_psr.format(arf,psr))
#         exec(def_get_arf_psr.format(arf,psr))

# I use these tedious definitions just to activate auto completions of Sublime
def get_abs_pos(obj,dim=-1):       return get_arf_psr("abs","pos",obj,dim)
def get_abs_rot(obj,dim=-1):       return get_arf_psr("abs","rot",obj,dim)
def get_abs_scale(obj,dim=-1):     return get_arf_psr("abs","scale",obj,dim)
def get_rel_pos(obj,dim=-1):       return get_arf_psr("rel","pos",obj,dim)
def get_rel_rot(obj,dim=-1):       return get_arf_psr("rel","rot",obj,dim)
def get_rel_scale(obj,dim=-1):     return get_arf_psr("rel","scale",obj,dim)
def get_frozen_pos(obj,dim=-1):    return get_arf_psr("frozen","pos",obj,dim)
def get_frozen_rot(obj,dim=-1):    return get_arf_psr("frozen","rot",obj,dim)
def get_frozen_scale(obj,dim=-1):  return get_arf_psr("frozen","scale",obj,dim)

def set_abs_pos(obj,xyz,dim=-1):       set_arf_psr("abs","pos",obj,xyz,dim)
def set_abs_rot(obj,xyz,dim=-1):       set_arf_psr("abs","rot",obj,xyz,dim)
def set_abs_scale(obj,xyz,dim=-1):     set_arf_psr("abs","scale",obj,xyz,dim)
def set_rel_pos(obj,xyz,dim=-1):       set_arf_psr("rel","pos",obj,xyz,dim)
def set_rel_rot(obj,xyz,dim=-1):       set_arf_psr("rel","rot",obj,xyz,dim)
def set_rel_scale(obj,xyz,dim=-1):     set_arf_psr("rel","scale",obj,xyz,dim)
def set_frozen_pos(obj,xyz,dim=-1):    set_arf_psr("frozen","pos",obj,xyz,dim)
def set_frozen_rot(obj,xyz,dim=-1):    set_arf_psr("frozen","rot",obj,xyz,dim)
def set_frozen_scale(obj,xyz,dim=-1):  set_arf_psr("frozen","scale",obj,xyz,dim)

def get_world_pos(obj):
    return obj.GetMg().off

# Be careful to use this!
def set_world_pos(obj,xyz):
    mg = obj.GetMg()
    v1,v2,v3 = mg.v1,mg.v2,mg.v3
    off_new = c4d.Vector(xyz[0],xyz[1],xyz[2])
    c4d_mat_mg = c4d.Matrix(off_new,v1,v2,v3)
    obj.SetMg(c4d_mat_mg)


def get_x_axis_vec(obj): return obj.GetMg().v1
def get_y_axis_vec(obj): return obj.GetMg().v2
def get_z_axis_vec(obj): return obj.GetMg().v3

def p_to_p_dist(p1,p2):
    return (p1-p2).GetLength()

def p_to_v_dist(p,q,v):
    # p: point (c4d.Vector)
    # q: point on vector (c4d.Vector)
    # v: vector (c4d.Vector)
    # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Vector_formulation
    return ((q-p)-((q-p)*v)*v).GetLength()

def p_to_v_foot(p,q,v):
    # similar to p_to_v_dist()
    return q + ((p-q)*v)*v

def v_angle(v1,v2,normal=None):
    # https://stackoverflow.com/questions/5188561/signed-angle-between-two-3d-vectors-with-same-origin-within-the-same-plane
    # NOTE: Left-handed coordinate sytem! (Cross is influenced!)
    # v1->v2 anticlockwise is positive
    sign = 1
    if normal != None:
        if v1.Cross(v2).Dot(normal) > 0:
            sign = -1

    return sign*acos(v1*v2/(v1.GetLength()*v2.GetLength()))/pi*180

def p_angle(p1,p2,p3):
    return v_angle(p2-p1,p2-p3)

def is_points_collinear(p1,p2,p3,threshold=1):
    abs_angle = abs(p_angle(p1,p2,p3))
    # print(abs_angle)
    if abs_angle <= threshold or abs_angle>=180-threshold :
        # print("collinear!!")
        return True
    else:
        return False

def v_plane_normal(v1,v2):
    """ c4d.Vector """
    return v1.Cross(v2).GetNormalized()

def p_plane_normal(p1,p2,p3,p4=None):
    """ c4d.Vector list
    > p4: c4d.Vector - Reserved point to deal with p1,p2,p3 collinear
    """
    ref = p3
    if is_points_collinear(p1,p2,p3):
        ref = p4
        print("Warning: Collinear points detected!")
    return v_plane_normal(p2-p1,p2-ref)

def rotate_vec(v,axis,angle):
    # https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    # angle: anticlockwise is positive
    # NOTE: C4D uses left-handed coordinate system,
    #       while Rodrigues rotation formula here uses right-hand,
    #       so we should change the sign of the angle
    ta = -deg2rad(angle)
    k = axis.GetNormalized()

    return v*cos(ta) + k.Cross(v)*sin(ta)+k*(k.Dot(v))*(1-cos(ta))

def two_circle_intersection(p1,r1,p2,r2,p3,p4=None):
    """ c4d.Vector list (len:0-2) 
    > p3: c4d.Vector - reference point to determine plane normal
    > p4: c4d.Vector - Reserved reference point avoid p1,p2,p3 collinear
    """
    # p1,p2: center of circle 
    # r1,r2: radius of circle
    # q: intersection(s)
    # return list of q (c4d.Vector)

    # https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
    # https://en.wikipedia.org/wiki/Heron%27s_formula
    # https://en.wikipedia.org/wiki/Cross_product
    p1p2_len = (p1-p2).GetLength()
    if p1p2_len > r1+r2:
        return []
    if p1p2_len < abs(r2-r1):
        return []
    if p1p2_len == r1+r2:
        return [p1+(p2-p1)*r1/p1p2_len]

    a,b,c = r1,r2,p1p2_len
    s = (a+b+c)/2
    area = sqrt(s*(s-a)*(s-b)*(s-c))
    height = 2*area/c
    leg = sqrt(pow(r1,2)-pow(height,2))
    foot = p1 + (p2-p1)*(leg/c)

    plane_normal_vec = p_plane_normal(p1,p2,p3,p4)

    # Q: What if ref,p1,p2 are collinear?
    # A1: Drop the result of next status of arm which makes them collinear.
        # Q: What if only one solution of intersection?
        # A: ...
    # A2: [Y] Or add one more ref to reduce the chances of this condition.
        # Q: What if the other ref also collinear?
        # A: ...
    # Do not worry about too many tiny things ... 

    p1p2_perp_vec = (p2-p1).Cross(plane_normal_vec).GetNormalized()

    intsect_L = []
    intsect_L.append(foot + p1p2_perp_vec * height)
    intsect_L.append(foot - p1p2_perp_vec * height)

    return intsect_L

def center_axis_to_anchor(end,center_L,axis_L):
    """ c4d.Vector list """
    anchor_L = []
    for center, axis in zip(center_L, axis_L):
        anchor_L.append(p_to_v_foot(end, center, axis))
    anchor_L.append(end)
    return anchor_L

def anchor_to_vec(base_vec,anchor_L):
    """ c4d.Vector list """
    vec_L = []
    vec_L.append(base_vec)
    for i in range(len(anchor_L)-1):
        vec_L.append(anchor_L[i+1]-anchor_L[i])
    return vec_L

def vec_to_len(vec_L):
    """ float list """
    len_L = []
    for vec in vec_L[1:]:
        len_L.append(vec.GetLength())
    return len_L

def vec_to_angle(vec_L,normal):
    """ float list """
    angle_L = []
    for i in range(len(vec_L)-1):
        angle_L.append(v_angle(-vec_L[i],vec_L[i+1],normal))
    return angle_L

def angle_delta(old_angle_L,new_angle_L):
    """ float list """
    return list(map(sub, new_angle_L, old_angle_L))


# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/misc/descriptions.html
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/Description/index.html#c4d-description
# https://developers.maxon.net/docs/Cinema4DCPPSDK/html/page_manual_descid.html#page_manual_descid_desclevel
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/DescLevel/index.html#c4d-desclevel
def get_arf_psr_desc_id(arf,psr,dim=-1):
    # Drag and drop element directly to python console to get DescID expression
    arf_L = ["abs","rel","frozen"]
    arf_str_L = ["ABS","REL","FROZEN"]
    psr_L = ["pos","rot","scale"]
    psr_str_L = ["POSITION","ROTATION","SCALE"]

    arf_str = arf_str_L[arf_L.index(arf.lower())]
    psr_str = psr_str_L[psr_L.index(psr.lower())]

    desc_level_1_1 = eval("_".join(["c4d.ID_BASEOBJECT",arf_str,psr_str]))
    desc_level_1 = c4d.DescLevel(desc_level_1_1,c4d.DTYPE_VECTOR,0)

    xyz_str = ["X","Y","Z"]
    if dim == -1:
        desc_id = c4d.DescID(desc_level_1)
    else:
        desc_level_2_1 = eval(("c4d.VECTOR_"+xyz_str[dim]))
        desc_level_2 = c4d.DescLevel(desc_level_2_1,c4d.DTYPE_REAL,0)
        desc_id = c4d.DescID(desc_level_1,desc_level_2)

    return desc_id

def get_abs_pos_desc_id(dim=-1):        return get_arf_psr_desc_id("abs","pos",dim)
def get_abs_rot_desc_id(dim=-1):        return get_arf_psr_desc_id("abs","rot",dim)
def get_abs_scale_desc_id(dim=-1):      return get_arf_psr_desc_id("abs","scale",dim)
def get_rel_pos_desc_id(dim=-1):        return get_arf_psr_desc_id("rel","pos",dim)
def get_rel_rot_desc_id(dim=-1):        return get_arf_psr_desc_id("rel","rot",dim)
def get_rel_scale_desc_id(dim=-1):      return get_arf_psr_desc_id("rel","scale",dim)
def get_frozen_pos_desc_id(dim=-1):     return get_arf_psr_desc_id("frozen","pos",dim)
def get_frozen_rot_desc_id(dim=-1):     return get_arf_psr_desc_id("frozen","rot",dim)
def get_frozen_scale_desc_id(dim=-1):   return get_arf_psr_desc_id("frozen","scale",dim)

# https://www.cineversity.com/wiki/Python%3A_DescIDs_and_Animation/
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/GeListNode/BaseList2D/CTrack/index.html?highlight=ctrack#c4d-ctrack
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/GeListNode/BaseList2D/CCurve/index.html?highlight=ctrack#c4d-ccurve
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/CKey/index.html?highlight=ctrack#c4d-ckey
# https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/BaseTime/index.html#c4d-basetime

def get_key_with_id(obj,desc_id,frm=None):
    trk = obj.FindCTrack(desc_id)

    if trk == None:
        return -2
    else:
        crv = trk.GetCurve()
        if frm==None:
            frm = get_current_frm()
        key = crv.FindKey(frm2bt(frm))
        if key != None:
            return key["key"]
        else:
            return -1

def get_arf_psr_key(arf,psr,obj,frm=None,dim=-1):
    if frm == None:
        frm = get_current_frm()

    if dim == -1:
        desc_id_L = [get_arf_psr_desc_id(arf,psr,i) for i in range(3)]
        key_L = []
        for desc_id in desc_id_L:
            key_L.append(get_key_with_id(obj,desc_id,frm))
        return key_L
    else: # dim != 1
        desc_id = get_arf_psr_desc_id(arf,psr,dim)
        return get_key_with_id(obj,desc_id,frm)

def set_key_with_id(obj,desc_id,val=None,frm=None):
    if frm == None:
        frm = get_current_frm()
    if val == None:
        val = obj[desc_id]
        # if type(val) != float:
        #     raise ValueError("val must be float!")
    if type(val)==c4d.Vector or type(obj[desc_id])==c4d.Vector:
        # c4d.VECTOR_X (1000) ~ c4d.VECTOR_Z (1002)
        for dim in range(3):
            desc_id_dim = (desc_id,1000+dim)
            set_key_with_id(obj,desc_id_dim,val[dim],frm)
        return
    else:
        pass
    key = get_key_with_id(obj,desc_id,frm)
    if type(key) == int:
        if key == -2:
            trk = c4d.CTrack(obj,desc_id)
            obj.InsertTrackSorted(trk)
        else:
            trk = obj.FindCTrack(desc_id)
        crv = trk.GetCurve()
        key = c4d.CKey()
        key.SetTime(crv,frm2bt(frm))
        crv.InsertKey(key)
    else:
        crv = key.GetCurve()
    key=crv.FindKey(frm2bt(frm))["key"]
    idx=crv.FindKey(frm2bt(frm))["idx"]
    key.SetValue(crv,val)
    # http://www.plugincafe.com/forum/forum_posts.asp?TID=14107&PID=56307#56307
    # https://plugincafe.maxon.net/topic/11698/beginner-how-can-i-set-a-key-frame-and-value-to-a-cube-by-python/3
    key.SetInterpolation(crv,c4d.CINTERPOLATION_SPLINE)
    # kidx = crv.FindKey(frm2bt(frm))["idx"]
    crv.SetKeyDefault(doc,idx)
    # key.SetAutomaticTangentMode(crv,c4d.CAUTOMODE_CLASSIC)
    # key.SetTimeLeft(crv,frm2bt(0))

def set_arf_psr_key(arf,psr,obj,val,frm=None,dim=-1):
    if frm == None:
        frm = get_current_frm()

    if dim == -1:
        desc_id_L = [get_arf_psr_desc_id(arf,psr,i) for i in range(3)]
        for i,desc_id in enumerate(desc_id_L):
            if psr == "rot":
                val[i] = deg2rad(val[i])
            set_key_with_id(obj,desc_id,val[i],frm)
    else:
        desc_id = get_arf_psr_desc_id(arf,psr,dim)
        if psr == "rot":
            val = deg2rad(val)
        set_key_with_id(obj,desc_id,val,frm)

def set_abs_pos_key(obj,val,frm=None,dim=-1):       set_arf_psr_key("abs","pos",obj,val,frm,dim)
def set_abs_rot_key(obj,val,frm=None,dim=-1):       set_arf_psr_key("abs","rot",obj,val,frm,dim)
def set_abs_scale_key(obj,val,frm=None,dim=-1):     set_arf_psr_key("abs","scale",obj,val,frm,dim)
def set_rel_pos_key(obj,val,frm=None,dim=-1):       set_arf_psr_key("rel","pos",obj,val,frm,dim)
def set_rel_rot_key(obj,val,frm=None,dim=-1):       set_arf_psr_key("rel","rot",obj,val,frm,dim)
def set_rel_scale_key(obj,val,frm=None,dim=-1):     set_arf_psr_key("rel","scale",obj,val,frm,dim)
def set_frozen_pos_key(obj,val,frm=None,dim=-1):    set_arf_psr_key("frozen","pos",obj,val,frm,dim)
def set_frozen_rot_key(obj,val,frm=None,dim=-1):    set_arf_psr_key("frozen","rot",obj,val,frm,dim)
def set_frozen_scale_key(obj,val,frm=None,dim=-1):  set_arf_psr_key("frozen","scale",obj,val,frm,dim)

# Only works on current 3-h-rot arm, need to be extended
class Arm:
    def __init__(self,joint_L=[],end=None):
        # joint: rotation object (c4d.BaseObject)
        self.joint_L = joint_L
        # end: arm end (c4d.Vector)
        self.end = end
        self.init_constants()

    def init_constants(self):
        self.old_axis_L  = []
        self.old_center_L = []
        self.old_rot_L = []
        for joint in self.joint_L:
            self.old_rot_L.append(get_rel_rot(joint)[0])
            self.old_axis_L.append(get_y_axis_vec(joint))
            self.old_center_L.append(get_world_pos(joint))

        self.old_anchor_L = center_axis_to_anchor(self.end,self.old_center_L,self.old_axis_L)

        self.start = self.old_anchor_L[0]
        # h_vec might be replaced with v_rot axis
        self.h_vec = c4d.Vector(0,1,0)
        self.old_vec_L = anchor_to_vec(self.h_vec,self.old_anchor_L)
        self.len_L = vec_to_len(self.old_vec_L)

        self.plane_normal = self.old_axis_L[0].GetNormalized()

        self.old_angle_L = vec_to_angle(self.old_vec_L,self.plane_normal)


    def is_target_reachable(self,target):
        # target: target position (c4d.Vector)
        total_len = sum(self.len_L)
        start_to_target_dist = p_to_p_dist(self.start,target)
        if start_to_target_dist > total_len:
            return False
        if start_to_target_dist < self.len_L[0]-(total_len-self.len_L[0]):
            return False
        return True

    # new_pos -> new_abs_rot -> delta_angle
    # return new_rot_L

    def get_best_joint_rot(self,target):
        if not self.is_target_reachable(target):
            print("Warning: Cannot reach target!")
            return None
        intsect_L = two_circle_intersection(self.start,self.len_L[0], target, self.len_L[-1]+self.len_L[-2],self.old_anchor_L[1],self.old_anchor_L[2])
        # print(intsect_L)

        if len(intsect_L) == 1:
            pass
            # todo

        joint_1_start_pos = intsect_L[0]
        joint_1_end_pos = intsect_L[1]

        joint_1_total_spin_delta = v_angle(joint_1_start_pos-self.start,joint_1_end_pos-self.start,normal=self.old_axis_L[0])
        # print(joint_1_total_spin_delta)

        spin_deg_safe_margin = 0.5
        if abs(joint_1_total_spin_delta) < spin_deg_safe_margin*2:
            pass
            # todo
        else:
            joint_1_total_spin_delta -= sign(joint_1_total_spin_delta)*spin_deg_safe_margin*2

        joint_1_start_vec = rotate_vec(joint_1_start_pos-self.start, self.old_axis_L[0], spin_deg_safe_margin)

        subdiv_num = 10
        joint_1_spin_step = joint_1_total_spin_delta/subdiv_num
        joint_1_pos_L = []
        joint_pos_LL = []
        for i in range(subdiv_num+1):
            joint_1_tmp_pos = self.start+rotate_vec(joint_1_start_vec,self.old_axis_L[0],i*joint_1_spin_step)
            # joint_1_tmp_pos_L.append(joint_1_tmp_pos)
            joint_2_tmp_pos_L = two_circle_intersection(joint_1_tmp_pos,self.len_L[1],target,self.len_L[2],self.old_anchor_L[0],self.old_anchor_L[2])
            for joint_2_tmp_pos in joint_2_tmp_pos_L:
                joint_pos_LL.append([self.start,joint_1_tmp_pos,joint_2_tmp_pos,target])
        # print(joint_pos_LL)
        best_joint_pos_L = []
        best_angle_delta = []
        # sum_abs_angle_delta = 0
        min_sort_abs_angle_delta = [float("Inf"),float("Inf"),float("Inf")]
        # print(self.old_angle_L)
        for joint_pos_L in joint_pos_LL:
            # print(joint_pos_L)
            tmp_new_angle_L = vec_to_angle(anchor_to_vec(self.h_vec,joint_pos_L),self.plane_normal)
            # new_sum_abs_angle_delta = sum_abs(angle_delta(self.old_angle_L,tmp_new_angle_L))
            tmp_angle_delta = angle_delta(self.old_angle_L,tmp_new_angle_L)
            tmp_sort_abs_angle_delta = sort_abs(tmp_angle_delta)
            # print(joint_pos_L,sum_abs_angle_delta)
            # print(tmp_new_angle_L)
            # if new_sum_abs_angle_delta < sum_abs_angle_delta:
                # sum_abs_angle_delta = new_sum_abs_angle_delta
            if cmp_angle_delta_L(tmp_sort_abs_angle_delta,min_sort_abs_angle_delta) == -1:
                best_joint_pos_L = joint_pos_L
                min_sort_abs_angle_delta = tmp_sort_abs_angle_delta
                best_angle_delta = tmp_angle_delta
            # print(tmp_angle_delta)
            # print(joint_pos_L[1],joint_pos_L[2])
            # print(joint_pos_L[1],joint_pos_L[2])
        # print(best_joint_pos_L)
        # print(best_angle_delta)
        best_joint_rot_L = list(map(add,self.old_rot_L,best_angle_delta))
        print(best_joint_rot_L)
        return best_joint_rot_L
        # return 
        # print(min_max_abs_angle_delta)
        # return best_angle_delta

    def set_joint_rot(self,new_rot_L,frm=None):
        for i, (joint,new_rot) in enumerate(zip(self.joint_L,new_rot_L)):
            old_rot_vec = get_rel_rot(joint)
            old_rot_vec[0] = new_rot
            if frm == None:
                set_rel_rot(joint,old_rot_vec)
                self.old_rot_L[i] = new_rot
            else:
                # set_rel_rot_key(joint,0,frm=0,dim=0)
                set_rel_rot_key(joint,new_rot,frm=frm,dim=0)


if __name__ == '__main__':
    clear_console()
    print("You are calling definitions!")