requirements:
	@pip install -r requirements.txt


# %%%%%%%%%%%%%% SERVICE %%%%%%%%%%%%%%
run: requirements redis workers
	@PYTHONPATH=$$PYTHONPATH:. r3-app --redis-port=7778 --redis-pass=r3 --config-file="./r3_gh/app_config.py"


# %%%%%%%%%%%%%% WORKER %%%%%%%%%%%%%%
worker:
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="1" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3

workers: kill-workers
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="1" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="2" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="3" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="4" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="5" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &
	@PYTHONPATH=$$PYTHONPATH:. r3-map --mapper-key="6" --mapper-class="r3_gh.mapper.CommitsPercentageMapper" --redis-port=7778 --redis-pass=r3 &

kill-workers:
	@ps aux | awk '(/r3-map --mapper-key/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'


# %%%%%%%%%%%%%% WEB %%%%%%%%%%%%%%
web:
	@PYTHONPATH=$$PYTHONPATH:. r3-web --redis-port=7778 --redis-pass=r3 --debug


# %%%%%%%%%%%%%% REDIS %%%%%%%%%%%%%%
kill_redis:
	@ps aux | awk '(/redis-server/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

redis: kill_redis
	@mkdir -p /tmp/r3/db
	@redis-server redis.conf &
