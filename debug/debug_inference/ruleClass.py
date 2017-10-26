class Rule:
    
    def __init__(self, head, body):
        self.head = head
        self.body = body
    
    def getHead(self):
        return self.head
    
    def getBody(self):
        return self.body
    
    def getTextRule(self):
        textRule = ''
        index = 0
        for bodyAtom in self.body:
            if (index==0):
                textRule+=bodyAtom.getTextAtom()
            else:
                textRule+= '&'+bodyAtom.getTextAtom()
            index+=1
        textRule += '->'+self.head.getTextAtom()
        return textRule