from pydantic import BaseModel, ValidationError


def validate_response_schema(json_response: dict, model_class):
    print("Raw JSON response:", json_response)
    try:
        model_class(**json_response)
        print("Schema validated successfully")
    except ValidationError as e:
        print("Schema validation failed:")
        print(e)
        raise