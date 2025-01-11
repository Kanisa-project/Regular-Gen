import artstyle


class Meem(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        super(Meem, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.setup_checkbutton_choices(["da_fuq", "forever_alone", "LLOOOLL", "me_gusta", "mother_of_god",
                                        "oh_kay", "srsly", "troll_face"])
