/*******************************************************************************
 * Copyright (c) 2015 Tom Cleymans
 *******************************************************************************/
package tcleyman;

import javax.jws.WebService;

@WebService(targetNamespace="http://tcleyman/")
public interface MyJMSWSI {
	 public String sayHello(String name);
	    
	    public String sayHello2(String name);

}
