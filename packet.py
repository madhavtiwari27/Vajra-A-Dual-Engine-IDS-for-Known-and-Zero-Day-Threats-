import pyshark
import random
class Packet:
    packet_list = list()            
    def initiating_packets(self):
        self.packet_list.clear()
       
        capture = pyshark.LiveCapture(interface="Wi-Fi") 
        for packet in capture.sniff_continuously(packet_count=25):
            try:
                if "<UDP Layer>" in str(packet.layers) and "<IP Layer>" in str(packet.layers):
                    self.packet_list.append(packet)
                elif "<TCP Layer>" in str(packet.layers) and "<IP Layer>" in str(packet.layers):
                    self.packet_list.append(packet)
            except:
                print(f"No Attribute name 'ip' {packet.layers}")
                
    def udp_packet_attributes(self,packet):
        attr_list = list()
        a1 = packet.ip.ttl
        a2 = packet.ip.proto
        a3 = self.__get_service(packet.udp.port, packet.udp.dstport)
        a4 = packet.ip.len
        a5 = random.randrange(0,1000)
        a6 = self.__get_land(packet,a2)
        a7 = 0        
        a8, a10, a11 = self.__get_count_with_same_and_diff_service_rate(packet.udp.dstport, a3) 
        a9, a12 = self.__get_srv_count_and_srv_diff_host_rate(packet.ip.dst, packet.udp.dstport, a3) 
        a13, a14 = self.__get_dst_host_count_and_same_srv_rate(packet.ip.dst, packet.udp.dstport) 
        a15, a16 = self.__get_dst_host_srv_count_and_same_srv_rate(packet.udp.dstport) 
        a17, a18 = self.__get_dst_host_same_src_port_and_srv_diff_host_rate(packet.udp.port, packet.udp.dstport, packet.ip.dst) 
        a19 = 0        
        attr_list.extend([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19])
        return attr_list
        
    def tcp_packet_attributes(self,packet):
        attr_list = list()
        a1 = packet.ip.ttl
        a2 = packet.ip.proto
        a3 = self.__get_service(packet.tcp.port, packet.tcp.dstport)
        a4 = packet.ip.len
        a5 = packet.tcp.window_size
        a6 = self.__get_land(packet,a2)
        a7 = packet.tcp.urgent_pointer
        a8, a10, a11 = self.__get_count_with_same_and_diff_service_rate(packet.tcp.dstport, a3) 
        a9, a12 = self.__get_srv_count_and_srv_diff_host_rate(packet.ip.dst, packet.tcp.dstport, a3) 
        a13, a14 = self.__get_dst_host_count_and_same_srv_rate(packet.ip.dst, packet.tcp.dstport) 
        a15, a16 = self.__get_dst_host_srv_count_and_same_srv_rate(packet.tcp.dstport) 
        a17, a18 = self.__get_dst_host_same_src_port_and_srv_diff_host_rate(packet.tcp.port, packet.tcp.dstport, packet.ip.dst) 
        a19 = 0
        attr_list.extend([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19])
        return attr_list
    
    def __get_service(self,src_port, dst_port):
        
        if str(dst_port)=='80' or str(src_port)=='80':
            return 80
        elif str(dst_port)=='443' or str(src_port)=='443':
            return 443
        elif str(dst_port)=='53' or str(src_port)=='53':
            return 53
        else:
            return 0
    
    def __get_land(self,packet,protocol):
        
        if protocol=='17':
            if (packet.ip.src==packet.ip.dst) and (packet.udp.port==packet.udp.dstport):
                return 1
            else:
                return 0
        elif protocol=='6':
            if (packet.ip.src==packet.ip.dst) and (packet.tcp.port==packet.tcp.dstport):
                return 1
            else:
                return 0
        else:
            return 0

    def __get_count_with_same_and_diff_service_rate(self,dst_port, service): 
        count = 0 
        same_srv = 0
        diff_srv = 0
        for p in self.packet_list:
            if "<UDP Layer>" in str(p.layers):
                if (p.udp.dstport == dst_port):
                    count+=1
                    if (self.__get_service(p.udp.port, p.udp.dstport) == service):
                        same_srv+=1
                    else:
                        diff_srv+=1
            elif "<TCP Layer>" in str(p.layers):
                if (p.tcp.dstport == dst_port):
                    count+=1
                    if (self.__get_service(p.tcp.port, p.tcp.dstport) == service):
                        same_srv+=1
                    else:
                        diff_srv+=1
        same_srv_rate = 0.0
        diff_srv_rate = 0.0
        if not count==0:
            same_srv_rate = ((same_srv*100)/count)/100
            diff_srv_rate = ((diff_srv*100)/count)/100
        return (count, same_srv_rate, diff_srv_rate)

    def __get_srv_count_and_srv_diff_host_rate(self,dst_ip, dst_port, service): 
        srv_count = 0
        srv_diff_host = 0
        for p in self.packet_list:
            if "<UDP Layer>" in str(p.layers):
                if (p.ip.dst == dst_ip) and (self.__get_service(p.udp.port, p.udp.dstport) == service):
                    srv_count+=1
                    if not (p.ip.src == p.ip.dst):
                        srv_diff_host+=1
            elif "<TCP Layer>" in str(p.layers):
                if (p.ip.dst == dst_ip) and (self.__get_service(p.tcp.port, p.tcp.dstport) == service):
                    srv_count+=1
                    if not (p.ip.src == p.ip.dst):
                        srv_diff_host+=1
        srv_diff_host_rate = 0.0
        if not srv_count == 0:
            srv_diff_host_rate = ((srv_diff_host*100)/srv_count)/100
        return (srv_count, srv_diff_host_rate)
    
    def __get_dst_host_count_and_same_srv_rate(self,dst_ip, dst_port): 
        dst_host_count = 0
        same_srv_count = 0
        for p in self.packet_list:
            if "<UDP Layer>" in str(p.layers):
                if (p.ip.dst == dst_ip):
                    dst_host_count+=1
                    if (p.udp.dstport == dst_port):
                        same_srv_count+=1
            elif "<TCP Layer>" in str(p.layers):
                if (p.ip.dst == dst_ip):
                    dst_host_count+=1
                    if (p.tcp.dstport == dst_port):
                        same_srv_count+=1
        dst_host_same_srv_rate = 0.0
        if not dst_host_count == 0:
            dst_host_same_srv_rate = ((same_srv_count*100)/dst_host_count)/100
        return (dst_host_count, dst_host_same_srv_rate)
    
    def __get_dst_host_srv_count_and_same_srv_rate(self,dst_port): 
        dst_host_srv_count = 0
        for p in self.packet_list:
            if "<UDP Layer>" in str(p.layers):
                if (p.udp.dstport == dst_port):
                    dst_host_srv_count+=1
            elif "<TCP Layer>" in str(p.layers):
                if (p.tcp.dstport == dst_port):
                    dst_host_srv_count+=1
        return (dst_host_srv_count, 1.0) 
    
    def __get_dst_host_same_src_port_and_srv_diff_host_rate(self,src_port, dst_port, dst_ip): 
        dst_host_srv_count = 0
        same_src_port = 0
        diff_dst_ip = 0
        for p in self.packet_list:
            if "<UDP Layer>" in str(p.layers):
                if (p.udp.dstport == dst_port):      
                    dst_host_srv_count+=1
                    if (p.udp.port == src_port):    
                        same_src_port+=1
                    if not (p.ip.dst == dst_ip):         
                        diff_dst_ip+=1

            elif "<TCP Layer>" in str(p.layers):
                if (p.tcp.dstport == dst_port):     
                    dst_host_srv_count+=1
                    if (p.tcp.port == src_port):     
                        same_src_port+=1
                    if not (p.ip.dst == dst_ip):         
                        diff_dst_ip+=1
        dst_host_same_src_port_rate = 0.0
        dst_host_srv_diff_host_rate = 0.0
        if not dst_host_srv_count==0:
            dst_host_same_src_port_rate = ((same_src_port*100)/dst_host_srv_count)/100
            dst_host_srv_diff_host_rate = ((diff_dst_ip*100)/dst_host_srv_count)/100
        return (dst_host_same_src_port_rate, dst_host_srv_diff_host_rate)
