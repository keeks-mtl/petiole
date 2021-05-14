# Petiole - Testing

[Main README.md file](README.md)

[View website on Heroku](petiole-plants.herokuapp.com/)

## Table of Contents

## Automated Testing
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) & [W3C HTML Validator](https://validator.w3.org/)
  - Were used to validate the CSS & HTML code respectively.
- [W3C HTML Validator](https://validator.w3.org/)
- [JSHint](https://jshint.com/)

### Navigation bar

1. Plan

   - On every page, every link should take you to where you are supposed to go
   - On mobile devices the navbar should turn to hamburger so it's visible and the drop-down menu should appear so navigational elements can be chosen

2. Implementation

   - The navbar was created using Bootstrap so that it was fully responsive
   - In the mobile implementation the Popfit header is hidden as a link

3. Test

   - Clicked on every link on every page & checked every page on different breakpoints to ensure responsiveness

4. Verdict
   - 

### Modals

1. Plan
   - Wanted a modal to pop up to choose a buying option for quick decision making to convert sales
2. Implementation
   - ...
3. Test
   - ...
4. Verdict

### Registration Form
1. Plan
- 
2. Implementation
- 
3. Test
- 
4. Verdict
- 


## Bugs

### Add_plant Bug

#### Bug
- When you click to add plant it just redirects to an empty add_plant page
#### Fix
- Change the code to check if user is logged in

### New User Like BUg
-   add_plant suddenly stopped working
#### Bug
- New users can't like plants
#### Fix
- Add liked_plant array to user when registering.
