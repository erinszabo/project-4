# UO CS322 - Project 4 #
### Erin Szabo
Fall 2023



### ACP controle times

This project consists of a web application that is based on RUSA's online calculator. The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help.
This project is essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). 

## Application Setup
-  cd into `brevets/` 
-  Build the flask app image using
    ```
    docker build -t some-image-name .
    ```
- Run the container using

  ```
  docker run -d -p 5001:5000 some-image-name
  ```
 - Launch `http://hostname:5001` using your web browser 



## Process Breakdown

* Start by selecting a brevet start date and time
* Next select the brevet length. This is the entire length of the brevet. A brevet can be 200, 300, 400, 600, or 1000 kilometers
* Now you can start entering your controls.
	* controls are like checkpoints along the brevet, so each control should be less than the length of the brevet (or up to 20% past the total brevet distance as the original calculator) and they each should be further from the starting point than the last (the application will still function if you enter them in any other order).
	* you can optionaly enter a location name for each brevet
	* you can enter these distances in either miles or kilometers, the application will automatically update the measure you do not use as it calculates the control's opening and closing times information.

	As controls are entered, their `opening` and `closing` times will be calculated and displayed. These calculations will be explained and illistrated with the table below.
	
The calculation of a control's `opening` time is based on the `maximum` speed. 

Calculation of a control's `closing` time is based on the `minimum` speed.




| Control location (km)      | Minimum Speed (km/hr) | Maximum Speed (km/hr) |    
| ----------- | ----------- | ----------- | 
| 0 - 200     | 15          | 34 | 
| 200 - 400   | 15          | 32 | 
| 400 - 600   | 15          | 30 | 
| 600 - 1000  | 11.428      | 28 | 
| 1000 - 1300 | 13.333      | 26 | 

Both closing and opening times are calculated by dividing the control distance by the associated speed. We start with the speed in the table across from the control location, but for distances larger than 200, it becomes a little more complex. 

When controls are larger than 200km, we break them uo into about 200km pieces. We first take 200 divided by the speed associated with the full distance. Then we add on the same 200 divided by the next speed above it in the table above. We continue with this pattern until we are at either the top of the table (in which case we divide the remainder of the control by the speed at the top of the table) or we have less than 200 of the brevet remaining (in which case we divide the remaining distance by the speed we are currently on). Examples are given at https://rusa.org/pages/acp-brevet-control-ti for further understanding. 



## Original Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
