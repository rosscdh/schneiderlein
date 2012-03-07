Need to install 
=====

* selenium - comes packaged in /bin/
* firefox - apt-get/aptitude install firefox
* Xvfb - apt-get/aptitude install Xvfb

Remember to run
=====

* ./manage.py runserver_plus (or runserver)
* ./manage.py tailor_start

Tailor Start Performs these actions
=====

* export DISPLAY=localhost:0.0
* Start Xvfb :0 -screen 0 1280x1024x24
* Start Selenium