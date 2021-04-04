#!/usr/bin/env python3

import sys
import docker
import time
import re


def log(message):
    print("{} {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))


def check_host(text, host):
    regex = r"\s" + host + "$"
    flags = re.I
    founds = re.compile(regex, flags).findall(text)
    return len(founds) > 0


def update_hosts_file():
    log("Updating hosts file")
    client = docker.from_env()
    containers = client.containers.list()

    hosts = []
    for c in containers:
        env = c.exec_run("env")
        output = env.output.decode("utf-8")
        # start = output.find("VIRTUAL_HOST")
        start = 1
        if start >= 0:
            end = output[start:].find("\n") + start
            # virtual_host = output[start:end].split("=")[1]
            virtual_host = c.name
            # ip = c.exec_run("hostname -i").output.decode("utf-8").split("\n")[0]
            ip = c.attrs["NetworkSettings"]["IPAddress"]
            if ip == "":
                continue

            add = True
            for h in hosts:
                if h["ip"] == ip:
                    add = False
                    break

            if add:
                hosts.append({
                    "virtual_host": virtual_host,
                    "ip": ip,
                    "content": ip + "\t" + virtual_host})

    host_file_content = open("/etc/hosts-host", "r").read().strip().split("\n")

    content = ""

    # update
    for line in host_file_content:
        add = True
        for h in hosts:
            if check_host(line, h["virtual_host"]):
                content += h["content"] + "\n"
                add = False
                log("{} updated".format(h["virtual_host"]))
        if add:
            content += line + "\n"

    for h in hosts:
        add = True
        for line in host_file_content:
            if check_host(line, h["virtual_host"]):
                add = False
                break

        if add:
            content += h["content"] + "\n"
            log("{} added".format(h["virtual_host"]))

    host_file = open("/etc/hosts-host", "w")
    host_file.write(content.strip())
    host_file.close()
    client.close()


while True:
    update_hosts_file()
    time.sleep(5)
