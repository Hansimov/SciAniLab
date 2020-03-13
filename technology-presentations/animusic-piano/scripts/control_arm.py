import sys
path_to_add = "H:/codes/SciAniLab/technology-presentations/animusic-piano/scripts/"
if not path_to_add in sys.path:
    sys.path.append(path_to_add)

import c4d_utils
reload(c4d_utils)
from c4d_utils import *

c4d.CallCommand(13957) # Clear Console

obj_list = find_obj_in_root("Cube", "Cube.3")
for obj in obj_list:
    print(obj.GetName())
# arm_list = []

# for i in dir(arm1):
#     print(i)
# print(arm1.GetChildren()[0].GetChildren())

# arm1 = doc.SearchObject("Arm_1")
# print(arm1.GetNext().GetName())
# cube = doc.SearchObject("Cube.4")
# print(cube.GetPred().GetName())

# cube = doc.SearchObject("Cylinder")
# print(cube.GetChildren()[0].GetName())
# print(cube.GetChildren())