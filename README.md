# everything-else-is-public-relations

RSS/Atom feeds for German Newspapers/German Media

## Development

### General

Based on [this template](https://github.com/skorokithakis/django-project-template) and following [this guide](https://www.stavros.io/posts/deploy-django-dokku/) to deploy it with [Dokku](http://dokku.viewdocs.io/dokku/).

### Access docker container

First get the container id

```bash
docker ps
```

then access the container with the id

```bash
docker exec -it f00d7aa42de8 bash
```
