Possible steps convert it to a fully
featured web application:

- instead of the command line tool, I would turn this to a rest/json micro-service, using (if Python) something like Flask, FastAPI or Django Rest Framework. to be consumable by Web apps and/or mobile apps.
- since the truck list unlikely to change frequently, to minimize the load on external Api (Socrata) I would probably implement some server side caching (e.g. in Redis) and/or adding caching http headers in the Web app.
- I would serve the content over the https instead of the default http.
- I would probably pack everything into a Docker container, for ease of deployment.
- since the real world use requires storing secrets (Socrata Api key), I would provide the key through the environment variable as sufficiently secure way.
- Depending on the scale requirements, I would consider running multiple instances of the app behind the load balancer (or Kubernetes service) Multiple instances could share same Redis cache.
- if the json documents returned by the external Api would be large, I would consider streaming json processing
