# hosts
> Automatically update container ip to /etc/hosts base on container name

## Getting start

Start a new container passing your local `docker.sock` file

```bash
docker run -d -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc/hosts:/etc/hosts-host hackerliang/hosts
```