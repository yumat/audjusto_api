# 設定
```
virtualenv .env(初回のみ)
ctrl+shift+p python:select interprinter
pip install -r requirements.txt
``` 

# 起動
```
uvicorn app.main:app --reload --host=0.0.0.0 --port=8003
```

# 稼働確認
## ブラウザアクセス
```
http://localhost:8003/docs#/
```

## api実行
```
curl http://localhost:8003/api/health_check
```

# DB準備
```
cd dynamodb
sudo service docker start
docker-compose up -d
```



# lambda build
connect_db.pyの修正
```
./build.sh
```