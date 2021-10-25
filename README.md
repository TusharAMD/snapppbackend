# Snappp (Meme Maker)

In this project I have created a meme making web app using React js for frontend and flask for backend. It also has a standalone progressive web app that is used to take snap shots or photos from mobile camera of real objects and send it to the Meme Canvas.

Note: This whole project is divided into 3 repositories, frontend,backend and for pwa. Links are available here
- Frontend: https://github.com/TusharAMD/Snappp_frontend
- Backend: https://github.com/TusharAMD/snapppbackend
- PWA: https://github.com/TusharAMD/Snappp_pwa

## Live Links
https://snapppfrontend.herokuapp.com/

## Features
In this web app user can make his/her own meme similar to http://imgflip.com/. Following are some of the important features
- Add gifs from "Tenor" api to your meme
- Facility to add own images using pwa in your phone and background is magically removed (similar to https://www.remove.bg/)
- Add your text to the canvas and also chnage color randomly
- "Bring forward" feature on the objects so that transparent objects can stay on top
- Authentication system
- Save meme and see a list of your collection in profile section.
- View someone else's collection by email id
- Like others meme

## Working
- First of let us see gif part. I have used Tenor api to grab the gif according to text and number of images user wants (query)
This is operated in backend and React requests the data using axios. (In this project I have used axios to perform all requests at end point of my Backend)
- Then on clicking get images the image is displayed on the canvas.
- The canvas is basically a div element and in that all the elements are resizeable and draggable. This is acheived by react and it gives use the actual freedom to make a meme
- By clicking on save button the user can save the div element as SVG image and that image data is send to backend and stored in database with user details
- Throughout the project I have used mongodb for database and in total I have used 3 Tables 
- The user data is well organised and user can easily retrieve the data
- The authentication is made using Auth0 and its carried out in frontend.
- Now another important feature is giving user the ability to upload his/her own images. For this I have made a Progressive Web App that can be installed on mobile phone
- This PWA is not deployed due to heroku slug size issue in free tier. So we can simply run the flask file using python and then visit the website using any mobile device
- Then Click add to homepage. Open the app and enter email id and also click photo using your mobile camera.
- This process takes some time to remove the background and then a done message will be displayed
- After that user can click get snap to get the "background removed pic" and its ready to use in the web app

## Tech Stack Used
- React
- Flask
- REST APIs
- MongoDB
- Flask PWA 
- Auth0

## Made By
Tushar Amdoskar
https://www.linkedin.com/in/tushar-amdoskar/
