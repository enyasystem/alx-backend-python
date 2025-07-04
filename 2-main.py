import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "batch_processing", "python-generators-0x00/1-batch_processing.py"
)
processing = importlib.util.module_from_spec(spec)
sys.modules["batch_processing"] = processing
spec.loader.exec_module(processing)

# Print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
