
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"

#define Max_Time 50

// n1   n2   n3   n4   --------------     n5   n6   n7   n8
// |    |    |    |    point-to-point     |    |    |    |
// ================                       ================
//  LAN 192.168.2.0                        LAN 222.192.3.0

using namespace ns3;
NS_LOG_COMPONENT_DEFINE("SecondScriptExample");

int main(int argc, char *argv[])
{
    bool verbose = true;
    uint32_t nCsma = 3;

    CommandLine cmd(__FILE__);
    cmd.AddValue("nCsma", "Number of \"extra\" CSMA nodes/devices", nCsma);
    cmd.AddValue("verbose", "Tell echo applications to log if true", verbose);

    cmd.Parse(argc, argv);

    if (verbose)
    {
        LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
        LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);
    }

    NodeContainer p2pNodes;
    p2pNodes.Create(2);

    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("10Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("1ms"));

    NetDeviceContainer p2pDevices;
    p2pDevices = pointToPoint.Install(p2pNodes);

    NodeContainer csmaNodes;
    csmaNodes.Add(p2pNodes.Get(1));

    NodeContainer csmaNodes1;
    csmaNodes1.Add(p2pNodes.Get(0));
    csmaNodes1.Create(nCsma);

    CsmaHelper csma;
    csma.SetChannelAttribute("DataRate", StringValue("10Mbps"));
    csma.SetChannelAttribute("Delay", StringValue("1ms"));

    NetDeviceContainer csmaDevices;
    csmaDevices = csma.Install(csmaNodes);

    NetDeviceContainer csmaDevices1;
    csmaDevices1 = csma.Install(csmaNodes1);

    InternetStackHelper stack;
    stack.Install(csmaNodes);
    stack.Install(csmaNodes1);

    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer p2pInterfaces;
    p2pInterfaces = address.Assign(p2pDevices);

    address.SetBase("192.168.2.0", "255.255.255.0");
    Ipv4InterfaceContainer csmaInterfaces;
    csmaInterfaces = address.Assign(csmaDevices);

    address.SetBase("222.192.3.0", "255.255.255.0");
    Ipv4InterfaceContainer csmaInterfaces1;
    csmaInterfaces1 = address.Assign(csmaDevices1);

    UdpEchoServerHelper echoServer(10);

    ApplicationContainer serverApps = echoServer.Install(csmaNodes1.Get(1)); // server is considered as n6
    serverApps.Start(Seconds(1.0));
    serverApps.Stop(Seconds(Max_Time - 1));

    UdpEchoClientHelper echoClient(csmaInterfaces1.GetAddress(1), 10);
    echoClient.SetAttribute("MaxPackets", UintegerValue(500));
    echoClient.SetAttribute("Interval", TimeValue(Seconds(2.0)));
    echoClient.SetAttribute("PacketSize", UintegerValue(2048));

    ApplicationContainer clientApps = echoClient.Install(csmaNodes.Get(1));
    clientApps.Start(Seconds(2.0));
    clientApps.Stop(Seconds(Max_Time));

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    AsciiTraceHelper ascii;
    csma.EnableAsciiAll(ascii.CreateFileStream("labtest.tr"));

    Simulator::Run();
    Simulator::Destroy();
    return 0;
}
