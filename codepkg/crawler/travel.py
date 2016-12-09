class City:
    id=0
    province=''
    cname=''
    clevel=''


    def __init__(self,id=0,province='',cname='',clevel=''):
        self.id = id
        self.province = province
        self.cname = cname
        self.clevel = clevel

    def  output(self):
        print '%d, %s, %s, %s'%(self.id,self.province, self.cname, self.clevel)