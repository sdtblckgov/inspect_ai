from typing import Any, Literal, cast

import jsonpatch
from pydantic import BaseModel, Field, JsonValue

JSONType = Literal["string", "integer", "number", "boolean", "array", "object", "null"]

PythonType = Literal["str", "int", "float", "bool", "list", "dict", "None"]


def python_type_to_json_type(python_type: str | None) -> JSONType:
    match python_type:
        case "str":
            return "string"
        case "int":
            return "integer"
        case "float":
            return "number"
        case "bool":
            return "boolean"
        case "list":
            return "array"
        case "dict":
            return "object"
        case "None":
            return "null"
        # treat 'unknown' as string as anything can be converted to string
        case None:
            return "string"
        case _:
            raise ValueError(
                f"Unsupported type: {python_type} for Python to JSON conversion."
            )


def json_type_to_python_type(json_type: str) -> PythonType:
    match json_type:
        case "string":
            return "str"
        case "integer":
            return "int"
        case "number":
            return "float"
        case "boolean":
            return "bool"
        case "array":
            return "list"
        case "object":
            return "dict"
        case "null":
            return "None"
        case _:
            raise ValueError(
                f"Unsupported type: {json_type} for JSON to Python conversion."
            )


class JsonChange(BaseModel):
    """Describes a change to data using JSON Patch format."""

    op: Literal["remove", "add", "replace", "move", "test", "copy"]
    """Change operation."""

    path: str
    """Path within object that was changed (uses / to delimit levels)."""

    from_: str | None = Field(default=None, alias="from")
    """Location from which data was moved or copied."""

    value: JsonValue = Field(default=None)
    """Changed value."""

    model_config = {"populate_by_name": True}


def json_changes(
    before: dict[str, Any], after: dict[str, Any]
) -> list[JsonChange] | None:
    patch = jsonpatch.make_patch(before, after)
    if patch:
        return [JsonChange(**change) for change in cast(list[Any], patch)]
    else:
        return None