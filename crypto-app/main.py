from fastapi import FastAPI
import cryptocompare, redis, pickle, time

app = FastAPI(title='FastAPI Redis Tutorial')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/about")
async def about():
    redis_client.flushall()
    return {"Data": "About"}

@app.get("/crypto/{name}")
async def crypto(name: str):
    start_time = time.time()
    price = redis_client.get(name)
    if not price:
        price_l = cryptocompare.get_price(name)
        price_d = pickle.dumps(price_l)
        server_type = 'API'
        redis_client.set(name, price_d)
    else:
        price_l = pickle.loads(price)
        server_type = 'Redis'
    totalTime = time.time() - start_time
    return {"crypto":price_l, 'Total Time':totalTime, 'Type':server_type}
