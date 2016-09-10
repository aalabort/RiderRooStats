(Project under construction, not finished yet)
============

#RiderRooStats:

App Impemented with Kivy and Python to provide instant information to Deliveroo Riders about their earnings and statistics about their deliveries. 

For the moment it consist of 2 parts:
* Algorithm to read the gmail of the courier to be able to scrape it and extract the useful data from
the mails sent by Deliveroo.
* Kivy App


The first part is ready, the algorithm works properly and print the results in the cmd.
The Kivy App is not finished, an initial layout is done but it remains to bind all the buttons with
the outputs of the mail reading algorithm and display the results.

#Installation:

This app was made utilizing the kivy library. Please refer to kivy.org for its installation. Additionally, the app requires navigationdrawer and graph from the kivy-garden in order to run. The buildozer tool can be used to build the app.
