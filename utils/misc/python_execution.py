import subprocess
import asyncio


def execute_python_code(python_code, timeout=2):
    try:
        # Define a list of disallowed module names
        disallowed_modules = [
            "os",
            "subprocess",
            "sys",
            "shutil",
            "socket",
            "ctypes",
            "pickle",
        ]

        new_import = """
def __import__(name, globals=None, locals=None, fromlist=(), level=0):
    if name in disallowed_modules:
        raise ImportError('不允许导入 ' + name + ' 包')
    return old_import(name, globals, locals, fromlist, level)
"""
        # Define a new open function that raises an exception
        new_open = """
def open(*args, **kwargs):
    raise PermissionError('不允许打开文件')
"""
        # Save the old __import__ and open functions and override them with the new ones
        python_code = (
            "old_import = __builtins__.__import__\n"
            + "disallowed_modules = "
            + str(disallowed_modules)
            + "\n"
            + new_import
            + "\n__builtins__.__import__ = __import__\n"
            + "old_open = __builtins__.open\n"
            + new_open
            + "\n__builtins__.open = open\n"
            + python_code
        )

        # Execute the Python code with a timeout
        process = subprocess.Popen(
            ["python3", "-c", python_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = process.communicate(timeout=timeout)

        # Decode the output bytes to a string
        output_str = output.decode("utf-8")
        error_str = error.decode("utf-8")

        return output_str + "\n" + error_str
    except subprocess.TimeoutExpired:
        return "Timeout: Execution took longer than {} seconds.".format(timeout)
    except Exception as e:
        return str(e)


async def async_execute_python_code(python_code, timeout=2):
    try:
        # Define a list of disallowed module names
        disallowed_modules = [
            "os",
            "subprocess",
            "sys",
            "shutil",
            "socket",
            "ctypes",
            "pickle",
        ]

        new_import = """
def __import__(name, globals=None, locals=None, fromlist=(), level=0):
    if name in disallowed_modules:
        raise ImportError('不允许导入 ' + name + ' 包')
    return old_import(name, globals, locals, fromlist, level)
"""
        # Define a new open function that raises an exception
        new_open = """
def open(*args, **kwargs):
    raise PermissionError('不允许打开文件')
"""
        # Save the old __import__ and open functions and override them with the new ones
        python_code = (
            "old_import = __builtins__.__import__\n"
            + "disallowed_modules = "
            + str(disallowed_modules)
            + "\n"
            + new_import
            + "\n__builtins__.__import__ = __import__\n"
            + "old_open = __builtins__.open\n"
            + new_open
            + "\n__builtins__.open = open\n"
            + python_code
        )

        # Execute the Python code with a timeout
        process = await asyncio.create_subprocess_exec(
            "python3",
            "-c",
            python_code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            output, error = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            output, error = await process.communicate()

        # Decode the output bytes to a string
        output_str = output.decode("utf-8")
        error_str = error.decode("utf-8")

        return output_str + "\n" + error_str
    except Exception as e:
        return str(e)
