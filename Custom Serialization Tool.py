import re

# ---  Custom Serialization Tool ---
class CustomDataSerializationTool:
    def serialize(self, data):
        """Serializes the given data into custom format."""
        if isinstance(data, dict):
            return self.serialize_dict(data)
        elif isinstance(data, list):
            return self.serialize_list(data)
        elif isinstance(data, str):
            return f'"{data}"'  # Serialize strings with quotes
        elif isinstance(data, (int, float)):
            return str(data)  # Serialize numbers directly
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def serialize_dict(self, data):
        """Serializes a dictionary into custom format."""
        result = "{"
        for key, value in data.items():
            serialized_key = f'"{key}"'
            serialized_value = self.serialize(value)
            result += f'{serialized_key}: {serialized_value}, '
        return result.rstrip(', ') + '}'

    def serialize_list(self, data):
        """Serializes a list into custom format."""
        result = "["
        for item in data:
            serialized_item = self.serialize(item)
            result += f'{serialized_item}, '
        return result.rstrip(', ') + "]"

    def deserialize(self, data_str):
        """Deserializes a custom format string into Python data."""
        if data_str.startswith("{"):
            return self.deserialize_dict(data_str)
        elif data_str.startswith("["):
            return self.deserialize_list(data_str)
        elif data_str.startswith('"') and data_str.endswith('"'):
            return data_str[1:-1]  # Deserialize string
        elif re.match(r'^-?\d+(\.\d+)?$', data_str):  # Match numbers (int or float)
            return float(data_str) if '.' in data_str else int(data_str)
        else:
            raise ValueError("Invalid data format")

    def deserialize_dict(self, data_str):
        """Deserializes a dictionary from custom format."""
        data_str = data_str[1:-1].strip()  # Remove the curly braces
        data = {}
        if data_str:
            pairs = data_str.split(", ")
            for pair in pairs:
                key, value = pair.split(": ")
                key = key[1:-1]  # Remove quotes from the key
                data[key] = self.deserialize(value)
        return data

    def deserialize_list(self, data_str):
        """Deserializes a list from custom format."""
        data_str = data_str[1:-1].strip()  # Remove the square brackets
        items = []
        if data_str:
            for item in data_str.split(", "):
                items.append(self.deserialize(item))
        return items

    def validate_schema(self, data, schema):
        """Validates data against a schema."""
        # Simple schema validation: checking types based on the schema
        if isinstance(data, dict):
            if not isinstance(schema, dict):
                raise ValueError(f"Schema mismatch: expected dictionary, got {type(data)}")
            for key, value in schema.items():
                if key not in data:
                    raise ValueError(f"Missing key: {key}")
                self.validate_schema(data[key], value)  # Recursively validate nested structures
        elif isinstance(data, list):
            if not isinstance(schema, list):
                raise ValueError(f"Schema mismatch: expected list, got {type(data)}")
            for item in data:
                self.validate_schema(item, schema[0])  # List schema should match the item type
        elif isinstance(data, (int, float)):
            if not isinstance(schema, (int, float)):
                raise ValueError(f"Schema mismatch: expected {type(schema)}, got {type(data)}")
        elif isinstance(data, str):
            if not isinstance(schema, str):
                raise ValueError(f"Schema mismatch: expected string, got {type(data)}")
        else:
            raise ValueError(f"Unsupported schema type: {type(schema)}")

# --- Testing the Custom Serialization Tool ---
def test_custom_serialization_tool():
    tool = CustomDataSerializationTool()
    # Sample data
    data_dict = {
        "name": "Alice",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Wonderland"
        },
        "friends": ["Bob", "Charlie", "David"]
    }
    # Sample schema
    schema_dict = {
        "name": str,
        "age": int,
        "address": {
            "street": str,
            "city": str
        },
        "friends": [str]
    }
    # Serialize the data
    serialized_data = tool.serialize(data_dict)
    print(f"Serialized Data: {serialized_data}")
    # Deserialize the data
    deserialized_data = tool.deserialize(serialized_data)
    print(f"Deserialized Data: {deserialized_data}")
    # Validate schema
    try:
        tool.validate_schema(deserialized_data, schema_dict)
        print("Schema validation passed!")
    except ValueError as e:
        print(f"Schema validation failed: {e}")

if __name__ == "__main__":
    test_custom_serialization_tool()