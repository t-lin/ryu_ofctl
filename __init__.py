# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Ryu RESTful API abstraction
# Designed for ECE361 (University of Toronto) labs on SDN

"""
Pythonic interface for basic ovs-ofctl commands
Example workflow:
    The equivalent of 'ovs-ofctl add-flow s1 in_port=1,actions=output:2'
    Assume switch 's1' has datapath ID of 0x1
    >>> import ryu-ofctl
    >>> flow = ryu-ofctl.FlowEntry()
    >>> act = ryu-ofctl.OutputAction(2)
    >>>
    >>> flow.in_port = 1
    >>> flow.addAction(act)
    >>>
    >>> dpid = 0x1
    >>> ryu-ofctl.insertFlow(dpid, flow)


    The equivalent of 'ovs-ofctl del-flows s1 in_port=1'
    >>> import ryu-ofctl
    >>> flow = ryu-ofctl.FlowEntry()
    >>>
    >>> flow.in_port = 1
    >>>
    >>> dpid = 0x1
    >>> ryu-ofctl.deleteFlow(dpid, flow)


    The equivalent of 'ovs-ofctl del-flows s1'
    >>> import ryu-ofctl
    >>>
    >>> dpid = 0x1
    >>> ryu-ofctl.deleteAllFlows(dpid)
"""

from ryu_client import insertFlow, deleteFlow, deleteAllFlows,\
                        listSwitches, listLinks, listSwitchLinks, getMacIngressPort
from flow_entry import FlowEntry, OutputAction

__version__ = '1.1.0'

__all__ = [
    'insertFlow', 'deleteFlow', 'deleteAllFlows',
    'listSwitches', 'listLinks', 'listSwitchLinks', 'getMacIngressPort',
    'FlowEntry', 'OutputAction'
]

__author__ = 'Thomas Lin <t.lin@mail.utoronto.ca>'


