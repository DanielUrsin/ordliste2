import requests
import time

n = 2

t1 = time.time()
for i in range(n):
    res = requests.get("http://85.166.149.205:23232/ord?alder=13")
    print(res.text)
t2 = time.time()

print(f"served {n/(t2-t1)} requests per sec")
