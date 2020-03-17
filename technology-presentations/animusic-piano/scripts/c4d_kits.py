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

def min_abs(num_L):
    return min(list(map(abs,num_L)))

def get_bros(obj, next_only=False, with_obj=True, condition=return_true):
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

# ARF = ["abs","rel","frozen"]
# PSR = ["pos","rot","scale"]

# def_set_arf_psr = "def set_{0}_{1}(obj,xyz): set_arf_psr(\"{0}\",\"{1}\",obj,xyz)"
# def_get_arf_psr = "def get_{0}_{1}(obj): return get_arf_psr(\"{0}\",\"{1}\",obj)"

# for arf in ARF:
#     for psr in PSR:
#         exec(def_set_arf_psr.format(arf,psr))
#         exec(def_get_arf_psr.format(arf,psr))

# I use these tedious definitions just to activate auto completions of Sublime
def get_abs_pos(obj):       return get_arf_psr("abs","pos",obj)
def get_abs_rot(obj):       return get_arf_psr("abs","rot",obj)
def get_abs_scale(obj):     return get_arf_psr("abs","scale",obj)
def get_rel_pos(obj):       return get_arf_psr("rel","pos",obj)
def get_rel_rot(obj):       return get_arf_psr("rel","rot",obj)
def get_rel_scale(obj):     return get_arf_psr("rel","scale",obj)
def get_frozen_pos(obj):    return get_arf_psr("frozen","pos",obj)
def get_frozen_rot(obj):    return get_arf_psr("frozen","rot",obj)
def get_frozen_scale(obj):  return get_arf_psr("frozen","scale",obj)

def set_abs_pos(obj,xyz):       set_arf_psr("abs","pos",obj,xyz)
def set_abs_rot(obj,xyz):       set_arf_psr("abs","rot",obj,xyz)
def set_abs_scale(obj,xyz):     set_arf_psr("abs","scale",obj,xyz)
def set_rel_pos(obj,xyz):       set_arf_psr("rel","pos",obj,xyz)
def set_rel_rot(obj,xyz):       set_arf_psr("rel","rot",obj,xyz)
def set_rel_scale(obj,xyz):     set_arf_psr("rel","scale",obj,xyz)
def set_frozen_pos(obj,xyz):    set_arf_psr("frozen","pos",obj,xyz)
def set_frozen_rot(obj,xyz):    set_arf_psr("frozen","rot",obj,xyz)
def set_frozen_scale(obj,xyz):  set_arf_psr("frozen","scale",obj,xyz)

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

def is_points_collinear(p1,p2,p3):
    if p_angle(p1,p2,p3) == 0:
        return True
    else:
        return False

def v_plane_normal(v1,v2):
    return v1.Cross(v2).GetNormalized()

def p_plane_normal(p1,p2,ref1,ref2=c4d.Vector(0,0,0)):
    ref = ref1
    if is_points_collinear(p1,p2,ref1):
        ref = ref2
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

def two_circle_intersection(p1,r1,p2,r2,ref):
    """ return intsect_L """
    # ref: reference point to determine plane orientation (c4d.Vector)
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

    plane_normal_vec = p_plane_normal(p1,p2,ref)

    # Q: What if ref,p1,p2 are collinear?
    # A1: Drop the result of next status of arm which makes them collinear.
        # Q: What if only one solution of intersection?
        # A: ...
    # A2: [Y] Or add one more ref to reduce the chances of this condition.
        # Q: What if the other ref also collinear?
        # A: ...
    # Do not worry about too many small things ... 

    p1p2_perp_vec = (p2-p1).Cross(plane_normal_vec).GetNormalized()

    intsect_L = []
    intsect_L.append(foot + p1p2_perp_vec * height)
    intsect_L.append(foot - p1p2_perp_vec * height)

    return intsect_L

def center_axis_to_anchor(end,center_L,axis_L):
    """ return anchor_L """
    anchor_L = []
    for center, axis in zip(center_L, axis_L):
        anchor_L.append(p_to_v_foot(end, center, axis))
    anchor_L.append(end)
    return anchor_L

