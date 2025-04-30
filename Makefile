install:
	bash init_valhalla_data.sh

valhalla-up:
	docker-compose up -d

valhalla-down:
	docker-compose down

valhalla-clean:
	rm -rf ./valhalla_data
