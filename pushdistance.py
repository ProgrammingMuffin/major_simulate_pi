from redis import Redis
import redisconfig as conf

r = Redis(conf.HOST, conf.PORT, conf.DB, conf.PASSWORD)

r.set(conf.DISTANCE_PUSHED_KEY, "false")
r.set(conf.DISTANCE_VALUE_KEY, "0")
r.set(conf.DISTANCE_REQUESTED_KEY, "false")

def pushDistanceToRedis():
    value = 0
    for i in range(1, 4):
        value += float(exec(open("ultrasonic.py").read())) #runs only in python 3+
    distance = value / 3
    r.set(conf.DISTANCE_VALUE_KEY, distance)

while (r.get(conf.EXIT_KEY) == "false"):
    is_distance_requested = r.get(conf.DISTANCE_REQUESTED_KEY)
    if (is_distance_requested == "true"):
        pushDistanceToRedis()
        r.set(conf.DISTANCE_PUSHED_KEY, "true")
        r.set(conf.DISTANCE_REQUESTED_KEY, "false")

print("Exiting Redis Listener")