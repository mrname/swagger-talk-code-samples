"""
A tiny demo of bravado client and why it's cool
"""

from __future__ import print_function

from bravado.client import SwaggerClient

# Load up the client
client = SwaggerClient.from_url("http://petstore.swagger.io/v2/swagger.json")

# See what we got up in hea
print(dir(client))

# See what we can do with pets specifically
print(dir(client.pet))

# Find only available pets. This returns an HTTPFuture object
request = client.pet.findPetsByStatus(status=['available'])
available_pets = request.result()

# Ask to buy the first pet
print('I would like to buy the pet named {0}'.format(available_pets[0].name))
