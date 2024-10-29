from abc import ABC, abstractmethod

class AbstractLayout(ABC):
    
    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.children = []
    
    @abstractmethod
    def buildLayout(self):
        pass
    
    @abstractmethod
    def buildCallbacks(self):
        pass