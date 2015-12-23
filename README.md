# Hyozan

An "Object storage" like application which uses Backblaze B2 for archival. Originally intended for screenshot uploads via ShareX, but it will probably support other files as well.

Named after the Japanese word 氷山 (Hyōzan), meaning iceberg. Referencing how most of it is hidden underwater.

# The goal of this project

Bandwidth is overpriced. Really overpriced.

Don't get me wrong. B2's $0.05/GB is perfectly reasonable compared to all the others like S3 and Google Cloud. In fact, it's pretty good.

Problem is that they're **all** overpriced. Storage is cheap, but never use these services for bandwidth alone.

Why pay over $50 per TB of bandwidth when you can just install this on a VPS from a host like DigitalOcean that will give you the same for $5?

# What it does

When you upload a file to Hyozan, it forwards it to B2. When users then try to access it later, Hyozan will first check if it has a local copy. If it does not, it will fetch the file from B2 and keep it for a while.

This will decrease both the bandwidth and transaction (request) costs that come with object storage services.

## In technical terms

Hyozan is an Object storage oriented API-only (for now) reverse proxy, designed to cache, manage, adding and hopefully deleting static files from a 3rd party object storage service while lowering your total bandwidth consumption from these services, in this case B2. Due to the code structure, rewriting it for something like S3 should not be too hard.

# Why?

Instead of paying $50 for 1 TB of B2 bandwidth. Let us assume that you have a DO droplet running Hyozan. If it cached 90% of your traffic. **That means you only pay about $5 for B2 bandwidth and $5 for your droplet. That's a total of just $10. A measly fifth of the regular cost**

And this does not even consider transaction costs, which can be high if you serve a lot of smaller files.

# Requirements

* Python 3 (Python 2 might work, dunno, i don't test that, don't care either)
* Install flask, currently that should be the only requirement and hopefully forever (``pip install -r requirements.txt``)

# Using the thing

* Clone the repo somewhere
* Do ``cp conf.py.sample conf.py``
* Edit ``conf.py`` so that the information is correct
* If possible, make it listen on ``127.0.0.1`` and then use something like nginx as a reverse proxy. For security purposes
* ``chmod +x run.py`` and then ``./run.py``
* ???
* PROFIT (Hopefully)