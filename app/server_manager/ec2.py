#!/usr/bin/env python

import logging

import boto.ec2

import config

class EC2Client:

    def __init__(self):
        self.conn = boto.ec2.connect_to_region(config.ec2_region)

    def stop(self):
        if self.get_status() in ['running', 'pending']:
            logging.info('Stopping server...')
            self.conn.stop_instances(instance_ids=[config.ec2_instance_id])

    def start(self):
        if self.get_status() == 'stopped':
            logging.info('Starting server...')
            self.conn.start_instances(instance_ids=[config.ec2_instance_id])

    def get_status(self):
        return self.get_instance()._state.name

    def get_ip(self):
        return self.get_instance().ip_address

    def get_instance(self):
        for instance in self.conn.get_only_instances():
            if instance.id == config.ec2_instance_id:
                return instance
        return None
