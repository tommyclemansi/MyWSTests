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
'''
username = 'weblogic'
password = 'Nore1234'
url='t3://localhost:7001'


def function_Info():
    try:
        print version
        print sys.platform
        print sys.version_info
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise     



def function_Connect():
    try:
        connect(username,password,url)
        return 'success'
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise     
    
def function_Authenticator():
    try:
        edit()
        startEdit()
        cd('/SecurityConfiguration/domainNewJMS/Realms/myrealm')
        cmo.createAuthenticationProvider('SAML_tcleyman_Authenticator', 'weblogic.security.providers.saml.SAMLAuthenticator')
        cd('/SecurityConfiguration/domainNewJMS/Realms/myrealm/AuthenticationProviders/SAML_tcleyman_Authenticator')
        cmo.setControlFlag('SUFFICIENT')
        save()
        activate(block="true")
        return 'success'
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise     

def function_IdentityAsserter():
    try:
        edit()
        startEdit()    
        cd('/SecurityConfiguration/domainNewJMS/Realms/myrealm')
        cmo.createAuthenticationProvider('SAML_tcleyman_IdAsserterV2', 'com.bea.security.saml2.providers.SAML2IdentityAsserter')
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

'''
print 'configuring SAML Authenticator ....'
print function_Authenticator()

print 'configuring SAML Identity Asserter ...'
print function_IdentityAsserter()
'''

print 'script finished successfully'