# clash-update
A script to update your clash config on linux based system

## Create a blank config first

e.g.

The file name is config.yaml
**(You must create the blank file first by yourself `touch config.yaml`)**

Then you can run the **clash-update** container,
1. Change the ([PROVIDER]: url) in clash-update.ini
to your clash subscription link.
   
2. Change the ([CONTAINER]: url) in clash-update.ini
to your clash RESTFUL url
   
3. Change the ([CONTAINER]: secret) in clash-update.ini
to your clash pass

Then run the container by:
```bash
docker run --name clash-update -d \
    -v /path/to/clash-update.ini:/clash-update.ini \
    -v /path/to/config.yaml:/config.yaml \
    --restart=always \
    --cpus=".5" \
    --memory=512m \
    hackerliang/clash-update
```

After this, you can run the clash core by:


```bash
docker run -d --name clash \
    -v /path/to/config.yaml:/root/.config/clash/config.yaml \
    -p 7890:7890 \
    -p 9090:9090 \
    --restart always \
    dreamacro/clash
```

Then, you can choose to run a clash webUI by:

```bash
docker run --name yacd -p 1234:80 \
    --restart=always -d haishanh/yacd
```

Visit http://YOUR_MACHINE_IP:1234