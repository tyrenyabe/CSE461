# Part 3 of UWCSE's Project 3
#
# based on Lab Final from UCSC's Networking Class
# which is based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr

log = core.getLogger()

#statically allocate a routing table for hosts
#MACs used in only in part 4
IPS = {
  "h10" : ("10.0.1.10", '00:00:00:00:00:01'),
  "h20" : ("10.0.2.20", '00:00:00:00:00:02'),
  "h30" : ("10.0.3.30", '00:00:00:00:00:03'),
  "serv1" : ("10.0.4.10", '00:00:00:00:00:04'),
  "hnotrust" : ("172.16.10.100", '00:00:00:00:00:05'),
}

class Part4Controller (object):
  """
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    print (connection.dpid)
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
    #use the dpid to figure out what switch is being created
    if (connection.dpid == 1):
      self.s1_setup()
    elif (connection.dpid == 2):
      self.s2_setup()
    elif (connection.dpid == 3):
      self.s3_setup()
    elif (connection.dpid == 21):
      self.cores21_setup()
    elif (connection.dpid == 31):
      self.dcs31_setup()
    else:
      print ("UNKNOWN SWITCH")
      exit(1)

    # Map from Host IP's to port #'s
    self.map = {}

  def s1_setup(self):
    #put switch 1 rules here
    fm=of.ofp_flow_mod()
    fm.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(fm)

  def s2_setup(self):
    #put switch 2 rules here
    fm=of.ofp_flow_mod()
    fm.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(fm)

  def s3_setup(self):
    #put switch 3 rules here
    fm=of.ofp_flow_mod()
    fm.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(fm)

  def cores21_setup(self):
    #put core switch rules here
    pass
    

  def dcs31_setup(self):
    #put datacenter switch rules here
    fm=of.ofp_flow_mod()
    fm.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(fm)

  #used in part 4 to handle individual ARP packets
  #not needed for part 3 (USE RULES!)
  #causes the switch to output packet_in on out_port
  def resend_packet(self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    try:
      if packet.payload.protosrc not in self.map:
        for k, v in self.map.items():
          if packet.payload.protosrc == IPS["hnotrust"][0]:
            if k == IPS["serv1"][0]:
              # Block any IP traffic from notrust to server
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_src = packet.payload.protosrc
              msg.match.nw_dst = k
              self.connection.send(msg)

              # Allow any IP traffic from server to notrust
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_dst = packet.payload.protosrc
              msg.match.nw_src = k
              action = of.ofp_action_dl_addr.set_dst(packet.payload.hwsrc)
              msg.actions.append(action)
              action = of.ofp_action_output(port = packet_in.in_port)
              msg.actions.append(action)
              self.connection.send(msg)
            else:
              # Block ICMP traffic from notrust to any host
              msg = of.ofp_flow_mod()
              msg.priority = 100
              msg.match.dl_type = 0x0800
              msg.match.nw_proto = 1
              msg.match.nw_src = packet.payload.protosrc
              msg.match.nw_dst = k
              self.connection.send(msg)

              # Allow any IP traffic from notrust to any host (lower priority than blocking ICMP traffic)
              msg = of.ofp_flow_mod()
              msg.priority = 50
              msg.match.dl_type = 0x0800
              msg.match.nw_src = packet.payload.protosrc
              msg.match.nw_dst = k
              action = of.ofp_action_dl_addr.set_dst(v[1])
              msg.actions.append(action)
              action = of.ofp_action_output(port = v[0])
              msg.actions.append(action)
              self.connection.send(msg)

              # Allow any IP traffic from any host to notrust
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_src = k
              msg.match.nw_dst = packet.payload.protosrc
              action = of.ofp_action_dl_addr.set_dst(packet.payload.hwsrc)
              msg.actions.append(action)
              action = of.ofp_action_output(port = packet_in.in_port)
              msg.actions.append(action)
              self.connection.send(msg)
          elif k == IPS["hnotrust"][0]:
            # Host to notrust / server to notrust
            if packet.payload.protosrc == IPS["serv1"][0]:
              # Block any IP traffic from notrust to server
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_src = k
              msg.match.nw_dst = packet.payload.protosrc
              self.connection.send(msg)

              # Allow any IP traffic from server to notrust
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_dst = k
              msg.match.nw_src = packet.payload.protosrc
              action = of.ofp_action_dl_addr.set_dst(v[1])
              msg.actions.append(action)
              action = of.ofp_action_output(port = v[0])
              msg.actions.append(action)
              self.connection.send(msg)
            else:
              # Block ICMP traffic from notrust to any host
              msg = of.ofp_flow_mod()
              msg.priority = 100
              msg.match.dl_type = 0x0800
              msg.match.nw_proto = 1
              msg.match.nw_src = k
              msg.match.nw_dst = packet.payload.protosrc
              self.connection.send(msg)

              # Allow any IP traffic from notrust to any host (lower priority than blocking ICMP traffic)
              msg = of.ofp_flow_mod()
              msg.priority = 50
              msg.match.dl_type = 0x0800
              msg.match.nw_src = packet.payload.protosrc
              msg.match.nw_dst = k
              action = of.ofp_action_dl_addr.set_dst(v[1])
              msg.actions.append(action)
              action = of.ofp_action_output(port = v[0])
              msg.actions.append(action)
              self.connection.send(msg)

              # Allow any IP traffic from any host to notrust
              msg = of.ofp_flow_mod()
              msg.match.dl_type = 0x0800
              msg.match.nw_src = k
              msg.match.nw_dst = packet.payload.protosrc
              action = of.ofp_action_dl_addr.set_dst(packet.payload.hwsrc)
              msg.actions.append(action)
              action = of.ofp_action_output(port = packet_in.in_port)
              msg.actions.append(action)
              self.connection.send(msg)
          else:
            # Host to host / server to host / host to server
            # Allow all IP traffic from A to B
            msg = of.ofp_flow_mod()
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = k
            msg.match.nw_src = packet.payload.protosrc
            action = of.ofp_action_dl_addr.set_dst(v[1])
            msg.actions.append(action)
            action = of.ofp_action_output(port = v[0])
            msg.actions.append(action)
            self.connection.send(msg)

            # Allow all IP traffic from B to A
            msg = of.ofp_flow_mod()
            msg.match.dl_type = 0x0800
            msg.match.nw_dst = packet.payload.protosrc
            msg.match.nw_src = k
            action = of.ofp_action_dl_addr.set_dst(packet.payload.hwsrc)
            msg.actions.append(action)
            action = of.ofp_action_output(port = packet_in.in_port)
            msg.actions.append(action)
            self.connection.send(msg)

        self.map[packet.payload.protosrc] = (packet_in.in_port, packet.payload.hwsrc, packet.payload.protodst)
        
      packet.payload.opcode = 2
      # temp = packet.payload.hwdst
      # packet.payload.hwdst = packet.payload.hwsrc
      # packet.payload.hwsrc = temp
      temp = packet.payload.protodst
      packet.payload.protodst = packet.payload.protosrc
      packet.payload.protosrc = temp

      self.resend_packet(packet, self.map[packet.payload.protodst][0])

      if packet.payload.protodst in self.map:
        self.resend_packet(packet, self.map[packet.payload.protodst][0])
      else:
        self.resend_packet(packet, of.OFPP_ALL)
    except:
      pass

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Part4Controller(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
