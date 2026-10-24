"""
LifeOps API Test Configuration
Sets test environment variables before any module is loaded.
"""
import os
import sys
from pathlib import Path

# Add api directory to sys.path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

# Mock environment variables for hermetic testing (formatted as JWT for supabase-py validation)
DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJvbGUiOiJzZXJ2aWNlX3JvbGUifQ.mocksignature"

os.environ["SUPABASE_URL"] = "https://mock-supabase.datalaria.internal"
os.environ["SUPABASE_ANON_KEY"] = DUMMY_JWT
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = DUMMY_JWT
os.environ["SUPABASE_JWT_SECRET"] = "test-secret-key-32-chars-long-minimum!!"
