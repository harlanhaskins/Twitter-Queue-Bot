Twitter-Queue-Bot
=================

A Twitter bot that reads and tweets messages in sequence from a queue in a SQLite database.

# Usage

## Backend (API)

#### Dependencies

Install using 

```
pip install -r requirements.txt
```

#### Setup

To start the server, just run `backend/webapi.py`. The service will be exposed on port 4200. You can access the API at "http://yourwebsite.com:4200".

To automatically pull tweets from the queue, run `backend/tweet.py` in a cronjob. This will pop the first tweet off of the queue, tweet it using the credentials specified in `backend/credentials.json`, and delete it from the queue if the tweet was posted successfully.

The credentials JSON file should look something like this:

```json
{
	"consumer_secret": "",
	"consumer_key": "",
	"access_key":"",
	"access_secret":""
}
```

Be sure to add in your own info!

#### API Methods

These are the valid queries to the web API:

| URL            |  Parameters |     Description                                |            Method              |
|----------------|-------------|------------------------------------------------|--------------------------------|
| `/add`         |  `content`  | Adds a new tweet to the queue.                 |       POST                     |
| `/move`        |  `id`       | Moves the provided ID to the top of the queue. |       POST                     |
| `/all`         |  None       | All of the tweets in the queue.                |       GET                      |
| `/next`        |  None       | The next tweet in the queue.                   |       GET                      |
| `/count`       |  None       | The total number of tweets in the queue.       |       GET                      |  
| `/remove`      |  `id`       | Removes the provided ID from the database      |       DELETE                   |   

## Frontend (Admin Panel)

We've included a basic interface for adding and managing your tweet queue. Just set a few config vars in `frontend/assets/js/app.js` and you're good to go:

```javascript
/*
*   UPDATE THIS WITH YOUR INFO!
*   base_url = Base url for the API
*   title = The name you want for the admin panel
*   twitter = The Twitter username for the queue (without the "@")
*/
var config = {
    base_url: "",
    title: "Twitter Queue",
    twitter: ""
}
```
