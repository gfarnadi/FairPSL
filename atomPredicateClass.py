

class AtomPredicate:
    
    def __init__(self, symbolName, arguments, isNegated):
        self.symbolName = symbolName
        self.isNegated = isNegated
        self.arguments = argarguments
    
    def getSymbolName(self):
        return self.symbolName
    
    def getIsNegated(self):
        return self.isNegated
    
    
    def getArguments(self):
        return self.arguments
    
    def getTextAtom(self):
        if self.isNegated:
            atomText = '~'+self.getSymbolName()+'('
        else:
            atomText = self.getSymbolName()+'('
        index = 0
        for arg in self.arguments:
            if (index==0):
                atomText+=arg
            else:   
                atomText+=','+arg
        
        atomText+=')'
        return atomText