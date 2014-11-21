minecraft-proxy
===============

A Minecraft proxy that boots an AWS EC2 instance when players connect. Every hour after boot minecraft-proxy shuts the instance down if there are no players. The idea is that end-users think this is just a normal Minecraft server. This requires some magic, and the magic might stop working in future versions.

Requirements
------------

 * You need an EC2 instance (I have `t2.small`) that starts Minecraft server 1.8 on boot.
 * You need access keys to boot and shutdown your instance.
 * You need python library `boto`

Usage
-----

 * Make sure the Minecraft server has idle kick.
 * Put you ec2 credintials to `~/.aws/credintials`. 
 * Edit `config.py`
 * Run `mcproxy.py`
