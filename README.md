Twitter-Queue-Bot
=================

A Twitter bot that reads and tweets messages in sequence from a queue in a SQLite database.

# Usage

## Backend (API)

The server requires a few python libraries: `flask`, `peewee`, `twitter`, `argparse`.

All of these are installable through `pip`.

These are the valid queries to the web api:

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