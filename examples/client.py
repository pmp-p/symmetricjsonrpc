#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=UTF-8 :

# python-symmetric-jsonrpc
# Copyright (C) 2009 Egil Moeller <redhog@redhog.org>
# Copyright (C) 2009 Nicklas Lindgren <nili@gulmohar.se>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import symmetricjsonrpc, sys

class PingRPCClient(symmetricjsonrpc.RPCClient):
    class Request(symmetricjsonrpc.RPCClient.Request):
        def dispatch_request(self, subject):
            # Handle callbacks from the server
            print("dispatch_request(%s)" % (repr(subject),))
            assert subject['method'] == "pingping"
            return "pingpong"

if '--help' in sys.argv:
    print("""client.py
    --ssl
        Encrypt communication with SSL using M2Crypto. Requires a
        server.pem in the current directory.
""")
    sys.exit(0)

if '--ssl' in sys.argv:
    # Set up an SSL connection
    import M2Crypto
    ctx = M2Crypto.SSL.Context()
    ctx.set_verify(M2Crypto.SSL.verify_peer | M2Crypto.SSL.verify_fail_if_no_peer_cert, depth=9)
    if ctx.load_verify_locations('server.pem') != 1: raise Exception('No CA certs')
    s = M2Crypto.SSL.Connection(ctx)
else:
    # Set up a TCP socket
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#  Connect to the server
s.connect(('192.168.3.111', 4712))

# Create a client thread handling for incoming requests
client = PingRPCClient(s)

# Call a method on the server
res = client.request("ping", wait_for_response=True)
print("client.ping => %s" % (repr(res),))
assert res == "pong"

# Notify server it can shut down
client.notify("shutdown")

client.shutdown()
