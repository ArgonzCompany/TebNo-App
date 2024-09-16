import os, sys
import uuid
import resources

class OSHandling(object):

    @staticmethod
    def styleHandling():
        # filename = os.path.join(os.path.dirname(__file__),'style.css')
        # return filename
        return OSHandling.resource_path('resources/style.css')
    
    @staticmethod
    def messageboxHandling():
        # filename = os.path.join(os.path.dirname(__file__),'messagebox.css')
        # return filename
        return OSHandling.resource_path('resources/messagebox.css')
    
    @staticmethod
    def templateHandling():
        # filename = os.path.join(os.path.dirname(__file__),'messagebox.css')
        # return filename
        return OSHandling.resource_path('resources/report.html')

    @staticmethod
    def resource_path(relative_path):

        try:
            base_path = sys._MEIPASS
        
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def get_mac_address():
        return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])




    


