from fastapi import FastAPI, Form
import uvicorn
from fastapi import File

from uuid import uuid4
from testers.cpp_tester import CppCompiler, CppExecutor, CppTester, compare_cpp_codes_by_output
from testers.java_tester import JavaCompiler, JavaExecutor, JavaTester, compare_java_codes_by_output
from testers.rust_tester import RustCompiler, RustExecutor, RustTester, compare_rust_codes_by_output
from testers.python_tester import PythonExecutor, PythonTester, compare_python_codes_by_output
from testers.go_tester import GoCompiler, GoExecutor, GoTester, compare_go_codes_by_output
from enum import Enum
from settings import  get_settings
# import magic 
app = FastAPI()

app_settings = get_settings()

def get_temp_file_path():
    return "temp/" + str(uuid4())

SupportedLanguages : Enum = Enum("SupportedLanguages",  app_settings.CONTEST_SUPPORTED_LANGUAGES)




@app.post("/compile_execute_all_file_types")
def compile_execute_all_file_types(code: bytes = File(...), input: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    code_file_path = get_temp_file_path() + "." + programming_language.value
    input_file_path = get_temp_file_path() + ".txt"
    # 1. Save code to a temporary file
    with open(code_file_path, "wb") as f:
        f.write(code)

    # 2. Save input to a temporary file
    with open(input_file_path, "wb") as f:
        f.write(input)

    executors = {
        SupportedLanguages.CPP: CppExecutor,
        SupportedLanguages.JAVA: JavaExecutor,
        SupportedLanguages.RUST: RustExecutor,
        SupportedLanguages.PYTHON: PythonExecutor,
        SupportedLanguages.GO: GoExecutor
    }

    executer = executors[programming_language](code_file_path, input_file_path)
    
    output_file_path = executer.run()
    if output_file_path == "":
        return {"error": "Failed to execute the code"}
    else:
        with open(output_file_path, "r") as f:
            output = f.read()
        return {"output": output}





@app.post("/validate_input_output_all_file_types")
def validate_input_output_all_file_types(code: bytes = File(...), input: bytes = File(...), expected_output: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    code_file_path = get_temp_file_path() + "." + programming_language.value
    input_file_path = get_temp_file_path() + ".txt"
    output_file_path = get_temp_file_path() + ".txt"
    # 1. Save code to a temporary file
    with open(code_file_path, "wb") as f:
        f.write(code)

    # 2. Save input to a temporary file
    with open(input_file_path, "wb") as f:
        f.write(input)

    # 3. Save output to a temporary file
    with open(output_file_path, "wb") as f:
        f.write(expected_output)

    testers = {
        SupportedLanguages.CPP: CppTester,
        SupportedLanguages.JAVA: JavaTester,
        SupportedLanguages.RUST: RustTester,
        SupportedLanguages.PYTHON: PythonTester,
        SupportedLanguages.GO: GoTester
    }

    tester = testers[programming_language](code_file_path, input_file_path, output_file_path)
    
    result = tester.test()
    if result:
        return {"result": "Accepted"}
    else:
        return {"result": "Wrong Answer"}



@app.post("/compare_all_codes_by_output")
def compare_all_codes_by_output(code1: bytes = File(...), code2: bytes = File(...), input: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    code1_file_path = get_temp_file_path() + "." + programming_language.value
    code2_file_path = get_temp_file_path() + "." + programming_language.value
    input_file_path = get_temp_file_path() + ".txt"
    # 1. Save code1 to a temporary file
    with open(code1_file_path, "wb") as f:
        f.write(code1)

    # 2. Save code2 to a temporary file
    with open(code2_file_path, "wb") as f:
        f.write(code2)

    # 3. Save input to a temporary file
    with open(input_file_path, "wb") as f:
        f.write(input)

    compare_functions = {
        SupportedLanguages.CPP: compare_cpp_codes_by_output,
        SupportedLanguages.JAVA: compare_java_codes_by_output,
        SupportedLanguages.RUST: compare_rust_codes_by_output,
        SupportedLanguages.PYTHON: compare_python_codes_by_output,
        SupportedLanguages.GO: compare_go_codes_by_output
    }

    compare_function = compare_functions[programming_language]

    result = compare_function(code1_file_path, code2_file_path, input_file_path)

    
    if result:
        return {"result": "Same Output"}
    else:
        return {"result": "Different Output"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" , port=8000)
