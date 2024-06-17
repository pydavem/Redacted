""" a simple class to return information to the user about results of any redactions """


class Results:
    """ simple class to return results """

    def __init__(self):
        self.file = ''
        self.ips = 0
        self.logins = 0
        self.macs = 0
        self.machines = 0

    def add_file(self, file):
        """ add a new redacted file """
        self.files = file

    def add_ip(self):
        """ increment the ip value """
        self.ips += 1

    def add_login(self):
        """ increment the logins redacted counter """
        self.logins += 1

    def add_mac(self):
        """ increment the macs counter """
        self.macs += 1

    def add_machine(self):
        """ increment the machines counter """
        self.machines += 1
