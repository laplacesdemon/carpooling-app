==============
Carpooling App
==============

This is a project that I started with a friend, than in a week we changed our mind and abandon the project. Here is the work so far, and I am willing to continue as an open source project if there's anyone to help me. 

Take a look at `design` folder and my initial class diagram. Rest api is implemented as well. 

What is the App
===============

Carpooling app will be a mobile app to share rides with fellow drivers. 

App Pages
=========

Application consists of following pages

 * [[Request a ride]]
 * [[Select a ride]]
 * [[Create a ride]]
 * [[Ride Details]]
 * [[My rides]]
 * [[User profile]]
 * [[Notifications]]
 * [[Accept/Reject a ride request]]

In addition, there are some simple pages as follows:

 * Help
 * About Us
 * [[Contact Us]]

Rest API
========

The REST api is the data endpoint of mobile apps.

GET Rides Service
-----------------

Returns ride objects for specified parameters. If no parameter is passed, returns all rides with pagination.

A ride object is a brief description of the ride. If you want to see details of it, use [[Ride Detail Service]]

**Endpoint**

/api/rides

**Parameters**

Name|Description|Example
----|-----------|-------
start_latitude|Latitude coordinates for the start location (in decimals)|42.3434
start_longitude|Longitude coordinates for the start location (in decimals)|42.3434
start_radius|Radius of the start location's circle (in meters)|1000
end_latitude|Latitude coordinates for the destination (in decimals)|42.3434
end_longitude|Longitude coordinates for the destination location (in decimals)|42.3434
end_radius|Radius of the destination location's circle (in meters)|1000
date|The date and time of the ride.|2013-12-25T14:53:05Z
until|Optional date to fetch results until specified date.|2013-12-25T14:53:05Z

**Example Response**

		[
		    {
		        "pk": 1, 
		        "route": {
		            "start_address": "Hac\u0131 \u015e\u00fckr\u00fc Sk 1-19, Kadikoy, Turkey", 
		            "end_address": "Cicek Pasaji, Beyoglu, Turkey"
		        }, 
		        "driver": {
		            "url": "/api/users/2/", 
		            "username": "ahmet", 
		            "public_name": "Ahmet K."
		        }, 
		        "vehicle": {
		            "url": "/api/vehicles/1/", 
		            "brand": "BMW", 
		            "model": "3.16i", 
		            "year": 2001, 
		            "seat_capacity": 3
		        }, 
		        "registered_seats": "0/2", 
		        "price": 40, 
		        "date": "2013-12-25T13:32:05Z"
		    }
		]