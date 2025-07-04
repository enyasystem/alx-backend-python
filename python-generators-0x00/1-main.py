
from itertools import islice
import importlib.util
import sys

# Dynamically import stream_users from 0-stream_users.py
spec = importlib.util.spec_from_file_location(
    "stream_users", "python-generators-0x00/0-stream_users.py"
)
stream_users_module = importlib.util.module_from_spec(spec)
sys.modules["stream_users"] = stream_users_module
spec.loader.exec_module(stream_users_module)
stream_users = stream_users_module.stream_users

# Print the first 6 users from the generator
for user in islice(stream_users(), 6):
    print(user)
