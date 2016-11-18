## ryu\_ofctl: Pythonic interface for interfacing with Ryu's RESTful APIs
Pythonic interface for providing:
  - Basic ovs-ofctl commands
  - Querying topology information

Currently, flow entry match fields support:
  - L1 port (*in\_port*)
  - L2 src & dst (*dl\_src* and *dl\_dst*)

### Example workflow for flow-table manipulation
**All examples here assume switch 's1' has datapath ID of 0x1**

The equivalent of *'ovs-ofctl add-flow s1 in_port=1,dl_dst=00:00:00:00:00:02,actions=output:2'*  
This installs a flow table rule that matches any packets coming in from  
port 1 with destination MAC 00:00:00:00:00:02, and forwards it via port 2
```
>>> import ryu_ofctl
>>> flow = ryu_ofctl.FlowEntry()
>>> act = ryu_ofctl.OutputAction(2)
>>>
>>> flow.in_port = 1
>>> flow.dl_dst = "00:00:00:00:00:02"
>>> flow.addAction(act)
>>>
>>> dpid = 0x1
>>> ryu_ofctl.insertFlow(dpid, flow)
'Success!'
>>>
```

The equivalent of *'ovs-ofctl add-flow s1 in_port=2,actions=output:3,output:1'*  
This installs a flow table rule that matches any packets coming in from  
port 2 and forwards a copy of it via port 3 and port 1
```
>>> import ryu_ofctl
>>> flow = ryu_ofctl.FlowEntry()
>>> act1 = ryu_ofctl.OutputAction(3)
>>> act2 = ryu_ofctl.OutputAction(1)
>>>
>>> flow.in_port = 2
>>> flow.addAction(act1)
>>> flow.addAction(act2)
>>>
>>> dpid = 0x1
>>> ryu_ofctl.insertFlow(dpid, flow)
'Success!'
>>>
```

The equivalent of *'ovs-ofctl del-flows s1 in_port=1'*  
This deletes any flow table rules that matches on input port of 1
```
>>> import ryu_ofctl
>>> flow = ryu_ofctl.FlowEntry()
>>>
>>> flow.in_port = 1
>>>
>>> dpid = 0x1
>>> ryu_ofctl.deleteFlow(dpid, flow)
'Success!'
>>>
```

The equivalent of *'ovs-ofctl del-flows s1'* (flushing the flow table)  
This deletes all flow table rules in the switch
```
>>> import ryu_ofctl
>>> dpid = 0x1
>>> ryu_ofctl.deleteAllFlows(dpid)
'Success!'
>>>
```

To get the list of current actions in a FlowEntry object, or print them
```
>>> import ryu_ofctl
>>> flow = ryu_ofctl.FlowEntry()
>>> act1 = ryu_ofctl.OutputAction(3)
>>> act2 = ryu_ofctl.OutputAction(1)
>>>
>>> flow.addAction(act1)
>>> flow.addAction(act2)
>>>
>>> flow.getActions()
[<ryu_ofctl.flow_entry.OutputAction object at 0x19317d0>, <ryu_ofctl.flow_entry.OutputAction object at 0x1931810>]
>>>
>>> flow.printActions()
OutputAction: 3
OutputAction: 1
>>>
```


### Example workflow for querying topology information
**The following APIs returns either None or some type of dictionary object (i.e. JSON format)**

To get a list of switch IDs (a.k.a. datapath IDs or dpids)
```
>>> import ryu_ofctl
>>> ryu_ofctl.listSwitches()
{'dpids': [1, 2, 3]}
>>>
```

To query a list of links within the topology  
**Note:** A link is defined as a *uni-directional* connection between two switches, where  
both switches belonged to the list of switches provided by `listSwitches()`
```
>>> import ryu_ofctl
>>> ryu_ofctl.listLinks() # Each link is uni-directional
{'links': [{'endpoint1': {'port': 3, 'dpid': 2}, 'endpoint2': {'port': 2, 'dpid': 3}}, {'endpoint1': {'port': 2, 'dpid': 2}, 'endpoint2': {'port': 2, 'dpid': 1}}, {'endpoint1': {'port': 2, 'dpid': 3}, 'endpoint2': {'port': 3, 'dpid': 2}}, {'endpoint1': {'port': 2, 'dpid': 1}, 'endpoint2': {'port': 2, 'dpid': 2}}]}
>>>
```

To query a list of links connected to a given switch ID
```
>>> import ryu_ofctl
>>> ryu_ofctl.listSwitchLinks(1) # Each link is uni-directional
{'links': [{'endpoint1': {'port': 2, 'dpid': 2}, 'endpoint2': {'port': 2, 'dpid': 1}}, {'endpoint1': {'port': 2, 'dpid': 1}, 'endpoint2': {'port': 2, 'dpid': 2}}]}
>>>
```

To query the ingress port of packets with a given source MAC address (i.e. the switch and  
physical port where packets from a given source enter the network)  
This returns None if the ingress port is unknown (no packets with this source has yet to  
be seen by the controller)
```
>>> import ryu_ofctl
>>> mac = "00:00:00:00:00:03"
>>> ryu_ofctl.getMacIngressPort(mac)
{'port': 1, 'dpid': 3}
>>>
>>> mac2 = "de:ad:be:ef:12:34" # Does not exist
>>> ryu_ofctl.getMacIngressPort(mac2)
>>>
```

