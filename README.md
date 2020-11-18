**Activate the virtual environment**
"""
blockchain-env/Scripts/activate
"""

**Install all packages**
"""
pip3 install -r requirements.txt
"""

**Run the tests**
"""
Make sure that the virtual environment is activated.
python -m pytest backend\tests
"""

**Run the application and API**
"""
Make sure that the virtual environment is activated.
python -m backend.app
"""

**Run a peer instance**
"""
Make sure that the virtual environment is activated.
set PEER=True && python -m backend.app
"""

**Seed the backend with data**
"""
Make sure that the virtual environment is activated.
set SEED_DATA=True && python -m backend.app
"""

**Run the frontend**
"""
In the frontend directory.
npm run start
"""
