### Backend
```
# activate env
source backend\venv\bin\activate

# run app (telegram endpoint)
python3 app.py
```

### Ngrok
```
ngrok http 5001
```

### Steps
1. run the backend app
2. run ngrok
3. copy ngrok cmd into backend/.env

### Postres DB on RDS
1. Open CloudShell
1. `psql -h remindme.cc5g4i0islpz.us-east-1.rds.amazonaws.com -U postgres -d remindme`
2. Enter the password