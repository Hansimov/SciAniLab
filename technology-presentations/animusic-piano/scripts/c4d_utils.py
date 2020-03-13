import c4d
# c4d.CallCommand(13957) # Clear Console

# Must add the line below when importing this module, otherwise:
#   "NameError: Global Name `doc` is not defined"
doc = c4d.documents.GetActiveDocument()

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

def find_obj_in_root(name, root="", case_sensitive=True):
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
            def is_name_equal_root(obj):
                if obj.GetName() == root:
                    return True
            stack.extend(get_bros(first_obj, condition=is_name_equal_root))
    else:
    # root is a specified object
        stack.extend([root])

    # Depth First Search
    while stack != []:
        obj = stack.pop()
        # print(obj.GetName())
        if obj.GetName() == name:
            obj_list.append(obj)
        for child in obj.GetChildren()[::-1]:
            stack.append(child)

    # for obj in stack:
    #     print(obj.GetName())
    # return stack

    return obj_list