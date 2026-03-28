# XML-RPC Socket Server (From Scratch)

Academic project implementing an XML-RPC client and server from scratch using raw TCP sockets in Python.

This project does not rely on high-level HTTP or RPC frameworks. 
All protocol handling is implemented manually.

## Features

- Manual HTTP/1.1 parsing
- XML-RPC request and response handling
- Fault code management
- Multithreaded server using threading
- Timeout handling
- Strict protocol validation
- Custom method registration

## Architecture

- `client.py` → XML-RPC client implementation
- `server.py` → Multithreaded XML-RPC server
- `examples/` → Example usage

## What I Learned

- Low-level socket programming
- Manual HTTP protocol parsing
- XML parsing and validation
- Multithreaded server design
- Error handling in network protocols
- Designing a simple RPC system

## Technologies

- Python
- socket
- threading
- xml.etree.ElementTree