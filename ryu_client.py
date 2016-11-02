# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Abstraction for Ryu RESTful APIs

import httplib
import json

from flow_entry import FlowEntry, OutputAction

# Flow match and actions specified in body
ADD_FLOW_URL = '/stats/flowentry/add'

# (dpid)
DEL_ALL_FLOWS_URL = '/stats/flowentry/clear/%s'

# Flow match specified in body
DEL_FLOW_URL = '/stats/flowentry/delete'

RYU_API_HOST = '127.0.0.1'
RYU_API_PORT = 8090

def setRyuEndpoint(ip, port):
    assert type(ip) in (str, unicode)
    assert type(port) is int
    RYU_API_HOST = ip
    RYU_API_PORT = port

# Returns 0 if everything is okay, else a non-zero status
def _controllerAction(action, method, body=None):
    conn = httplib.HTTPConnection(RYU_API_HOST, RYU_API_PORT)

    url = action
    #LOG.debug("SENDING DOWN TO CONTROLLER: url = %s ; body = %s" % (url, body))
    conn.request(method, url, body)
    res = conn.getresponse()
    if res.status in (httplib.OK,
                      httplib.CREATED,
                      httplib.ACCEPTED,
                      httplib.NO_CONTENT):
        return res.status

    raise httplib.HTTPException(
        res, 'code %d reason %s' % (res.status, res.reason),
        res.getheaders(), res.read())

# Returns a dictionary version of the flow match in a form Ryu can use
def _getMatchDict(flow):
    assert isinstance(flow, FlowEntry)
    match = {}

    if flow.in_port:
        match['in_port'] = flow.in_port
    if flow.dl_src:
        match['dl_src'] = flow.dl_src
    if flow.dl_dst:
        match['dl_dst'] = flow.dl_dst
    #if flow.dl_type:
    #    match['dl_type'] = flow.dl_type
    #if flow.dl_vlan:
    #    match['dl_vlan'] = flow.dl_vlan
    #if flow.dl_vlan_pcp:
    #    match['dl_vlan_pcp'] = flow.dl_vlan_pcp
    #if flow.nw_src:
    #    match['nw_src'] = flow.nw_src
    #if flow.nw_dst:
    #    match['nw_dst'] = flow.nw_dst
    #if flow.nw_proto:
    #    match['nw_proto'] = flow.nw_proto
    #if flow.nw_tos:
    #    match['nw_tos'] = flow.nw_tos
    #if flow.tp_src:
    #    match['tp_src'] = flow.tp_src
    #if flow.tp_dst:
    #    match['tp_dst'] = flow.tp_dst

    return match

# Insert a flow into a switch
def insertFlow(dpid, flowEntry):
    #LOG.debug("Ryu driver adding flow")
    #dpid = kwargs.get('dpid')
    #flow = kwargs.get('flow')
    assert type(dpid) in (int, long)
    assert flowEntry.isAllWild() is False

    actions = []
    for act in flowEntry.getActions():
        if isinstance(act, OutputAction):
            actions.append({"type": "OUTPUT", "port": act.out_port})
        else:
            LOG.debug("%s ERROR: Unimplemented actions", self.__class__.__name__)

    match = _getMatchDict(flowEntry)
    body = {"dpid": dpid, "actions": actions, "match": match}

    #LOG.debug("ADDING FLOW dpid = %s, in_port = %s, src = %s, dst = %s, actions = %s",
    #            (dpid), flow.in_port, flow.dl_src, flow.dl_dst, actions)
    status = _controllerAction(ADD_FLOW_URL, 'POST', json.dumps(body))
    return status

# Delete flow(s) from a switch
def deleteFlow(dpid, flowEntry):
    #LOG.debug("Ryu driver deleting flow")
    #dpid = kwargs.get('dpid')
    #flow = kwargs.get('flow')
    assert type(dpid) in (int, long)
    assert isinstance(flowEntry, FlowEntry)

    if flowEntry.isAllWild() and not flowEntry.out_port:
        # Delete all flows
        #LOG.debug("Deleting all flows in switch %s", hex(dpid))
        status = _controllerAction(DEL_ALL_FLOWS_URL % dpid, 'DELETE')
    else:
        # Delete specific flows
        match = _getMatchDict(flowEntry)
        body = {"dpid": dpid, "match": match}
        if flowEntry.out_port:
            body["out_port"] = flowEntry.out_port
        status = _controllerAction(DEL_FLOW_URL, 'POST', json.dumps(body))

    return status

# Delete all flows from a switch
def deleteAllFlows(dpid):
    return deleteFlow(dpid, FlowEntry())


