# Parkify
## The Application

### A world in constant motion

We live in a world where being able to do things faster has become a necessity to the point where even five minutes can feel like an eternity; this couple with the fact that finding a parking space is more difficult everyday due to the constant increase of traffic makes this tedious process take longer than what the world around us demands. With no way to be able to explore the entirety of a parking lot we begin to lose time that although it doesn’t seem a lot at the moment (normally not more than a couple minutes), it starts to add up costing us not only time, but gas as well in an activity which should be simpler.

### What is Parkify?

Parkify is an application that aims to solve this parking problem so you are able to find a spot to park your car in a more efficient and effective way than by searching driving around. It is a simple solution which manages to separate a parking lot in different areas and tells you how many spaces are free in each of this areas. This way, looking for a parking spot can stop being a chore and become an easy step throughout the day.

### How Parkify is achieved

This application was built from the ground up by utilizing an Intel Edison Board and simulating a parking environment with the use of sensors to mark the entry and exit of cars in an area, a database stored in a web server as well as a communication with the application through the use of .json files. To put it simply, we have an application which communicates utilizing a ssh protocol to the Edison and to a database, whenever an entry or exit sensor is triggered, the the app will change accordingly.
## Hardware and software
### Intel Edison
The Intel Edison board will be utilizing a button to count a car occupying a new space, a touch sensor to represent a car leaving a free space, and an LCD screen which lists the number of free parking spots and changes color between green, yellow, and red depending on this number, with green being more than half parking spaces available, yellow being half or less spaces available, and red when there is no availability left; The updates can only be received from the sensors after an interval of 0.05 seconds. The whole development for the Edison can be found in this link.

 https://github.com/dtoledo23/development_card/blob/master/firstFunctional.py

#### Image Recognition
The implementation of the use of a camera to be able to detect license plates to identify the cars entering the parking lot area is still in progress. It will capture video constantly and will take a picture whenever a license plate enters its field of view and then it will save the image and restart the camera so it is ready to detect another plate. Though this implementation isn’t complete yet, a rough version of the code is found here:

https://github.com/dtoledo23/development_card/blob/master/cameraTest.py
### Web service
Also included within the Intel Edison, we will be using its IP address to host a web server which will be used to display the main webpage of Parkify made utilizing a Materialize template as well as giving you the option to create your own parking space for the use of the application. The css and necessary scripts for it to run correctly can be found here as well as the server:

 https://github.com/iotchallenge2016/development_card/blob/950f8b029e6447204472b0a2a5b5659d0c9766be/static/js/init.js

https://github.com/iotchallenge2016/development_card/blob/950f8b029e6447204472b0a2a5b5659d0c9766be/static/css/main.css

https://github.com/iotchallenge2016/development_card/blob/950f8b029e6447204472b0a2a5b5659d0c9766be/server.py

The server will not only manage the webpage, but it also be in charge of reading the initial state of the areas of the parking lot through a csv file through a loader py file, then we have a another py file that makes requests to the server and writes into the lcd of the Edison with the use of its sensors, and finally we have another file which states when a request is invalid.

https://github.com/iotchallenge2016/development_card/blob/950f8b029e6447204472b0a2a5b5659d0c9766be/invalid_request.py

https://github.com/iotchallenge2016/development_card/blob/950f8b029e6447204472b0a2a5b5659d0c9766be/loader.py

https://github.com/iotchallenge2016/Parking-lot/blob/55d001aade8c4c797b8b5044747d22ce86add645/requests_to_server.py

## Resources
Python sensor libraries:

https://github.com/intel-iot-devkit/upm/tree/master/examples/python


git branches:

https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging


IOT internet of things:ss

https://www.gitbook.com/book/theiotlearninginitiative/internetofthings101/details
