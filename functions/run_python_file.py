import os
import subprocess

from google.genai import types


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None,
) -> str:
    try:
        abs_wdir = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(abs_wdir, file_path)
        )

        valid_target = (
            os.path.commonpath([abs_wdir, target_file]) == abs_wdir
        )

        if not valid_target:
            return (
                f'Error: Cannot execute "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_file):
            return (
                f'Error: "{file_path}" does not exist '
                f'or is not a regular file'
            )

        if not target_file.endswith(".py"):
            return (
                f'Error: "{file_path}" is not a Python file'
            )

        command = ["python3", target_file]

        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=abs_wdir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        if completed.returncode != 0:
            output += (
                f"Process exited with code "
                f"{completed.returncode}\n"
            )

        if completed.stdout:
            output += f"STDOUT:\n{completed.stdout}"

        if completed.stderr:
            output += f"STDERR:\n{completed.stderr}"

        if not completed.stdout and not completed.stderr:
            output += "No output produced"

        return output.rstrip()

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file to execute relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional command-line arguments.",
            ),
        },
    ),
)
