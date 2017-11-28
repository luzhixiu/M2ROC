sudo service nginx stop
sudo pkill python
sudo pkill gunicorn
sudo gunicorn --bind 0.0.0.0:80 flaskapp:app --threads 12 -w 4

