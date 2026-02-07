from tools.builtin.read_file import ReadFileTool
__all__ = [
    'ReadFileTool'
]

def get_all_builitin_tools() -> list[type]:
    return [
        ReadFileTool,
    ]