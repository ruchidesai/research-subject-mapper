import pysftp as sftp
import sys
import os
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin')


class sftp_transactions:
    """A class for handling the sftp transactions. This class contains
    functions for getting a file from sftp server and putting a file
    to a sftp server"""

    def __init__(self):
        self.data = []
        
    def send_file_to_uri(self, site_URI, uname, password, remotepath, localpath, contact_email):
        '''This function puts the specified file to the given uri.
        Authentication is done using the uname and password
        remotepath - the path where the file needs to be put
        localpath - the path where the file is picked from
        contact_email - the email of the concerned authority to mail to incase of failed
        transaction
        
        '''
        # make a connection with uri and credentials
        connect = sftp.Connection(host=site_URI, username=uname, password=password)

        # import here to eliminate circular dependancy
        import generate_subject_map_input
        try:
            # put the file at the designated location in the server
            connect.put(localpath, remotepath)
            # close the connection
            connect.close()
        except Exception, e:
            # closing the connection incase there is any exception
            connect.close()
            '''Report should be sent to the concerned authority with the error
                message
            '''
            print 'Error sending file to '+site_URI
            print 'Check the credentials/remotepath/localpath/Server URI'
            generate_subject_map_input.send_report('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)
    pass

    def get_file_from_uri(self, site_URI, uname, password, remotepath, localpath, contact_email):
        '''This function gets the specified file to the given uri.
        Authentication is done using the uname and password
        remotepath - the path where the file needs to be put
        localpath - the path where the file is picked from
        contact_email - the email of the concerned authority to mail to incase of failed
        transaction
        
        '''
        # make a connection with uri and credentials
        connect = sftp.Connection(host=site_URI, username=uname, password=password)

        # import here to eliminate circular dependancy
        import generate_subject_map_input
        try:
            # get the file from the designated location in the server
            connect.get(remotepath, localpath)
            # close the connection
            connect.close()
        except Exception, e:
            # closing the connection incase there is any exception
            connect.close()
            '''Report should be sent to the concerned authority with the error
                message
            '''
            generate_subject_map_input.send_report('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)
    pass