'''
script created by tcleyman
script configures SAML Authenticator & SAML IdentityAsserter
script assumes that the WLS Admin Server is up and running
'''

'''
Need to fix this script in order to fix startup issue .. 

calling this script:
1. adapt env variables
2. invoke setDomainEnv.cmd
3. java weblogic.WLST C:\Users\tcleyman\git\EJBWS_tcleyman\EJBWS_tcleyman\wlst\script1_authenticator.py
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

def function_StartServer():
    '''
    function_StartServer() should start WLS
    and connect
    '''
    try:
        print 'starting WLS server'
        startServer('AdminServer',domainName,url,username,password,domainHome)
        #,block='true',60000)
        #,'-Dweblogic.wsee.policy.LoadFromClassPathEnabled=true'')
        connect(username,password,url)
        return 'success'
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
    
def function_DestroyExisting():
    '''
    function_DestroyExisting will remove existing config, for testing purposes
    '''
    try:
        edit()
        startEdit()
        cd('/SecurityConfiguration/domainNewJMS/Realms/myrealm')
        cmo.destroyAuthenticationProvider(getMBean('/SecurityConfiguration/domainNewJMS/Realms/myrealm/AuthenticationProviders/SAML_tcleyman_Authenticator'))
        cmo.destroyAuthenticationProvider(getMBean('/SecurityConfiguration/domainNewJMS/Realms/myrealm/AuthenticationProviders/SAML_tcleyman_IdAsserterV2'))
        save()
        activate(block="true")
        return 'success'
    except Exception, e:
        print e 
        print "Error while trying to save and/or activate!!!"
        dumpStack()
        raise     
    
def function_Restart():
    '''
    function_Restart should restart WLS after making config changes
    '''
    try:
        shutdown('AdminServer','Server', ignoreSessions='true')
        function_StartServer()
        return 'success'
    except Exception, e:
        print e 
        print "Error Restarting Server!!!"
        dumpStack()
        raise 
    
def function_Authenticator():
    '''
    function_Authenticator(): configure SAML Authenticator and set it to SUFFICIENT 
    '''
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
    '''
    function_IdentityAsserter(): configure a SAML Identity Asserter
    Note after this function the Server must be restarted
    '''
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

#print 'destroy existing config'
#print function_DestroyExisting()

#print 'restarting server'
#print function_Restart()

print 'configuring SAML Authenticator ....'
print function_Authenticator()

print 'configuring SAML Identity Asserter ...'
print function_IdentityAsserter()

#print 'restarting server'
#print function_Restart()

print 'script finished successfully'
print 'exiting ...'
disconnect()
exit()
