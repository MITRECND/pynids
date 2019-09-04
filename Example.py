#! /usr/bin/env python

# pynids Example
# $Id: Example,v 1.3 2005/01/27 04:53:45 mjp Exp $

import os
import pwd
import sys
import nids

NOTROOT = "nobody"   # edit to taste
end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)


def handleTcpStream(tcp):
    print("tcps -", str(tcp.addr), " state:", tcp.nids_state)
    if tcp.nids_state == nids.NIDS_JUST_EST:
        # new to us, but do we care?
        ((src, sport), (dst, dport)) = tcp.addr
        print(tcp.addr)
        if dport in (80, 8000, 8080):
            print("collecting...")
            tcp.client.collect = 1
            tcp.server.collect = 1
    elif tcp.nids_state == nids.NIDS_DATA:
        # keep all of the stream's new data
        tcp.discard(0)
    elif tcp.nids_state in end_states:
        print("addr:", tcp.addr)
        print("To server:")
        print(tcp.server.data[:tcp.server.count])  # WARNING - may be binary
        print("To client:")
        print(tcp.client.data[:tcp.client.count])  # WARNING - as above


def main():

    # nids.param("pcap_filter", "tcp")      # bpf restrict to TCP only, note
                                            # libnids caution about fragments

    nids.param("scan_num_hosts", 0)         # disable portscan detection

    nids.chksum_ctl([('0.0.0.0/0', False)]) # disable checksumming

    if len(sys.argv) == 2:                  # read a pcap file?
        nids.param("filename", sys.argv[1])

    nids.init()

    (uid, gid) = pwd.getpwnam(NOTROOT)[2:4]
    os.setgroups([gid, ])
    os.setgid(gid)
    os.setuid(uid)
    if 0 in [os.getuid(), os.getgid()] + list(os.getgroups()):
        print("error - drop root, please!")
        sys.exit(1)

    nids.register_tcp(handleTcpStream)
    print("pid", os.getpid())

    # Loop forever (network device), or until EOF (pcap file)
    # Note that an exception in the callback will break the loop!
    try:
        nids.run()
    except nids.error as e:
        print("nids/pcap error:", e)
    except Exception as e:
        print("misc. exception (runtime error in user callback?):", e)


if __name__ == '__main__':
    main()
