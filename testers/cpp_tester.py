import os
import subprocess

class CppCompiler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.executable_file = source_file.split('.')[0] + ".exe"

    def compile(self):
        try:
            result = subprocess.run(
                ["g++", self.source_file, "-o", self.executable_file],
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode != 0:
                return False

            return True

        except OSError as e:
            return False
        
    def __del__(self):
        try:
            os.remove(self.executable_file)
        except:
            pass
        
class CppExecutor(CppCompiler):
    def __init__(self, source_file, input_file):
        super().__init__(source_file)
        self.input_file = input_file
        self.output_file = source_file.split('.')[0] + ".txt"

    def execute(self):
        try:
            with open(self.input_file, 'r') as file:
                input = file.read()

            result = subprocess.run(
                ["./" + self.executable_file],
                input=input,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            with open(self.output_file, "w") as f:
                f.write(result.stdout)

            return self.output_file

        except OSError as e:
            return ""
        
    def run(self):
        if not self.compile():
            return ""
        return self.execute()
    
    def __del__(self):
        super().__del__()
        try:
            os.remove(self.output_file)
        except:
            pass
     
    
class CppTester(CppExecutor):
    def __init__(self, source_file, input_file, expected_output_file):
        super().__init__(source_file, input_file)
        self.expected_output_file = expected_output_file

    def test(self):
        output_file = self.run()
        if output_file == "":
            return False
        with open(output_file, 'r') as file:
            output = file.read()
        with open(self.expected_output_file, 'r') as file:
            expected_output = file.read()
        return output == expected_output
    
    def __del__(self):
        super().__del__()
        try:
            os.remove(self.expected_output_file)
        except:
            pass


        
def compare_cpp_codes_by_output(source_file, another_source_file, input_file):
    tester1 = CppExecutor(source_file, input_file)
    tester2 = CppExecutor(another_source_file, input_file)
    output1 = tester1.run()
    output2 = tester2.run()
    if output1 == "" or output2 == "":
        return False
    with open(output1, 'r') as file:
        output1 = file.read()
    with open(output2, 'r') as file:
        output2 = file.read()
    return output1 == output2