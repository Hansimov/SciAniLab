import sys
path_to_add = "H:/codes/SciAniLab/technology-presentations/animusic-piano/scripts/"
if not path_to_add in sys.path:
    sys.path.append(path_to_add)

import c4d_kits
reload(c4d_kits)
from c4d_kits import *

# obj_list = find_obj_in_root("Cube","")
# obj_list = find_obj_in_root(".*Rot.*", "Arm_.*",case_sensitive=[1,0])
# doc.SetActiveObject(None,c4d.SELECTION_NEW)
# for obj in obj_list:
    # print(obj.GetName())
    # doc.SetActiveObject(obj,c4d.SELECTION_ADD)
# c4d.EventAdd()

clear_console()
arm_1 = find_obj_in_root("arm_1","")[0]
v_rot_1 = find_obj_in_root("v_rot_1",arm_1)[0]
v_rot_2 = find_obj_in_root("v_rot_2",arm_1)[0]
h_rot_1 = find_obj_in_root("h_rot_1",arm_1)[0]
h_rot_2 = find_obj_in_root("h_rot_2",arm_1)[0]
h_rot_3 = find_obj_in_root("h_rot_3",arm_1)[0]
locator = find_obj_in_root("locator",arm_1)[0]
ball = find_obj_in_root("ball",arm_1)[0]

cube = find_obj_in_root("cube_test","")[0]

# print(arm_1.GetName())
# print("=========")
start_undo()
add_undo(c4d.UNDOTYPE_CHANGE, arm_1)
# add_undo(c4d.UNDOTYPE_CHANGE_SMALL, v_rot_1)
# # add_undo(c4d.UNDOTYPE_CHANGE_SMALL, h_rot_1)
# v_rot_1.SetRelRot(rot_vec(20,0,0))
# v_rot_2.SetRelRot(rot_vec(20,0,0))
# h_rot_1.SetRelRot(rot_vec(-20,0,0))
# print(v_rot_1.GetMl())
# print(v_rot_1.GetAbsPos())
# set_rel_rot(v_rot_1,[180,0,0])
# print(type(arm_1))
# print(type(v_rot_1))
# print(h_rot_1.GetMg())
# print(h_rot_2.GetMg())
# v1 = h_rot_1.GetMg().off
# v2 = h_rot_2.GetMg().off
# v3 = v1 - v2
# print(v3)
# dist = sqrt(v3[1]*v3[1]+v3[2]*v3[2])
# print(dist)
# print(v_rot_1.GetMg())
# print(v_rot_2.GetMg().off)
# print(locator.GetMg().off)
# print(ball.GetMg().off)
# print(ball.GetMl().off)
# print(get_rel_pos(ball))
# print(get_rel_rot(ball))
# print(get_rel_scale(ball))
add_undo(c4d.UNDOTYPE_CHANGE, cube)
print(get_world_pos(cube))
set_world_pos(cube,[100,200,300])
end_undo()
event_add()
print(get_world_pos(cube))
# print(get_rel_rot(v_rot_1))
# print(v_rot_1.GetAbsRot())