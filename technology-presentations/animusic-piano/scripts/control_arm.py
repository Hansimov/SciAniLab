import sys
path_to_add = "H:/codes/SciAniLab/technology-presentations/animusic-piano/scripts/"
if not path_to_add in sys.path:
    sys.path.append(path_to_add)

import c4d_kits
reload(c4d_kits)
from c4d_kits import *

# obj_list = find_obj(".*Rot.*", "Arm_.*",case_sensitive=[1,0])
# doc.SetActiveObject(None,c4d.SELECTION_NEW)
# for obj in obj_list:
    # print(obj.GetName())
    # doc.SetActiveObject(obj,c4d.SELECTION_ADD)
# c4d.EventAdd()

clear_console()
arm_1 = find_obj("arm_1","")[0]
v_rot_1 = find_obj("v_rot_1",arm_1)[0]
v_rot_2 = find_obj("v_rot_2",arm_1)[0]
h_rot_1 = find_obj("h_rot_1",arm_1)[0]
h_rot_2 = find_obj("h_rot_2",arm_1)[0]
h_rot_3 = find_obj("h_rot_3",arm_1)[0]
loc_null = find_obj("loc_null",arm_1)[0]
loc_ball = find_obj("loc_ball",arm_1)[0]
cube_test = find_obj("cube_test","")[0]

start_undo()
add_undo(c4d.UNDOTYPE_CHANGE, arm_1)
end_undo()

p3 = get_world_pos(h_rot_3)
p2 = get_world_pos(h_rot_2)
v = get_y_axis_vec(h_rot_2)
o = get_world_pos(loc_ball)
# print(p_to_v_dist(o,p2,v))
# print(p_to_v_foot(o,p2,v))
# print(p_angle(p2,p3,o))
# print(get_world_pos(cube_test))
# print(get_rel_rot(h_rot_3)[0])
joints = find_obj("h_rot_.*","arm_1")
# get_joint_angle_new(get_world_pos(cube_test),get_world_pos(loc_ball),joints)
arm = Arm(joints,get_world_pos(loc_ball))
print(two_circle_intersection(arm.start,arm.len_L[0], get_world_pos(cube_test),arm.len_L[1]+arm.len_L[2], arm.end))
event_add()