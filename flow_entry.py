# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2013, The SAVI Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class FlowAction(object):
    def __init__(self, action_id, param):
        assert type(action_id) is int
        self.action_id = action_id
        self.param = param

class OutputAction(FlowAction):
    def __init__(self, out_port):
        assert type(out_port) is int
        self.param = out_port

    def __str__(self):
        return "OutputAction: %s" % self.param


class FlowEntry(object):
    def __init__(self):
        # Initialize OF flow match's 12-tuple to all None (wildcards)
        self.in_port = None
        self.dl_src = None
        self.dl_dst = None
        self.dl_type = None
        self.dl_vlan = None
        self.dl_vlan_pcp = None
        self.nw_src = None
        self.nw_dst = None
        self.nw_proto = None
        self.nw_tos = None
        self.tp_src = None
        self.tp_dst = None

        # Not part of OF's 12-tuple; Used for deleting flows only
        self.out_port = None

        # Priority for tie-breaking
        self.priority = None

        # Initialize list of actions to empty list
        # Each action in the list is of a FlowAction class object
        self.actions = []

    def addAction(self, action):
        assert isinstance(action, FlowAction)
        self.actions.append(action)

    def getActions(self):
        return self.actions

    def printActions(self):
        for act in self.actions:
            print act

    def isAllWild(self):
        allWild = not (self.in_port or self.dl_src or self.dl_dst or \
                        self.dl_type or self.dl_vlan or self.dl_vlan_pcp or \
                        self.nw_src or self.nw_dst or self.nw_proto or \
                        self.nw_tos or self.tp_src or self.tp_dst)
        return allWild

    def printMatch(self):
        print str({'in_port': self.in_port, 'dl_dst': self.dl_dst, 'dl_src': self.dl_src,
            'dl_type': self.dl_type, 'dl_vlan': self.dl_vlan, 'dl_vlan_pcp': self.dl_vlan_pcp,
            'nw_dst': self.nw_dst, 'nw_proto': self.nw_proto,'nw_src': self.nw_src,
            'nw_tos': self.nw_tos, 'tp_src': self.tp_src, 'tp_dst': self.tp_dst})

    def reset(self):
        self.__init__()

    def validateMatch(self):
        # Ensure that if tp_dst or tp_src is set, it's either UDP or TCP
        if (self.tp_src or self.tp_dst):
            if (self.dl_type != 0x800):
                return False

            if (self.nw_proto != 0x6 and self.nw_proto != 0x11):
                return False

        return True
