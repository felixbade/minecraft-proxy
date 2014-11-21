# About the real Minecraft server
minecraft_server_port = 25565
ec2_region = '' # eg. 'eu-west-1'
ec2_instance_id = '' # eg. 'i-3fa43c84'

# Only these players can start the server. Other players can, however,
# keep the server running.
whitelist = ['put your username here']

# Stuff visible to the players
port = 25565
description_offline = 'Server is offline'
description_online = 'Server is online'
max_players_online = 20
max_players_offline = 0

# There is currently not an easy way to put your favicon to minecraft-proxy.
# You have to inspect the raw tcp stream that your client and your server sends.
# Then, if you have favicon, you should see there something that begins like this:
# data:image/png;base64,
# Copy paste it here.
favicon = None # eg. b'data:image/png;base64,iVBORw0KGgoAAA...AAAElFTkSuQmCC\\n'
