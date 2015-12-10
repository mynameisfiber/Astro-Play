import cherrypy
import simplejson

from gopigo import *
from grove_compass_lib import *

class Root(object):

    @cherrypy.expose
    def update(self):
        #print (cheerypy.request.headers)
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        
        body = simplejson.loads(rawbody)
        print(body)  #Look inside JSON string
        for key in body:  #Start iterating through JSON string
            # print(key) #debug print to see where we are in the dict
            #command=(body['cmd2']) #assign command to json command not need if for loop
            command=(body[key]) #assign command to json based on value of key which should be cmd1 etc. 
            # print(body['cmd2']) #Debug statement to value of cmd2 key
            print (command[0]) # Debug statement to see first character of command-key
            print(command[2:]) #Debug statement to see 3rd->len of command-key
            c=compass()  #shorten compass method
            divider=4    #factor to shorten how far the robot goes
            if command[0] == 'f':  #Forward dist primitive
                 dist=int(command[2:])
                 enc_tgt(1,1,dist)
                 fwd()
                 while read_enc_status() == 1: # Wait until fwd command completes by checking encoders
                     print(read_enc_status())
            elif command[0] == 'b': #Backward distance primitive
                 dist=int(command[2:])
                 enc_tgt(1,1,dist)
                 bwd()

            elif command[0]=='r':  #Rotate right if command if r
                angle=int(command[2:]) # Take angle from last half of string
                if angle >360 or angle <0:  #Check for angle out of bounds
                    print "Wrong angle"
                    # continue #Used with the try: loop
                    
                c.update()  # Query Compass (what is this really doing ?
                start=c.headingDegrees  #Assign starting angle
                target= (start+angle)%360 #Calculate destination angle
                right_rot() #Start Rotation
                while True:
                    current=c.headingDegrees #Check current angle
                    #if debug: #Copied from example
                    print start,target,current #Cooment out when done debugging
                    if target-start>0: #If in the 'positive' quadrant check surrent
                        if current>target: #current went past target
                            stop()
                            break;
                    else:
                        if current>target and current <start-5: #If in the negative quadrant check current
                            stop()
                            break;
                    c.update()
                    #time.sleep(.1)
                 
            elif command[0]=='x': #Stop robot primitives if the encoders don't work
                 stop()  # Stop all motors
             
        return "Updated %r." % (body,)

    @cherrypy.expose
    def shutdown(self):
        cherrypy.engine.exit()
        
    @cherrypy.expose
    def index(self):
        return """
<html>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type='text/javascript'>
function Update() {
    $.ajax({
      type: 'POST',
      url: "update",
      contentType: "application/json",
      processData: false,
      data: $('#updatebox').val(),
      success: function(data) {alert(data);},
      dataType: "text"
    });
}
</script>
<body>
<input type='textbox' id='updatebox' value='{}' size='20' />
<input type='submit' value='Update' onClick='Update(); return false' />
<a href="./shutdown">Shutdown server</a>
</body>
</html>
"""

if __name__ == '__main__':
     conf = {
         'global': {'server.socket_port' : 8081,'server.socket_host': '0.0.0.0'}
         ##'/': {
           #  'tools.sessions.on': True,
         #}
     }
cherrypy.quickstart(Root(), '/', conf)
