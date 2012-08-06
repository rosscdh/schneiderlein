The valiant little tailor
=====

This is a django app that integrates with selenium to produce pixel perfect url comparisons.

Ie.. you have a list of urls that you want to ensure always look the same (or indeed jsut elements on that page); 
The app allows you to define pages and view those pages via selenium.
You can select whole pages or just elements on a page to test


1. define the urls you want to test in the "Pages" section
2. run the tests
3. profit


Management Commands
=====

* manage.py tailor_cutting_room - Allows you to manage the cutting room, delete screenshots etc
* manage.py tailor_run_layout_test <page_id page_id ...> - generate specific page id screenshots
* manage.py tailor_start - Start the tailor process, this starts Xvfb and Selenium

Need to install 
=====

Youll probably want to run this app on a ubuntu VM

* selenium - comes packaged in /bin/
* firefox - apt-get/aptitude install firefox
* Xvfb - apt-get/aptitude install Xvfb

Remember to run
=====

* ./manage.py tailor_start &
* ./manage.py runserver_plus (or runserver)


Tailor Start Performs these actions
=====

* export DISPLAY=localhost:0.0
* Start Xvfb :0 -screen 0 1280x1024x24
* Start Selenium