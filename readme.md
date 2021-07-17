**Steps for setting up project**

1. Create a project directory named "assignment"
2. Through terminal go to assignment directory
3. Create virtual environment
   
    `virtualenv -p /usr/bin/python3.8 venv`

4. Activate virtual environment
   
	`source ./venv/bin/activate`

5. Clone project 
   
   `git clone https://github.com/p-smita/geo_django.git`
   
6. Install requirement
   
	`pip install -r requirement.txt`
 
7. Install migrations
   
	`python manage.py migrate`

8. Runserver to test

	`python manage.py runserver`

9. Load Station data

	`<domain>/load_spatial_data`

10. Load Spatial points
	
	`<domain>/load_spatial_points`

11. Load weather forecast data
	
	`<domain>/get_forecast`

12. Check forecast on map

	`<domain>`
 