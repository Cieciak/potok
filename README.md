# potok

My homemade HTTP-like protocol

## Structure
```
-BEGIN-
POTOK
0.1
GET
-HEAD-
Target: example
Origin: here
-BODY-
rawdatabytes...
ewerfer56t4g43f
4364g3r3t5yvwvd
8net357u67453bh 

```
Content in `BODY` should be escaped

### There are no other constrains

# `CPPPMessage`

`class CPPPMessage(raw_data = None, *, header: dict = None, body = None)`

### `raw_data`
> Raw contents of the CPPP message
### `header`
> Dictionary containing CPPP header
### `body`
> Bytearray with message body

## Attributes
### `raw`
> Raw contents of the CPPP message
### `header`
> Message header
### `body`
> Bytearray with data

## Methods
### `add_header(header: dict)`
> Set message header to given dict
### `add_body(content: bytearray)`
> Set message body to bytearray

# CPPPServer

`class CPPPServer(address: str, port: int)`

## Attributes
### `address`
> Server address
### `port`
> Server port
### `connections`
> List of alive connections
### `ctx`
> Context for the server operation

### `request_handler`
> Function for handling the requests
```py
@server
def handler(msg: CPPPMessage, ctx):
	...
	return response
```

### `startup_handler`
> Startup function
```py
@server
def setup(ctx):
	...
```

### `error_handler`
> Fallback for server error
```py
@server
def error(msg: CPPPMessage, err: Execption, ctx):
	...
	return response
```
## Methods
### `serve()`
> Start the server

## Decorators
### `@self`
> Set server configuration functions