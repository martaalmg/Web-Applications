100451724-Marta Balairón García
100451979-Marta Almagro Fuello

WITHOUT BEING LOGGED IN:
* Main page:
	- ADDITIONAL: Image slider (basis.html)
	- Side bar (basis.html) with links to the different pages of our web page
	- Login botton, inside this template we can find the option of sing up (auth folder templates)
	- ADDITIONAL: Search bar for looking up for animals. If the animal exists, the web gets redirected to the animal template (animal_template.html) 
	  if not, it gets redirected to the home page.
* Animal catalog (catalog.html):
	- All the animals are displayed with their picture and a botton to access to the animal view (animal_catalog_template.html). 
	  When we click on this botton, it redirects to the animal template (animal_template.html)
	- ADDITIONAL: In this view we can observe the relationship with the events where we can find this animal. When clicking on it, 
        it redirects to the event template (event_template.html)
	- ADDITIONAL: filter tool, the user can select just some characteristic related to the zone and the animal tool. When clicking the botton, just the animals 
	  which satisfy those conditions are shown.
* Events catalog (event_catalog.html):
	- All the events are displayed with a botton to access to the event view (event_catalog_template.html). 
	  When we click on this botton, it redirects to the event template (event_template.html).
	- ADDITIONAL: in addition to the requiered functionality, users are noticed that they cannot do reservations unless they login.
	- ADDITIONAL: in side the event view, on the one hand, users can see a message if the event is not sheduled and 
	  on the other hand, if it is sheduled, they can see the future dates (scheduled_template_present.html) and past dates (scheduled_past_template.html)
* ADDITIONAL Zoo Map (map.html)
	- In this view, we inser an image and an icon for each animal. Working with the coordinates, we locate each object and when clicking on it, 
	  it reedirects to the correspondant animal view (animal_template.html)

BEING LOGGED IN AS USER:
* Main page:
	- ADDITIONAL: Image slider (basis.html)
	- Side bar (basis.html) with links to the different pages of our web page
	- Logout botton (auth folder templates)
	- Costumer view botton, it redirects to the costumer view template (costumer_template.html)
	- ADDITIONAL: Search bar for looking up for animals. If the animal exists, the web gets redirected to the animal template (animal_template.html) 
	  if not, it gets redirected to the home page.
* Costumer view:
	- ADDITIONAL: We can find some bottons which will redirect to the events catalog template (event_catalog.html) and 
        to a page where the reservations can be cancelled (edit_reservations_template.html)
	* ADDITIONAL: Edit reservations template (edit_reservations_template.html)
		- Here users can see all their resrvations (options_reservation.html)
		- Here authenticated users can cancell the reservations by clicking on a botton. When doing this, the number of places get updated.
		- If you dont have any reservation, a message notices you.
	- User can see the future reservations and the past reservations with the requiered asspects about them (user_reservation_template.html)_reservation.html).
	- ADDITIONAL: If there is not reservations a message is shown.
* Animal catalog (catalog.html):
	- Same as not logged in.
* Events catalog (event_catalog.html):
	- All the events are displayed with a botton to access to the event view (event_catalog_template.html). 
	  When we click on this botton, it redirects to the event template (event_template.html).
	- ADDITIONAL: in side the event view, on the one hand, users can see a message if the event is not sheduled and 
	  on the other hand, if it is sheduled, they can see the future dates (scheduled_template_present.html) and past dates (scheduled_past_template.html)
	- Users can find a botton to perform a reservations which redirects to the reservation template (reservation_template.html)
	  ADDITIONAL: Users can go back with a botton which redirects to the event template (event_templated.html)
* ADDITIONAL Zoo Map (map.html)
	- Same as not logged in.

BEING LOGGED IN AS MANAGER:
* Main page:
	- ADDITIONAL: Image slider (basis.html)
	- Side bar (basis.html) with links to the different pages of our web page
	- Logout botton (auth folder templates)
	- Manager view botton, it redirects to the manager view template (manager_template.html)
	- ADDITIONAL: Search bar for looking up for animals. If the animal exists, the web gets redirected to the animal template (animal_template.html) 
	  if not, it gets redirected to the home page.
* Manager view (manager_template.html):
	- In this view we can see three different bottons which redirect to three different fuctions.
	- Modify feautured and not featured (event_featured.html). At this template we can observe each of the events (event_featured_template.html) 
	  with a botton that allows the manager to change an event from featured to not featured and viceverse.
	  Moreover, the manager also can add a newe date for an activity already created.
	- ADDITIONAL: Adding animals (add_animal.html) at this template we can observe all the current animlas as well as a form tu add new ones. 
	  In case the manager tries to insert an existing animal, an error message is shown.
	- Adding activities (add_activity.html) at this template we can observe all the current events as well as a form tu add new ones. 
	  In case the manager tries to insert an existing activity, an error message is shown.
* Animal catalog (catalog.html):
	- Same as not logged in.
* Events catalog (event_catalog.html):
	- Same as logged in as a user
* ADDITIONAL Zoo Map (map.html)
	- Same as not logged in.
