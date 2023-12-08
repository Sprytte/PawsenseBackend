# PawsenseBackend - ABSTRACT
Our project “Pawsense” focuses on examining the relationship between pets and their eating habits by monitoring both the pet’s weight as well as their amount of food fed to them through IoT devices. We incorporated a weight sensor and set it up on a plank where the pet would first walk on it, which will register its weight, then will do the same thing for the food bowl weight. We created a website for our project which contained the login page, home page, and pet details page. Via the homepage, you can access all of your pets that are saved in your database, as well as an overview of their information. You can then choose to view more details about the pet which will navigate you to a page where there are more details to look at such as the graph specific to that pet. The graph shows the food weight for that specific pet throughout the day by showing the time and weight (data gotten from the sensors and then saved to the database). Our database holds the data for our pets (name, weight, type), food bowl (petId, weight, time), users (username, password). The backend using Flask contains the endpoints that will be accessed by the frontend (ReactJs) to display the data.