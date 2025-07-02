# Build
First, create the `data` and `output` folders in the project root. Then, set up the Python virtual environment.   
To start building on powershell run the following:

```powershell
New-Item -ItemType Directory -Path "data"
New-Item -ItemType Directory -Path "output"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

For other shells, run the following:

```bash
mkdir data
mkdir output
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```