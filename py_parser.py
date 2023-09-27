import fnmatch
import ast
import os


def find_files_with_function(directory, function_name_to_replace):
    python_files_with_function = []
    for root, _, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, '*.py'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    code = f.read()

                parsed_code = ast.parse(code)

                for node in ast.walk(parsed_code):
                    if isinstance(node, ast.FunctionDef) and node.name == function_name_to_replace:
                        python_files_with_function.append(file_path)
    if len(python_files_with_function) == 0:
        raise ValueError(f"Function '{function_name_to_replace}' not found in any Python file.")
    elif len(python_files_with_function) > 1:
        raise ValueError(f"Function '{function_name_to_replace}' found in multiple Python files.")

    return python_files_with_function


def replace_function_definition(file_path, function_name_to_replace, new_function_code):
    with open(file_path, 'r') as f:
        code = f.read()
    parsed_code = ast.parse(code)

    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef) and node.name == function_name_to_replace:

            new_function_ast = ast.parse(new_function_code).body[0]
            ast.copy_location(new_function_ast, node)
            node.__dict__ = new_function_ast.__dict__

    updated_code = ast.unparse(parsed_code)

    with open(file_path, 'w') as f:
        f.write(updated_code)


def get_return_value_of_function(function_name, file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    parsed_code = ast.parse(code)
    return_value = None
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:            
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Return):
                    return_value = subnode.value
                    break

    return return_value


def main(
        directory_to_search,
        function_name_to_replace,
        new_function_code,
        function_name_to_get_output
        ):
    files_with_function = find_files_with_function(directory_to_search, function_name_to_replace)
    file_path = files_with_function[0]
    replace_function_definition(file_path, function_name_to_replace, new_function_code)
    print(f"Function '{function_name_to_replace}' definition replaced in the file:")

    # return_value = get_return_value_of_function(function_name_to_get_output, file_path)
    # if return_value:
    #     print(f"The function '{function_name_to_get_output}' returns: {ast.dump(return_value)}")
    #     if isinstance(return_value, ast.Tuple):
    #         for elt in return_value.elts:
    #             if isinstance(elt, ast.Constant):
    #                 print(f"Constant Value: {elt.value}")
    #             else:
    #                 print("Element is not a constant.")
    #     else:
    #         print("Return value is not a tuple.")
    # else:
    #     print(f"The function '{function_name_to_get_output}' does not have a return statement or was not found in the file.")

    print(file_path)


directory_to_search = './files_to_parse'
function_name_to_replace = 'pivot_offline_database'
new_function_code = '''def new_function(x):
    return x ** 2
'''
function_name_to_get_output = 'pivot_offline_database'

try:
    print('Hello from py_parser.py')
    main(
        directory_to_search,
        function_name_to_replace,
        new_function_code,
        function_name_to_get_output
        )
except ValueError as e:
    print(e)
