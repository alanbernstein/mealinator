"""
Utility functions for smart file writing that preserves timestamps
when content hasn't changed.
"""

import os
import filecmp
import shutil

def write_if_changed(file_path, content, encoding='utf-8'):
    """
    Write content to file only if it has changed.

    This preserves the file's modification time if the content is identical,
    which allows incremental deployment to work correctly.

    Args:
        file_path: Path to the file
        content: Content to write (string or bytes)
        encoding: Text encoding (only used if content is string)

    Returns:
        bool: True if file was written (changed), False if skipped (unchanged)
    """
    # Ensure parent directory exists
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # Check if file exists
    if not os.path.exists(file_path):
        # File doesn't exist, write it
        _write_file(file_path, content, encoding)
        return True

    # File exists, compare content
    temp_path = file_path + '.tmp'
    _write_file(temp_path, content, encoding)

    # Compare files
    if filecmp.cmp(file_path, temp_path, shallow=False):
        # Content is identical, remove temp and keep original
        os.remove(temp_path)
        return False
    else:
        # Content changed, replace original with temp
        shutil.move(temp_path, file_path)
        return True

def _write_file(file_path, content, encoding):
    """Helper to write content to file."""
    if isinstance(content, str):
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    else:
        with open(file_path, 'wb') as f:
            f.write(content)
