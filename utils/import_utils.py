from typing import Any
import os
import sys
import importlib
import importlib.util


def import_object(full_path: str) -> Any:
    """
    Dynamically imports an object from a given module specified by its full path.

    This function supports importing from both filesystem paths and installed modules.
    If the path contains a '/', it is treated as a filesystem path.
    Otherwise, it is treated as a module path.
    The object name should be the last component after a period in the given path.

    :param full_path: The full path to the object, including directory, module, and object names.

    :return: The object specified by `full_path`.
    """
    if '/' in full_path:
        # Handling file system path imports
        module_path, obj_name = full_path.rsplit('.', 1)
        dir_path, file_name = os.path.split(module_path)
        module_base_name, _ = os.path.splitext(file_name)
        if dir_path not in sys.path:
            sys.path.append(dir_path)  # Ensure the directory is in sys.path

        module_file_path = os.path.join(dir_path, module_base_name + '.py')
        module_spec = importlib.util.spec_from_file_location(module_base_name, module_file_path)
        loaded_module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(loaded_module)

        return getattr(loaded_module, obj_name)
    
    elif '.' in full_path:
        module_base_name, obj_name = full_path.rsplit('.', 1)
        loaded_module = importlib.import_module(module_base_name)
        
        return getattr(loaded_module, obj_name)


# def some_function(x):  # for testing
#     return x
# 
# 
# def test_import_object_from_str():
#     func_result = import_object(
#         os.path.abspath(__file__) + ".some_function"
#     )
#     assert func_result(7) == 7
#     ceil = import_object("math.ceil")
#     assert 3 == ceil(2.5)
#     det = import_object("numpy.linalg.det")
#     import numpy as np
#     assert det(np.array([[1, 0], [0, 1]])) == 1
