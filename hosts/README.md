# hosts
> Automatically update container ip to /etc/hosts base on container name

## Getting start

Start a new container passing your local `docker.sock` file

```bash
docker run -d --name hosts \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc/hosts:/etc/hosts-host hackerliang/hosts
```

This is a modified version of https://github.com/jaswdr/dockers/tree/master/docker-image-hosts