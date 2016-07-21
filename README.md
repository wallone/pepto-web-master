

# Developer setup

The following are directions for running the application using Python3.5 on a Mac.
Install virtualenv to create the flask python environment to install all the files.

		pip3 install virtualenv

You may need to use sudo to install virtualenv on your system. While inside the project folder, run the create the virtual environment, activate the environment, and install the appropriate packages.

		virtualenv -p /usr/local/bin/python3.5 env
		source env/bin/activate
		pip3 install -r requirements.txt

If using Ubuntu linux, the first line can be replaced with the following `virtualenv -p /usr/bin/python3 env`.

Now you should have all the prerequisites installed so you can run the applications.
When you want to exit the environment simply type `deactivate`.
Before leaving the environment, if you install any new python packages you can save
the arrangement by freezing the packages to requirement.txt file before you deactivate.
The command to perform this is `pip3 freeze > requirements.txt`. 

On the command line, `python3 run.py`. Runs the application. Pay attention to
the output to record the URL and port number. (It is likely
http://localhost:5000).

You can now open a browser and and go to the two applications.

### The Twitter Survey
    http://localhost:5000/twsurvey

### Tweet labeler
    http://localhost:5000/labeler


# Flask Tutorial gives a introduction to a typical project setup
http://exploreflask.readthedocs.io/



