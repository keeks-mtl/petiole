# Petiole

## Goal For This Project

Petiole is a place for plant lovers to unite. Creating a safe haven to share their plant 
babies and see other beautiful and rare plants that others have collected. An opportunity
to see how other people feel about different plants and get inspiration to expand your 
plant collection. 

## Table of Contents


## UX

### User Goals

- Search plants
- Registration to join the community
- A website that caters to desktop, tablet & mobile
- Visually appealling elements that catch your eye
- Find information on different plants

### User Stories

- As a user, I want a clear & easy way to register and join.
- As a user, I want to see which plants are popular.
- As a user, I want to find out more about Petiole on social media. 
- As a user, I want to discover & search plants.
- As a user, I want to look for a plant with a specific characteristic.
- As a user, I want to easily log in with my username and password.
- As a user, I want to be able to add my plants to the website.
- As a user, I want to be able to "like" a specific plant.
- As a user, I want to be able to edit a plant post.
- As a user, I want to be able to delete plants i've posted. 
** admin **


### Site Owners Goals

- As the site owner,
- As the site owner,
- As the site owner,
- As the site owner,
- As the site owner, 

### wireframes

- [Wireframes](): A plant directory and social plant site.

The initial wireframes and the current project differ in some minor ways:

- ...

### Design Choices

