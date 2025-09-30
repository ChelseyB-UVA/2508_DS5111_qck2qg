
import platform
import sys
sys.path.append('.')

import bin.normalize_gainers as nm

def test_of_pytest():
    assert True

def test_python_version():
    """Checking the version is 3.10 or newer"""
    major, minor = sys.version_info[:2]
    assert (major, minor) >= (3, 10), f"Python {major}.{minor} is to old!"
    print(f"Python version:{major}.{minor}")

def test_os_version():
    """Check Operating System (os) name and version."""
    os_name = platform.system()
    os_version = platform.release()

    print(f"Operating System: {os_name} {os_version}")
    assert True
