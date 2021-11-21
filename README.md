# Inspiration
After looking online most solar calculators for existing homes are outrageously complicated and time-consuming. This does not fit the possibilities of extracting all the demanded information from high-quality satellite images. To reduce the hurdles for possible homeowners to get a quote the only thing that should be of interest is the address. 

# What it does
We take that address of a house and detect the corresponding roof and the available area on it to then give the homeowner an estimation on how much money and CO2 they might be able to save by going solar. 

![](/images/Website.png)

# Starting the React App / Webserver

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
To set the website up the first time, go to the root repository in a command prompt or anaconda prompt and run 

`npm install`

# Launching the python server

Install flask and flask_cors by running 

`pip install flask
pip install flask_cors`

Open a command promt or anaconda prompt and go to the folder [python_backend](/python_backend) in it. The first time, set the environment variable for flask:

`set FLASK_APP=FlaskServer`

To start the flask server, run 

`flask run`

## Start the Server
Open a command prompt or anaconda prompt, go to the root of the project and call

`npm start`

This should lead to the following output:

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

# Note
This project has been established during the virtual 2 day hackathon Hackatum from 19th to 21st November 2021. The project works as intended for some houses with flaat roofs, but might fail for others and can't take tilt of the roof into account.
