class BaseCompiler:
    def __init__(self, source_file):
        self.source_file = source_file

    def compile(self):
        raise NotImplementedError

class BaseExecutor(BaseCompiler):
    def __init__(self, source_file, input_file):
        super().__init__(source_file)
        self.input_file = input_file

    def execute(self):
        raise NotImplementedError

    def run(self):
        if not self.compile():
            return ""
        return self.execute()

class BaseTester(BaseExecutor):
    def __init__(self, source_file, input_file, expected_output_file):
        super().__init__(source_file, input_file)
        self.expected_output_file = expected_output_file

    def test(self):
        raise NotImplementedError
