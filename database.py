import datetime

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.btnlist = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.btnlist = {}

        for line in self.file:
            btn_name, x_coor, y_coor = line.strip().split(";")
            self.btnlist[btn_name] = (x_coor, y_coor)

        self.file.close()

    def add_pos(self, btn_name, x_coor, y_coor):
        x_coor = str(x_coor)
        y_coor = str(y_coor)
        self.btnlist[btn_name.strip()] = (x_coor, y_coor)
        self.save()
        return 1

    def save(self):
        with open(self.filename, "w") as f:
            for btn in self.btnlist:
                f.write(btn + ";" + self.btnlist[btn][0] + ";" + self.btnlist[btn][1] + ";" + "\n")
