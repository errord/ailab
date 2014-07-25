#
# concept neural network
#

import sys

debug = True

def logging(msg):
    if not debug:
        return
    print msg

class Seq(object):
    seq = 0
    def __init__(self):
        pass

    @classmethod
    def get_seq(cls):
        cls.seq += 1
        return cls.seq

class Node(object):
    STATE_STOP = 0
    STATE_ACTIVATION = 1

    def __init__(self, natures):
        self._natures = natures
        self._state = self.STATE_STOP
        self._actived = False
        self._link_node = []
        self._seq = 0

    def get_natures(self):
        return self._natures

    def add_link_node(self, node):
        self._link_node.append(node)

    def activ_link_node(self, natures):
        for node in self._link_node:
            node.activation(natures)

    def is_activ(self):
        return False if self._state == self.STATE_STOP else True

    def is_actived(self):
        return self._actived

    def actived(self):
        self._actived = True
        self._seq = Seq.get_seq()

    def activation(self, stimulates):
        pass

    def action(self):
        pass

class NoActivNode(Node):
    def __init__(self):
        super(NoActivNode, self).__init__(None)

    def is_activ(self):
        return False

class MemNode(NoActivNode):
    def __init__(self, mem_nodes, mem):
        super(MemNode, self).__init__()
        self._mem_nodes = mem_nodes
        self._mem = mem

    def action(self):
        for node in self._mem_nodes:
            if not node.is_actived():
                return
        self._mem.activation(self._mem.get_natures())
        self._mem.action()

class WatchNode(NoActivNode):
    def __init__(self):
        super(WatchNode, self).__init__()
        self._watchs = []

    def activation(self, stimulates):
        self._watchs.append(stimulates)

    def get_watchs(self):
        return self._watchs

    def dump_watchs(self):
        if not debug:
            return

        print '-'*50, 'watch', '-'*50
        for watch in self._watchs:
            print watch

    def result(self):
        return self._watchs[-1]

class SymbolNode(Node):
    def __init__(self, natures):
        super(SymbolNode, self).__init__(natures)

    def __str__(self):
        return "<SymbolNode seq:%s state:%s actived:%s symbol:%s>" % (
            self._seq,
            self._state, 
            self._actived,
            self._natures)

    def activation(self, stimulates):
        stimulates = str(stimulates)
        if stimulates == self._natures:
            self._state = self.STATE_ACTIVATION
            self.actived()

        logging("%s %s" % (self, stimulates))

    def action(self):
        if self._state == self.STATE_STOP:
            return

        nature = ('Symbol', self._natures)
        self.activ_link_node(nature)
        self._state = self.STATE_STOP

class OpNode(Node):
    def __init__(self, natures):
        super(OpNode, self).__init__(natures)
        self._op_args = []

    def __str__(self):
        return "<OpNode seq:%s state:%s op:%s args:%s>" % (
            self._seq,
            self._state, 
            self._natures, self._op_args)

    def activation(self, stimulates):
        print 'a'*10, stimulates
        if self._state == self.STATE_STOP and stimulates == self._natures:
            self._state = self.STATE_ACTIVATION
            self.actived()

        if self._state == self.STATE_ACTIVATION and type(stimulates) == tuple:
            if stimulates[0] == 'Symbol':
                self._op_args.append(stimulates[1])

    def action(self):
        if self._state == self.STATE_STOP:
            return

        if len(self._op_args) >= 2:
            nature = self.run_op(self._op_args[0], self._op_args[1])
            self.activ_link_node(nature)
            self._state = self.STATE_STOP

class ADD_OpNode(OpNode):
    def __init__(self):
        super(ADD_OpNode, self).__init__('+')
        pass

    def run_op(self, arg1, arg2):
        return int(arg1) + int(arg2)


class NN(object):
    def __init__(self):
        self._watchnode = WatchNode()
        self._nodes = [
            self._watchnode,
            ADD_OpNode(),
        ]
        node_0 = SymbolNode('0')
        self._nodes.append(node_0)
        node_1 = SymbolNode('1')
        self._nodes.append(node_1)
        node_2 = SymbolNode('2')
        self._nodes.append(node_2)
        node_3 = SymbolNode('3')
        self._nodes.append(node_3)
        node_4 = SymbolNode('4')
        self._nodes.append(node_4)
        node_5 = SymbolNode('5')
        self._nodes.append(node_5)
        node_6 = SymbolNode('6')
        self._nodes.append(node_6)
        node_7 = SymbolNode('7')
        self._nodes.append(node_7)
        node_8 = SymbolNode('8')
        self._nodes.append(node_8)
        node_9 = SymbolNode('9')
        self._nodes.append(node_9)

        node_mutl = SymbolNode('*')
        self._nodes.append(node_mutl)

        memnode = MemNode([node_2, node_3, node_mutl], node_6)
        self._nodes.append(memnode)

        self._link_all_node()

    def _link_all_node(self):
        for node in self._nodes:
            for lnode in self._nodes:
                if node != lnode:
                    node.add_link_node(lnode)

    def _init_activ(self, e):
        for natures in e:
            for node in self._nodes:
                node.activation(natures)

    def _action_order(self):
        self._nodes.sort(key=lambda node: node._seq)

    def _actions(self):
        has_activ = True
        while has_activ:
            has_activ = False
            self._action_order()
            for node in self._nodes:
                node.action()
                if node.is_activ():
                    has_activ = True
            self.dump()

    def dump(self):
        if not debug:
            return

        print '-'*50, 'dump', '-'*50
        for node in self._nodes:
            print node
        print 'characterization:'
        print self.characterization()

    def characterization(self):
        character = ''
        for node in self._nodes:
            if node.is_activ():
                character += '1'
            else:
                character += '0'
        return character

    def run(self, e):
        print 'exec: %s' % e
        self._init_activ(e)
        self._actions()
        self._watchnode.dump_watchs()
        return str(self._watchnode.result())

if __name__ == '__main__':
    debug = True
    nn = NN()
    e =  'c3+50 =s -df'
    if len(sys.argv) > 1:
        e = sys.argv[1]
    print "reslut: %s" % nn.run(e)
