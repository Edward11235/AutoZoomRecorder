class DataBase:
    def __init__(self, filename):
        self.filename = filename

        if filename == "info.txt":
            self.btnlist = None
            self.file = None
            self.load()
        else:
            self.userlist = None
            self.userfile = None
            self.zoomid = "zoom id (delete it and write yours)"
            self.zoompassword = "zoom password (delete it and write yours)"
            self.meetingid = "meeting id (delete it and write yours)"
            self.load_user()

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
                f.write(btn + ";" + self.btnlist[btn][0] + ";" + self.btnlist[btn][1] + "\n")

    def load_user(self):
        self.file = open(self.filename, "r")
        self.userlist = []

        if self.file != "":
            for line in self.file:
                self.zoomid, self.zoompassword, self.meetingid = line.split(";")
            #读取后加到my.kv的input里面,在main class里进行

        self.file.close()

    def add_user(self, id, password, meetingid):
        id = str(id)
        password = str(password)
        meetingid = str(meetingid)
        self.userlist = [id, password, meetingid]
        self.save_user()
        return 1

    def save_user(self):
        with open(self.filename, "w") as u:
            u.write(self.userlist[0] + ";" + self.userlist[1] + ";" + self.userlist[2] + "\n")