def anchor_to_vec(base_vec,anchor_L):
    """ return vec_L """
    vec_L = []
    vec_L.append(base_vec)
    for i in range(len(anchor_L)-1):
        vec_L.append(anchor_L[i+1]-anchor_L[i])
    return vec_L

def vec_to_len(vec_L):
    """ return len_L """
    len_L = []
    for vec in vec_L[1:]:
        len_L.append(vec.GetLength())
    return len_L

def vec_to_angle(vec_L,normal):
    """ return angle_L """
    angle_L = []
    for i in range(len(vec_L)-1):
        angle_L.append(v_angle(-vec_L[i],vec_L[i+1],normal))
    return angle_L

def angle_delta(old_angle_L,new_angle_L):
    """ return float_L """
    return list(map(sub, new_angle_L, old_angle_L))

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
            self.old_axis_L.append(get_y_axis_vec(joint))
            self.old_center_L.append(get_world_pos(joint))
            self.old_rot_L.append(get_rel_rot(joint)[0])

        self.old_anchor_L = center_axis_to_anchor(self.end,self.old_center_L,self.old_axis_L)

        self.start = self.old_anchor_L[0]
        # h_vec might be replaced with v_rot axis
        self.h_vec = c4d.Vector(0,1,0)
        self.old_vec_L = anchor_to_vec(self.h_vec,self.old_anchor_L)
        self.len_L = vec_to_len(self.old_vec_L)

        self.plane_normal = self.old_axis_L[0].GetNormalized()

        self.old_angle_L = vec_to_angle(self.old_vec_L,self.plane_normal)

        # for angle in self.old_angle_L:
        #     print(angle)
        # for vec in self.old_vec_L:
        #     print(vec)
        # print(rotate_vec(self.old_vec_L[0],self.plane_normal,540)+self.start)

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

    def get_new_rot(self,target):
        if not self.is_target_reachable(target):
            print("Warning: Cannot reach target!")
            return None
        intsect_L = two_circle_intersection(self.start,self.len_L[0], target, self.len_L[-1]+self.len_L[-2],self.old_anchor_L[1])
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
            joint_2_tmp_pos_L = two_circle_intersection(joint_1_tmp_pos,self.len_L[1],target,self.len_L[2],self.old_axis_L[0])
            for joint_2_tmp_pos in joint_2_tmp_pos_L:
                joint_pos_LL.append([self.start,joint_1_tmp_pos,joint_2_tmp_pos,target])
        # print(joint_pos_LL)
        best_joint_pos_L = []
        # sum_abs_angle_delta = 0
        min_abs_angle_delta = float("Inf")
        # print(self.old_angle_L)
        for joint_pos_L in joint_pos_LL:
            # print(joint_pos_L)
            tmp_new_angle_L = vec_to_angle(anchor_to_vec(self.h_vec,joint_pos_L),self.plane_normal)
            # new_sum_abs_angle_delta = sum_abs(angle_delta(self.old_angle_L,tmp_new_angle_L))
            tmp_angle_delta = angle_delta(self.old_angle_L,tmp_new_angle_L)
            new_min_abs_angle_delta = min_abs(tmp_angle_delta)
            # print(joint_pos_L,sum_abs_angle_delta)
            # print(tmp_new_angle_L)
            # if new_sum_abs_angle_delta < sum_abs_angle_delta:
                # sum_abs_angle_delta = new_sum_abs_angle_delta
            if new_min_abs_angle_delta < min_abs_angle_delta:
                best_joint_pos_L = joint_pos_L
                min_abs_angle_delta = new_min_abs_angle_delta
            print(min_abs_angle_delta)
        print(best_joint_pos_L)

        # for tmp_pos in joint_1_tmp_pos_L:
        #     print(tmp_pos)

        # joint_2_tmp_pos_L = []
        # for joint_1_tmp_pos in joint_1_tmp_pos_L:
        #     tmp_intsect_L = two_circle_intersection(joint_1_tmp_pos,self.len_L[1],target,self.len_L[2],self.old_axis_L[0])
        #     if len(tmp_intsect_L)>1:
        #         tmp_angle_L = []
        #         for tmp_intsect in tmp_intsect_L:
        #             tmp_anchor_L = 

