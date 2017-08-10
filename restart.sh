sudo pkill python
sudo pkill gunicorn
sudo gunicorn --bind 0.0.0.0:80 preset:app
