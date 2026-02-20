import re
import json

def extract_tool_call(text: str):
    """
    Extract tool name and arguments from XML-style tool call.
    Example:
    <multiply>{"a": 2, "b": 4}</multiply>
    """

    pattern = r"<(\w+)>(.*?)</\1>"
    match = re.search(pattern, text, re.DOTALL)

    if not match:
        return None, None

    tool_name = match.group(1)
    args_str = match.group(2).strip()

    try:
        arguments = json.loads(args_str)
    except json.JSONDecodeError:
        arguments = None

    return tool_name, arguments