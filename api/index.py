import sys
import os
from pathlib import Path
from mangum import Mangum

# Add the 'backend' folder to sys.path so we can import 'app'
# We are currently in /var/task/api/index.py (roughly)
# We need to reach /var/task/backend
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "backend"))

from backend.app.main import app

# Wrap the FastAPI app with Mangum for Vercel/Lambda compatibility
handler = Mangum(app)
