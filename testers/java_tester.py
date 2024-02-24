import os
import subprocess
import uuid

class JavaCompiler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.class_name = self.extract_class_name()
        self.executable_file = self.class_name + ".class"

    def extract_class_name(self):
        return os.path.basename(self.source_file).split('.')[0]

    def compile(self):
        try:
            result = subprocess.run(
                ["javac", self.source_file],
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode != 0:
                print(f"Compilation error: {result.stderr}")
                return False
            return True
        except OSError as e:
            print(f"Compilation failed: {e}")
            return False
        
    def __del__(self):
        try:
            os.remove(self.executable_file)
        except OSError:
            pass
        
class JavaExecutor(JavaCompiler):
    def __init__(self, source_file, input_file):
        super().__init__(source_file)
        self.input_file = input_file
        self.output_file = f"{self.class_name}_{str(uuid.uuid4())}.txt"

    def execute(self):
        if not self.compile():
            return ""
        try:
            with open(self.input_file, 'r') as file:
                input_data = file.read()

            result = subprocess.run(
                ["java", self.class_name],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.source_file)  # Execute in the directory of the source file
            )

            with open(self.output_file, "w") as f:
                f.write(result.stdout)

            if result.stderr:
                print(f"Runtime error: {result.stderr}")
            return self.output_file
        except OSError as e:
            print(f"Execution failed: {e}")
            return ""
        
    def run(self):
        return self.execute()
        
    def __del__(self):
        super().__del__()
        try:
            os.remove(self.output_file)
        except OSError:
            pass

    
class JavaTester(JavaExecutor):
    def __init__(self, source_file, input_file, expected_output_file):
        super().__init__(source_file, input_file)
        self.expected_output_file = expected_output_file

    def test(self):
        output_file = self.run()
        if output_file == "":
            return False
        with open(output_file, 'r') as file:
            output = file.read().strip()
        with open(self.expected_output_file, 'r') as file:
            expected_output = file.read().strip()
        return output == expected_output
    
    def __del__(self):
        super().__del__()
        try:
            os.remove(self.expected_output_file)
        except OSError:
            pass

def compare_java_codes_by_output(source_file, another_source_file, input_file):
    tester1 = JavaExecutor(source_file, input_file)
    tester2 = JavaExecutor(another_source_file, input_file)
    output1 = tester1.run()
    output2 = tester2.run()
    if output1 == "" or output2 == "":
        return False
    with open(output1, 'r') as file:
        output1 = file.read().strip()
    with open(output2, 'r') as file:
        output2 = file.read().strip()
    return output1 == output2
