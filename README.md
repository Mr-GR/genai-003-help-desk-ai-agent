# Getting started help-desk-ai-agent
Install the initial environment

## For Mac open Terminal and run the following 

`pip install numpy pandas matplotlib sickit-learn`

`pip install jupyter`

## To run a jupyter server run the following

`jupyter notebook`

## Run fastAPI Server
First ensure that you have installed the following:
`pip install fastapi`

`pip install uvicorn`

start the server
`uvicorn main:app --reload`

once the server is running go to your browser and enter
`http://1270.0.1:8000`
expected return: hello world

Access FastAPI docs
`http://1270.0.1:8000/docs#`

or 

`http://1270.0.1:8000/redoc`

## Test out fast api 
Get main server
`curl -X GET 'http://1270.0.1:8000'`
expected return: 
<img width="1512" alt="Screenshot 2025-03-29 at 2 57 14 PM" src="https://github.com/user-attachments/assets/0698d64b-1033-4c1e-8477-41bada64fc6e" />

Create an item
make sure to change the item from orange to whatever you would like
`curl -X POST -H "Content-Type: application/json" -d '{"text":"orange"}' 'http://127.0.0.1:8000/items`
expected return: 
<img width="1512" alt="Screenshot 2025-03-29 at 2 55 12 PM" src="https://github.com/user-attachments/assets/f8821e0e-53aa-425c-b467-18b57a3e8f93" />

Get all the items
`curl -X GET 'http://127.0.0.1:8000/items'` 
expected return:
<img width="1512" alt="Screenshot 2025-03-29 at 2 55 42 PM" src="https://github.com/user-attachments/assets/efc29eb7-ce81-461d-9745-7ad2d331f682" />


