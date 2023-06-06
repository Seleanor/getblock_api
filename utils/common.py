import json
import allure
from pydantic import ValidationError, BaseModel
from typing import Type, Any


def check_object_model(model: Type[BaseModel], _object: Any) -> Any:
    try:
        get_model = model.parse_obj(_object)
        return get_model
    except ValidationError as i:
        allure.attach(json.dumps(_object, indent=4), name="CLICK TO OPEN JSON",
                      attachment_type=allure.attachment_type.JSON)
        with allure.step(f"We have validation errors:\n{i}"):
            raise Exception(f"Validation object has errors")
