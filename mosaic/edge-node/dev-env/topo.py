from mininet.topo import Topo

class MyTopo( Topo ):
    def __init__( self ):
        Topo.__init__( self )

        # Add hosts
        h1 = self.addHost('h1', ip="10.0.0.1/8")
        h2 = self.addHost('h2', ip="10.0.0.2/8")
        # h3 = self.addHost("h3", ip="10.0.0.3/9")

        # Add switches
        s1 = self.addSwitch( 's1' )
        
        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        # self.addLink( h3, s1 )
        # self.addLink(h1, h2)


topos = { 'mytopo': MyTopo }
