'''
script created by tcleyman
Need to configure this one

aim is to configure credential mappers 
for /MyJMSWS/MyJMSWSService?WSDL
for //MyJMSWS_JMS/MyJMSWS?WSDL 
port jms:jndi:com.oracle.webservices.api.jms.RequestQueue?targetService=tcleyman.MyJMSWSService&jndiURL=t3://localhost:7001
'''

'''
 C:\PRODUCTS\WLS1213\user_projects\domains\domainNEWJMSClient\Script1421783603740.py.
C:\PRODUCTS\WLS1213\user_projects\domains\domainNEWJMSClient\Script1421783747400.py.
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
url='t3://localhost:7003'

domainName='domainNEWJMSClient'
domainHome='C:/PRODUCTS/WLS1213/user_projects/domains/domainNewJMS'
clear="true"
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
    

    
def function_CredMapper():
    '''
    function_CredMapper(): configure a SAML Credential Mapper
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
        saml2cm = rlm.lookupCredentialMapper("SAML_tcleyman_CredMapperV2")
        
        # do edit and startEdit later
        edit()
        startEdit() 
        # saml2cm.setIssuerURI('http://tomstest/')

        if (clear == "true"):
            print 'REMOVE ANY EXISTING CM PARTNERS'
            cursor = saml2cm.listSPPartners("*", 0)
            while saml2cm.haveCurrent(cursor) :
                name = saml2cm.getCurrentName(cursor)
                print 'removing ' + name
                saml2cm.removeSPPartner(name)
                saml2cm.advance(cursor)
            saml2cm.close(cursor)

        print 'finished deleting partners'
        
        # now configuring new partner
        print 'Configuring tomsCMPartner' 
        sp = saml2cm.newWSSSPPartner()
        sp.setName("tomsCMPartner")
        sp.setDescription('calling my saml - created by tcleyman')
        sp.setAudienceURIs(array(['target:*:/MyJMSWS'], java.lang.String))
        sp.setConfirmationMethod(sp.ASSERTION_TYPE_BEARER)
        sp.setEnabled(true)
        saml2cm.addSPPartner(sp)
        print 'Added IDP for ' + sp.getDescription()
        print sp.getAudienceURIs()
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

print 'configuring SAML Credential Mapper ....'
print function_CredMapper()


#print 'restarting server'
#print function_Restart()

print 'script finished successfully'
print 'exiting ...'
disconnect()
exit()