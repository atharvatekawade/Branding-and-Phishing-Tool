echo " BUILD START"
python3.11.0  -m pip install -r requirements.txt
python3.11.0 manage.py collectstatic  --noinput --clear
echo " BUILD END"