from fastapi import FastAPI, Form, File
from kafka import KafkaProducer
import json
from uuid import uuid4
from enum import Enum
from settings import get_settings

app = FastAPI()
app_settings = get_settings()

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers=f"{app_settings.KAFKA_SERVER}:{str(app_settings.KAFKA_PORT)}", 
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    security_protocol='SASL_SSL',  # or 'SASL_SSL' if you're using SSL
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username=app_settings.KAFKA_USERNAME,  # Replace with your actual username
    sasl_plain_password=app_settings.KAFKA_PASSWORD   # Replace with your actual password
)


def get_temp_file_path():
    return "temp/" + str(uuid4())

SupportedLanguages: Enum = Enum("SupportedLanguages", app_settings.CONTEST_SUPPORTED_LANGUAGES)

@app.post("/compile_execute_all_file_types")
def compile_execute_all_file_types(code: bytes = File(...), input: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    task = {
        "task_type": "compile_execute",
        "code": code.decode(),
        "input": input.decode(),
        "programming_language": programming_language.value
    }
    producer.send(app_settings.KAFKA_TOPIC, value=task)
    return {"message": "Compilation and execution task submitted to Kafka."}

@app.post("/validate_input_output_all_file_types")
def validate_input_output_all_file_types(code: bytes = File(...), input: bytes = File(...), expected_output: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    task = {
        "task_type": "validate_input_output",
        "code": code.decode(),
        "input": input.decode(),
        "expected_output": expected_output.decode(),
        "programming_language": programming_language.value
    }
    producer.send(app_settings.KAFKA_TOPIC, value=task)
    return {"message": "Input/output validation task submitted to Kafka."}

@app.post("/compare_all_codes_by_output")
def compare_all_codes_by_output(code1: bytes = File(...), code2: bytes = File(...), input: bytes = File(...), programming_language: SupportedLanguages = Form(...)):
    task = {
        "task_type": "compare_codes",
        "code1": code1.decode(),
        "code2": code2.decode(),
        "input": input.decode(),
        "programming_language": programming_language.value
    }
    producer.send(app_settings.KAFKA_TOPIC, value=task)
    return {"message": "Code comparison task submitted to Kafka."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
