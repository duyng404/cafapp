# API Documentation

## Table of contents

[Auto Queue](#auto queue)

[Orders](#orders)

## General Overview
This is the restful api documentation for the CafApp project
through Enactus

The following will be a rough api spec containing all
the calls that have been included in the project. This
document is of course subject to change and should be updated
as the spec changes and more calls are added.

Remember, more documentation is better than less more less
is better than none at all.

As a reminder **all calls need to be authenticated through
the CAS single login system unless DEV mode is on** so the appropriate
permission decorators should be added to all api resources

## Auto Queue
`/api/v1/prep POST`

Can adjust the feed and refresh rate of the auto feeder

`/api/v1/prep/{run_flag} GET`

Turns the auto feeding of the queue on and off

## Orders
Perform basic operations such as creating a new order
`/api/v1/orders GET, POST`

Post requires *owner* and *content* which is a list of menu ids

`/api/v1/orders/{order_id} GET, PUT(Not yet implemented)`

Basic fetch and update of an order. PUT is not yet implemented

`/api/v1/orders/{order_id}/status GET, PUT`

Gets and updates the status of an order. Orders may not be manualy moved
from the wait queue (0) or from done (4). All other moves are valid.
PUT requires a from and a to

`/api/v1/orders/active`

Gets a list of all orders in prep (1), hot lamp (2), an on delivery (3)

## Users
`/api/v1/users GET, POST`

Basic get and post commands for the user resource. 
API will default to CAS credentials if dev flag is not turned on.
GET is not yet implemented

`/api/v1/users/{username} GET`

Get data for a user.
