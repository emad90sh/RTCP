# RealTime Cryptocurrencies Price (RTCP)


## Description:

Files in `Service` directory, get data from **Kucoin** broker by using `public websocket channel`, and store prices in database. **(These files should run as a service)**

Files in `Server` directory, create a get endpoint on `/` to render `index.html` and a `/price` for update prices in webpage.

Endpoints are managed by `FastAPI`.

Update Interval is 1 second.

<br>

## Requirements:

- **Python3**

- **Redis**

- **Nginx**

<br>

## This Script tested on:

- **Ubuntu 20.04 LTS**

- **Python 3.8.10**

- **Nginx 1.18.0**

- **Redis 5.0.7**


