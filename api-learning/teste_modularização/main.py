class Dbinfo:
    def __init__(self,dbuser,dbpassword,dbhost,dbtable_name):

        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbhost = dbhost
        self.dbtable_name = dbtable_name


class Api_requi:
    def __init__(self,api_key,api_url,data_return,cidade_api):
        self.api_key = api_key
        self.api_url = api_url
        self.data_return = data_return
        self.cidade_api =cidade_api