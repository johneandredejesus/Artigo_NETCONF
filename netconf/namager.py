from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager

host: str  = "210.200.20.70"
port: int = 22 # A porta default 22 pode ser usada. Mas a porta padrão é a 830.
username: str  = "admin"
password: str  = "admin"
timeout: int = 120

manager: Manager = None

def connect():
    global manager
    session = connect_ssh(host=host, port=port, username=username, password=password)
    manager = Manager(session, timeout=timeout)

def get_config():
    global manager
    filter_: str = """<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <ifmgr-cfg:interface-configurations xmlns:ifmgr-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg" 
                        xmlns:ipv4-io-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg" 
                        xmlns:ipv6-ma-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-cfg">
                        <ifmgr-cfg:interface-configuration>
                            <ifmgr-cfg:active>
                                act
                            </ifmgr-cfg:active>
                            <ifmgr-cfg:interface-name>
                                GigabitEthernet0/0/0/4
                            </ifmgr-cfg:interface-name>
                        </ifmgr-cfg:interface-configuration>
                    </ifmgr-cfg:interface-configurations>
                 </filter>"""
    return manager.get_config(source='candidate', filter=filter_).data_xml


def edit_config():
    global manager
    config: str ="""<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ifmgr-cfg:interface-configurations xmlns:ifmgr-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg" 
                xmlns:ipv4-io-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg" 
                xmlns:ipv6-ma-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-cfg">
                <ifmgr-cfg:interface-configuration>
                   <ifmgr-cfg:active>
                       act
                    </ifmgr-cfg:active>
                    <ifmgr-cfg:interface-name>
                       GigabitEthernet0/0/0/4
                    </ifmgr-cfg:interface-name>
                    <ipv4-io-cfg:ipv4-network>
                       <ipv4-io-cfg:addresses>
                           <ipv4-io-cfg:primary>
                               <ipv4-io-cfg:address>
                                   192.168.70.10
                                </ipv4-io-cfg:address>
                                <ipv4-io-cfg:netmask>
                                   255.255.255.0
                                </ipv4-io-cfg:netmask>
                            </ipv4-io-cfg:primary>
                        </ipv4-io-cfg:addresses>
                    </ipv4-io-cfg:ipv4-network>
                </ifmgr-cfg:interface-configuration>
        </ifmgr-cfg:interface-configurations>
    </config>"""
    manager.edit_config(config=config, target='candidate')
    manager.commit() #Usado para validar as ações desejadas.


def delete_config():
    global manager
    config: str ="""<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ifmgr-cfg:interface-configurations xmlns:ifmgr-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg" 
            xmlns:ipv4-io-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg" 
            xmlns:ipv6-ma-cfg="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-cfg">
            <ifmgr-cfg:interface-configuration>
                <ifmgr-cfg:active>
                    act
                </ifmgr-cfg:active>
                <ifmgr-cfg:interface-name>
                    GigabitEthernet0/0/0/4
                </ifmgr-cfg:interface-name>
                <ipv4-io-cfg:ipv4-network>
                    <ipv4-io-cfg:addresses>
                        <ipv4-io-cfg:primary xc:operation="delete">
                            <ipv4-io-cfg:address>
                                192.168.70.10
                            </ipv4-io-cfg:address>
                            <ipv4-io-cfg:netmask>
                                255.255.255.0
                            </ipv4-io-cfg:netmask>
                        </ipv4-io-cfg:primary>
                    </ipv4-io-cfg:addresses>
                </ipv4-io-cfg:ipv4-network>
            </ifmgr-cfg:interface-configuration>
        </ifmgr-cfg:interface-configurations>
    </config>"""
    manager.edit_config(config=config, target='candidate')
    manager.commit() #Usado para validar as ações desejadas


def main():
    connect()
    edit_config()
    xml = get_config()
    
    print('                                         ')
    print('                                         ')
    print(f'                {xml}                   ')
    print('                                         ')
    print('                                         ')
 
    
    delete_config()
    xml = get_config()
    
    print(f'                {xml}                   ')
    print('                                         ')
    print('                                         ')
     

if __name__ == '__main__':
    main()
