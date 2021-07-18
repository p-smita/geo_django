**Steps for setting up project**

1. Create virtual environment
   
    `virtualenv -p /usr/bin/python3.8 venv`

2. Activate virtual environment
   
	`source ./venv/bin/activate`

3. Clone project 
   
   `git clone https://github.com/p-smita/geo_django.git`
   
4. Install requirement
   
	`pip install -r requirement.txt`
 
5. Install migrations
   
	`python manage.py migrate`

6. Runserver to test

	`python manage.py runserver`

7. Load Station data

	`<domain>/load_spatial_data`

8. Load Spatial points
	
	`<domain>/load_spatial_points`

9. Load weather forecast data
	
	`<domain>/get_forecast`

10. Check forecast on map

	`<domain>`
 