package tcleyman;

import javax.ejb.LocalBean;
import javax.ejb.Stateless;
import javax.jws.WebService;

import weblogic.jws.Policies;
import weblogic.jws.Policy;

import com.oracle.webservices.api.jms.JMSTransportService;
import com.oracle.webservices.api.jms.JMSDestinationType;
import com.oracle.webservices.api.jms.JMSMessageType;
import com.oracle.webservices.api.jms.JMSDeliveryMode;

/**
 * Session Bean implementation class MyJMSWS
 */


// destinationName: Specifies the JNDI name of the request queue
// default: com.oracle.webservices.api.jms.RequestQueue
// replyToName: Specifies the JNDI name of the JMS destination to which the response message is sent.
// default: replyToName = "com.oracle.webservices.api.jms.ResponseQueue",
// removed the JMSTransportService, ported that tho the pom file

@Policies({
    @Policy(uri="policy:Wssp1.2-2007-Saml1.1-Bearer-Wss1.1.xml")
    })
@WebService
//@JMSTransportService(targetService = "MyWS", destinationType = JMSDestinationType.QUEUE,messageType = JMSMessageType.TEXT, deliveryMode = JMSDeliveryMode.NON_PERSISTENT, priority = 4, mdbPerDestination = true)
//@JMSTransportService
@Stateless
@LocalBean
public class MyJMSWS2 {

    /**
     * Default constructor. 
     */
    public MyJMSWS2() {
        // TODO Auto-generated constructor stub
    }
    
    public String sayHello(String name)
    {
    System.out.println("sayHello invoked");
    return "hello " + name;
    }
    
    public String sayHello2(String name)
    {
    System.out.println("sayHello invoked");
    return "hello " + name;
    }

}
