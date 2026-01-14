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