python -m streamlit run app.py
cd ..
python -m streamlit run frontend/app.py

python -m uvicorn backend.main:app --port 8080

api key setup :

https://auth.openai.com/log-in

Api key:
[YOUR_OPENAI_API_KEY_HERE]


give create table query (You'll see a detailed script with comments!)
show all students
list employees where role is Data Scientist