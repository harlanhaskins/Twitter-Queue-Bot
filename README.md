Twitter-Queue-Bot
=================

A Twitter bot that reads and tweets messages in sequence from a queue in a SQLite database.

# Usage

The server requires a few python libraries: `requests`, `peewee`, `twitter`, `argparse`.

There are four main queries to the web api:

| URL            |  Parameters  |     Description                          |           Method                    |
|----------------|--------------|------------------------------------------|-------------------------------------|
| `/add`         |  `content`   | The tweet's content.                     |            POST                     |
| `/all`         |  None        | All of the tweets in the queue.          |            GET                      |
| `/next`        |  None        | The next tweet in the queue.             |            GET                      |
| `/count`       |  None        | The total number of tweets in the queue. |            GET                      |   
