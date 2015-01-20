'''
script created by tcleyman
Need to configure this one

aim is to configure identity asserters 
for /MyJMSWS/MyJMSWSService?WSDL
for //MyJMSWS_JMS/MyJMSWS?WSDL 
port jms:jndi:com.oracle.webservices.api.jms.RequestQueue?targetService=tcleyman.MyJMSWSService&jndiURL=t3://localhost:7001
'''

#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

'''
variables used in script:
change where needed
'''
username = 'weblogic'
password = 'Nore1234'
url='t3://localhost:7001'

domainName='domainNewJMS'
domainHome='C:/PRODUCTS/WLS1213/user_projects/domains/domainNewJMS'
clear="false"
# means delete any previous created identity partners

def function_Info():
    '''
    function_Info() will dump info on the environment
    '''
    try:
        print version
        print sys.platform
        print sys.version_info
        print os.getenv("CLASSPATH")
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise     

def function_Connect():
    '''
    function_Connect() will connect to AdminServer
    '''
    try:
        connect(username,password,url)
        return 'success'
    except Exception, e:
        print e 
        print "Error while connecting!, trying to start AdminServer"
        #function_StartServer()
        dumpStack()
        raise     
    

    
def function_IdentityAsserter():
    '''
    function_IdentityAsserter(): configure a SAML Identity Asserter
    Note after this function the Server must be restarted
    '''
    try:
        '''
        java.lang.RuntimeException: java.lang.RuntimeException: Runtime Exception while calling invoke. Invoking management operations on Realm, UserLockoutManager and Security Provider MBeans via the Edit MBean Server is illegal. These management operations are supported by the Runtime MBean Server. If using WLST, modify your script to include a serverRuntime() command to switch to the runtime MBean hierarchy. If using a JMX client, modify your client to connect to the runtime MBean Server instead of the Edit MBean Server.
        '''
        #serverRuntime()
        #startEdit()
        #edit()
        #startEdit()
        '''
        this should also work:
        rlm = cmo.getSecurityConfiguration().getDefaultRealm()
        # SAML 2.0 IDENTITY ASSERTER
        saml2IA = rlm.lookupAuthenticationProvider("Saml2IdentityAsserter")
        '''
        #cd('/SecurityConfiguration/domainNewJMS/Realms/myrealm/AuthenticationProviders/SAML_tcleyman_IdAsserterV2')
        #saml2ia = cmo
        # assign cmo to var
        rlm = cmo.getSecurityConfiguration().getDefaultRealm()
        saml2ia = rlm.lookupAuthenticationProvider("SAML_tcleyman_IdAsserterV2")
        # do edit and startEdit later
        edit()
        startEdit() 
        if (clear == "true"):
            print 'REMOVE ANY EXISTING ID PARTNERS'
            cursor = saml2ia.listIdPPartners("*", 0)
            while saml2ia.haveCurrent(cursor) :
                name = saml2ia.getCurrentName(cursor)
                print 'deleting partner: ' + name
                saml2ia.removeIdPPartner(name)
                saml2ia.advance(cursor)
            saml2ia.close(cursor)
        print 'finished deleting partners'
        # now configuring new partner
        idp = saml2ia.newWSSIdPPartner()
        idp.setName('tomsIdentypartner')
        idp.setDescription('calling my saml - created by tcleyman')
        idp.setAudienceURIs(array(['target:*:/MyJMSWS'], java.lang.String))
        idp.setIssuerURI('http://tomstest/')
        idp.setConfirmationMethod(idp.ASSERTION_TYPE_BEARER)
        saml2ia.addIdPPartner(idp)
        print 'Added IDP for ' + idp.getDescription()
        print idp.getAudienceURIs()
        print 'save and activating changes ....'
        save()
        activate(block="true")
        return 'success'   
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise 



print 'starting the script ....'
print 'info on env being used'
function_Info()

print 'connecting ...'
print function_Connect()

#print 'destroy existing config'
#print function_DestroyExisting()

#print 'restarting server'
#print function_Restart()

print 'configuring SAML Identity Asserter ....'
print function_IdentityAsserter()


#print 'restarting server'
#print function_Restart()

print 'script finished successfully'
print 'exiting ...'
disconnect()
exit()
