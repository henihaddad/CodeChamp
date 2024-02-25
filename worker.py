from kafka import KafkaConsumer
import json
from uuid import uuid4
from enum import Enum
from settings import get_settings

# Import your testers and executors
from testers.cpp_tester import CppCompiler, CppExecutor, CppTester, compare_cpp_codes_by_output
from testers.java_tester import JavaCompiler, JavaExecutor, JavaTester, compare_java_codes_by_output
from testers.rust_tester import RustCompiler, RustExecutor, RustTester, compare_rust_codes_by_output
from testers.python_tester import PythonExecutor, PythonTester, compare_python_codes_by_output
from testers.go_tester import GoCompiler, GoExecutor, GoTester, compare_go_codes_by_output

app_settings = get_settings()

SupportedLanguages: Enum = Enum("SupportedLanguages", app_settings.CONTEST_SUPPORTED_LANGUAGES)

consumer = KafkaConsumer(
    app_settings.KAFKA_TOPIC,
    bootstrap_servers=[app_settings.KAFKA_SERVER+":"+str(app_settings.KAFKA_PORT)],  # Adjust this to your Kafka server
    auto_offset_reset='earliest',
    group_id=app_settings.KAFKA_GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    security_protocol='SASL_SSL',  # or 'SASL_SSL' if you're using SSL
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username=app_settings.KAFKA_USERNAME,  # Replace with your actual username
    sasl_plain_password=app_settings.KAFKA_PASSWORD   # Replace with your actual password
)


def get_temp_file_path(extension=""):
    return "temp/" + str(uuid4()) + extension

def write_temp_file(content, extension=""):
    file_path = get_temp_file_path(extension)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

def execute_task(task):
    code = task['code'].encode()
    input_data = task['input'].encode()
    programming_language = SupportedLanguages(task['programming_language'])
    code_file_path = write_temp_file(code, f".{programming_language.value}")
    input_file_path = write_temp_file(input_data, ".txt")

    if task['task_type'] == 'compile_execute':
        executors = {
            SupportedLanguages.CPP: CppExecutor,
            SupportedLanguages.JAVA: JavaExecutor,
            SupportedLanguages.RUST: RustExecutor,
            SupportedLanguages.PYTHON: PythonExecutor,
            SupportedLanguages.GO: GoExecutor
        }
        executor_class = executors[programming_language]
        executor = executor_class(code_file_path, input_file_path)
        output_file_path = executor.run()
        if output_file_path:
            with open(output_file_path, "r") as f:
                output = f.read()
            print("Execution Output:", output)
        else:
            print("Execution failed")

    elif task['task_type'] == 'validate_input_output':
        expected_output = task['expected_output'].encode()
        output_file_path = write_temp_file(expected_output, ".txt")

        testers = {
            SupportedLanguages.CPP: CppTester,
            SupportedLanguages.JAVA: JavaTester,
            SupportedLanguages.RUST: RustTester,
            SupportedLanguages.PYTHON: PythonTester,
            SupportedLanguages.GO: GoTester
        }
        tester_class = testers[programming_language]
        tester = tester_class(code_file_path, input_file_path, output_file_path)
        result = tester.test()
        print("Validation Result:", "Accepted" if result else "Wrong Answer")

    elif task['task_type'] == 'compare_codes':
        code2 = task['code2'].encode()
        code2_file_path = write_temp_file(code2, f".{programming_language.value}")
        
        compare_functions = {
            SupportedLanguages.CPP: compare_cpp_codes_by_output,
            SupportedLanguages.JAVA: compare_java_codes_by_output,
            SupportedLanguages.RUST: compare_rust_codes_by_output,
            SupportedLanguages.PYTHON: compare_python_codes_by_output,
            SupportedLanguages.GO: compare_go_codes_by_output
        }
        
        compare_function = compare_functions[programming_language]
        result = compare_function(code_file_path, code2_file_path, input_file_path)
        print("Comparison Result:", "Same Output" if result else "Different Output")

for message in consumer:
    print("Received task:", message.value)
    task = message.value
    print("Processing task:", task)
    execute_task(task)
