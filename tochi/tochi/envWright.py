import os
from typing import Dict, Any

class EnvWriter:
    
    @staticmethod
    def format_value(value: Any) -> str:
        """Format a value for writing to .env file"""
        if isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            # Escape quotes and wrap in quotes if string contains spaces
            value_str = str(value)
            if ' ' in value_str or '\n' in value_str or '=' in value_str:
                # Fixed the f-string syntax
                return '"{}"'.format(value_str.replace('"', '\\"'))
            return value_str

    @staticmethod
    def read_existing_env(filename: str) -> Dict[str, str]:
        """Read existing .env file into a dictionary"""
        env_dict = {}
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env_dict[key.strip()] = value.strip()
        return env_dict

    @staticmethod
    def write_env(filename: str, data: Dict[str, Any], mode: str = 'update') -> None:
        """
        Write or update environment variables in .env file
        
        Args:
            filename: Path to .env file
            data: Dictionary of variables to write
            mode: 'update' to preserve existing variables, 'overwrite' to replace file
        """
        # Prepare the final data to write
        final_data = {}
        
        # If updating, read existing data first
        if mode == 'update' and os.path.exists(filename):
            final_data = EnvWriter.read_existing_env(filename)
        
        # Update with new data, handling nested dictionaries
        for key, value in data.items():
            if isinstance(value, dict):
                # Handle nested dictionary
                for sub_key, sub_value in value.items():
                    final_data[f"{key}_{sub_key}".upper()] = sub_value
            else:
                final_data[key.upper()] = value

        # Write to file
        try:
            with open(filename, 'w') as file:
                for key, value in final_data.items():
                    formatted_value = EnvWriter.format_value(value)
                    file.write("{}={}\n".format(key, formatted_value))
        except Exception as e:
            raise Exception(f"Failed to write to .env file: {str(e)}")

    @staticmethod
    def append_env(filename: str, data: Dict[str, Any]) -> None:
        """Append new variables to .env file without reading existing ones"""
        try:
            with open(filename, 'a') as file:
                for key, value in data.items():
                    formatted_value = EnvWriter.format_value(value)
                    file.write("{}={}\n".format(key, formatted_value))
        except Exception as e:
            raise Exception(f"Failed to append to .env file: {str(e)}")