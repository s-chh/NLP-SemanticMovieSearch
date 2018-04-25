class SemanticData:
    def __init__(self, root="", isEntity=False, isEvent=False, properties={}):
        self.root = root
        self.isEntity = isEntity
        self.isEvent = isEvent
        self.properties = properties
        self.weight = 0

    def toString(self):
        to_String =  "Root: " + self.root
        for property in self.properties.keys():
            to_String += ("   " + str(property).title() + ":" + str(self.properties[property]))
        to_String += "   Weight:"+str(self.weight)
        return to_String

    def setWeight(self):
        weight = 0
        for property in self.properties.keys():
            attributes = self.properties[property]
            for attribute in attributes:
                weight += 1
        # if not self.root == "":
        #     weight += 1
        self.weight = weight
