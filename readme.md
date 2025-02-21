docker build -t medi_scan_ai .
docker run -p 8001:8001 -v ./app:/app/app --name myMediScanAIContainer medi_scan_ai
docker ps
docker exec -it [container_id] bash
python app/analyze_image.py 5 A00055446 80