- I attempted to create a website that felt light, fun and not too rigid.
- The colour choices were centered around [colorspace](https://mycolor.space/) to 
find the complementary colour palettes that worked well.

### Fonts

- The goal was to have a crisp and modern feel with a bit of punch. 
- The the Titles and the Branding, [Google Fonts](https://fonts.google.com/) Pacifico 
    was chosen to an eye-appealling look that stood out from the rest of the information
    on the page.
- The title font was paired with a crisp and readible font "Monserrat"

### Icons

- Pretiole takes advantage of iconography by utilizing icons from [Font Awesome](www.fontawesome.com)
- Many of the buttons use icons to give a clear visual cue as to solidify what they do. 
- The icons made the content more concise and didn't distract from the information.
- The icon seen most is the hamburger icon that will make navigation more simple on mobile devices.
- Social media icons are also used to give clear indication of how to follow Pretiole on social media.
- The logo and favicon was chosen for it's simple representation of one of the most popular houseplant. 

### Colours

- The colour theme included five main colours that complimented one another.
- The colours were chosen because of their contrast and the way they can be associated with plants.
- Buttons were also color coded in a way that intrinsically implied what they accomplished. A soft red/pink
    to cancel or delete and a green to add/go forward. 

## Features

- Responsive on all device sizes
  - Including a change in layout across different breakpoints.
- Interactive elements
  - Including: buttons, links, dropdown menus, and forms.

### Navigation

- The navigation bar was created using Bootstrap to ensure that it was fully responsive.
- An example of the change with responsiveness includes a hamburger menu when viewed on smaller viewports.
- The navigation bar shows Plants, Search, Login, and Register when a user is not logged in and when a user
    is logged in it shows Plants, Add Plant, Profile, Search, and Logout. 

### Plant Cards

- There are multiple cards across the site to include information about the plants themselves.
- They are clear organised to be easily read and understood.
- If a user is logged in and they created the plant card, they have the ability to edit or delete the card.
- The plant name is also a link the the plant page where you can see the information clearly and like the plant 
    as well. 

### Pagination

- The feature is used to make sure pages aren't filled with plant cards slowing down users viewing. 
- Each page displays 12 plant cards and displays the cards on serveral pages. 

### Home/Plants Page

- Displays plants sorted by their popularity or "Likes"

### Register

- The registration page allows users to register to use all of Pretiole's features.
- The registration form requires all of the following information to create an account:
    - User's first name 
    - User's last name
    - User's email
    - User's username
    - User's password
- All the data is then stored in a "users" collection on MongoDB database.
- The passwords are hashed 

### Log In

- Returning users who have already registered can use the log in form to 
    access Pretiole and their account. 
- The form requires a username and password which is then checked against their
    credentials stored in the database. 

### Profile Page

- The profile page allows users to see the plants that user has created. 
- On the page the user has the ability to sort their plants by either the plant's latin name
    or the plant's common name. 
- The Profile page shows the user's username and users also have the ability to click on the 
    "Add Plant" button to add to their collection. 

### Add Plant Page

- The add plant page allows a user to submit a form to create a plant card with the following inputs:
    - Latin Name (text field)
    - Common Name (text field)
    - Image URL (text field)
    - Lighting (radio options)
    - Watering (radio options)
    - Grow Speed (radio options)
    - Care (radio options)
    - Suitable for (checkboxes)
    - Toxic (toggle option)
    - Humidity (toggle option)
- if the image url is broken or invalid a default image will be added the card.
- The form makes sure all fields other than suitable for are valid and before users 
    can click "Add Plant" button. Once the button is clicked the user's are redirected
    to their Profile Page and a flash message appears telling them they've added their plant.
- User's can access the field through the navigation bar or their profile and the route is protected
    so user's not logged in can not access the feature. 

### Edit Plant 

- The edit plant feature allows user's to edit the information on the plant and update the card with 
    the new information.
- Only the user who created the plant (and logged in) can use the edit plant form to update the information. 
- The form has all the information that was submitted when creating the form prepopulated allowing the user 
    to see what was submitted and change anything they'd like.
- Once the user has clicked the "Edit Plant" button they are redirected to their profile page and are shown 
    a flash message letting them know the plant was editted. 
- The edit plant feature can be accessed through the plant card to only the user who created it on the following 
    pages:
    - plants.HTML
    - profile.HTML
    - search.HTML
    - plant.html (through the plant's specific id)

### Delete Plant

- a user can only use the delete plant function when they are logged in and they
    created the plant card. 
- When the "Delete" button is clicked a modal pops up asking for confirmation that the 
    user would like to delete the plant to prevent plants from accidentally being deleted.
- If the user clicks delete on the modal then the plant is deleted forever from Pretiole and the
    database. 
- The delete functionality can be accessed through the plant cards on the following pages:
    - Plants.html
    - Profile.html
    - Search.html
    - plant.html (through the plant's specific id)

### Plant Page

- Main page where plant cards are sorted by their popularity which is decided
    by how many "likes" a plant has. 
- Everyone has access to this page and is easily navigatable. 

### Like Plant

- A user has the ability to use the like feature only when logged in.
- A user can only like a plant once. 
- When clicked, the plant page reloads and adds the a like to the count. 
- The "likes" are used to order the plants on the main plant page. 


### Search

- Ability to search for specific plants by either their latin or common name. 
- Also have the ability to search for popular plant characterizations such as:
    - What lighting it requires
    - How much care it requires
    - Whether it is toxic/animal safe

### Log out

- The log out functionaly is located on the navigational bar and allows users 
    the ability to log out when clicked.
- The user when logged out is redirected to the log in page with a flash message
    that informs them they have been logged out. 

### Features Left to Implement

- Comment section for registered users to discuss the plants and share tips.
- Private messaging abilities for members to message other members to share information
    privately.
- Abiltiy to undo a "like"
- Afiliate links to plant shops so users can buy plants they've seen.
- Share plant ability (share plant card through social media)
- To check in realtime on register form if the username already exists. 

## Technologies Used

### Languages

- HTML5
  - The base of the code for the overall structure of the site.
- CSS3
  - For the styling of the site
- Javascript
    - ...
- Python
    - ...

### Libraries, Frameworks & Tools

- [Font Awesome](https://fontawesome.com/)
  - For the icons used as social media links
- [Bootstrap](https://getbootstrap.com/)
  - Was used for added styling and responsiveness of the project
- [Google Fonts](https://fonts.google.com/)
  - Used to import the main font for the styling of the project
- [Github](https://github.com/)
  - Used to store and push the code
- [Visual Studio Code](https://code.visualstudio.com/)
  - used to code and push the code
- [Google Developer Tools](https://developers.google.com/web/tools/chrome-devtools)
  - Used to debug code and show styling changes before changing the actual code
- [Balsamiq](https://balsamiq.com/)
  - Used for creating the wireframes in the planning stage
- [W3C HTML Validator](https://validator.w3.org/)
  - Used as a HTML validator
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
  - Used as a CSS validator
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - ...
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
- [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
- [MongoDB](https://www.mongodb.com/1)
- [Heroku](https://id.heroku.com/login)
- [Github](https://github.com/)

## Testing

Testing information can be found in this file : [testing.md](testing.md)

## Deployment

### Local Deployment
#### Requirements

- An IDE (such as Gitpod or Visual Studio Code)
- Python3
- PIP3
- MongoDB 

#### Instructions

- Open your IDE and in your terminal and clone the git repository with the following command.
    - git clone https://github.com/keeks-mtl/petiole
- Create environment file called "env.py" and add :
    - MONGO_URI= mongodb+srv:// (and link to your database)
    - SECRET_KEY= <your secret key>
- Add your env.py to your .gitignore. so it's not uploaded to github at any point.
- Upgrade pip locally with the command:
    - "pip install -U pip"
- Install the modules used to run the application using in your terminal:
    - "pip freeze > requirements.txt"
- In app.py, switch debug=False to debug=True
- Create a MongoDB account and create a database called "petiole"
- Create the following collections:
users
```
_id:<ObjectId>
first_name:<string>
last_name:<string>
email:<string>
username:<string>
password:<string>
liked_plant:<Array>
```
plants
```
_id:<ObjectId>
plant_latin_name:<string>
plant_common_name:<string>
plant_image:<string>
lighting:<string>
watering:<string>
grow_speed:<string>
care:<string>
suitable_for:<Array>
toxic:<string>
humidity:<string>
created_by:<string>
plant_like:<Decimal128>
```
- you can now run the application with the command
```
python3 app.py
```
- you can visit the website now at 
```
http://127.0.0.1:5000
```

### Heroku Deployment

- create a requirements.txt file using the terminal command
```
pip freeze > requirements.txt
```
- Create a Procfile with the terminal command 
```
echo web: python app.py > Procfile
```
- 'git add' and 'git commit' the new requirements and Procfile and then 'git push'
    to GitHub
- Create an account on [Heroku](https://www.heroku.com/home)
- Create a new app on Heroku by clicking the "New" button in your dashboard and then 'Create New App'.
- Give the app an unique name and set the region.
- In the dashboard for your new app, click on "Deploy" > "Deployment method" and select GitHub
- Confirm the linking of the Heroku app to the correct GitHub repository.
- In the heroku dashboard for the app, click on 'Settings' > 'Reveal Config Vars'
- Set the following config vars:
```
IP = 0.0.0.0
MONGO_DBNAME = petiole
MONGO_URI = `mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority`
PORT = 5000 
SECRET_KEY = `<your_secret_key>`
```
- in the Heroku dashboard, click "Deploy"
- Make sure master branch is selected and then click "Deploy Branch"

## Credits

### Content - Media -Inspiration

I have used the following websites to get info & images for my website.

#### Images
- [Pixabay](https://pixabay.com/)
  - Illustrative of monstera leaf for logo & illustration for 404 page
- [Unsplash](https://unsplash.com/)
  - Stock images for cards
- [Pexels](https://www.pexels.com/)
  - Stock images for cards

#### information
- [Patch Plants](https://www.patchplants.com/gb/en/)
- [The Sill](https://www.thesill.com/)

#### Code
- [Scalegrid](https://scalegrid.io/blog/fast-paging-with-mongodb/)
    - How to add pagination
- [Code-Maven](https://code-maven.com/flask-return-404)
    - 404 error handler
- [Pythonise](https://pythonise.com/series/learning-flask/flask-session-object)
    - fix check if logged in to access page (add_plant)
- [Themeisle](https://themeisle.com/blog/missing-images-on-website/)
    - How to handle broken images
- [StackOverflow](https://stackoverflow.com/questions/61829373/passing-data-to-a-bootstrap-modal-in-jinja-template-one-of-them-from-inside-a-f)
    - Confirm delete modal
- [Flask](https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/)
    - How to add favicon

- [HTML.com](https://html.com/attributes/input-pattern/#:~:text=A%20regular%20expression%20is%20a,numerals%20(%200%2D9%20).)
    - pattern attribute for inputs
-[](https://stackoverflow.com/questions/47329938/block-form-submit-if-no-one-checkbox-checked)
    - jquery for checkboxes

### Acknowledgements

- A special thank you to my mentor Antonija Simic for her help in going through my project thoroughly and guiding me through what 
    is expected of my website and how to clean up my code.
- The Code Institute Slack community for their technical support.

## Disclaimer
This website is for educational purposes only. 
