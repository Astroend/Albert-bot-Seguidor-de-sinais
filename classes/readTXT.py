# Recebe a variável txt como o nome do arquivo txt, lê e converte para dict.

from datetime import datetime

class Read():
    def __init__(self, txt):
        self.file = txt # txt file
        self.to_list()


# Convert txt string to list.
    def to_list(self):
        self.sinal_list = []
        with open( self.file, "r", encoding="UTF-8") as file:
            for line in file:
                if line != "\n":
                    line = line.replace("\n", "")
                    self.sinal_list.append(line)
        return self.sinal_list

    def convert_time(self, time):
        if time[0] == "H":
            return int(time[1:]*60)
        else: 
            return int(time[1:])

# Convert list to dict.
    def convert(self):
        return_list = []
        for element in self.sinal_list:
            element_dict = {}
            element = element.split("-")
            for item in element:
                if len(item) == 6:
                    if "OTC" in element:
                        element_dict["Active"] = item + "-OTC"
                    else:
                        element_dict["Active"] = item
                if item.find(":") >= 0:
                    element_dict["Hour"] = item.split(":")
                if item.upper() == "CALL" or item.upper() == "PUT":
                    element_dict["Action"] = item
                if item.find("H") >= 0 or item.find("M") >= 0:
                    element_dict["Duration"] = self.convert_time(item)
                if item.find("/") >= 0 and len(item) == 5:
                    element_dict["Date"] = item.split("/")
            return_list.append(element_dict)
        return return_list