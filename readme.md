how to update requiremnt.txt from venv

.\.venv\Scripts\Activate.ps1
(.venv) PS D:\Atul\ai-support-desk-oct-26> Copy-Item requirements.txt requirements.backup.txt
(.venv) PS D:\Atul\ai-support-desk-oct-26> python -m pip freeze > requirements.txt
Get-Content requirements.txt


  git config --global user.email "atul.yadav@merriment.co"
  git config --global user.name "Atul Yadav"

python --version


python -m pip --version
python -m pip install fastapi "uvicorn[standard]"
python -m pip install uvicorn
python -m pip install -r requirements.txt
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --reload --port 8001
python -m pip install fastapi "uvicorn[standard]"
python -m pip install langchain-chroma
python -m pip install langchain-openai
python -m pip install openpyxl
python -m pip install pypdf
python -m pip install PyMuPDF
python -m pip install python-docx

python -m pip install django

python manage.py runserver 8000