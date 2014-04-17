Twitter-Queue-Bot
=================

A Twitter bot that reads and tweets messages in sequence from a queue in a SQLite database.

# Usage

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
