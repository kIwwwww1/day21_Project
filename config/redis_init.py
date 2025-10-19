from redis import Redis

redis_client = Redis(host='localhost', decode_responses=True) # Заменить при деплое