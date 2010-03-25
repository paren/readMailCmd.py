import poplib
import smtplib
import re
import os
import time

class RMC:
    def __init__(self):
        self.mailServer = {"smtp" : "smtp.gmail.com", "sPort" : 587, "pop" : "pop.gmail.com", "pPort" : 995}
        self.mailAccount = {"login" : "readmail.py@gmail.com", "pass" : "Your-password-here"}
        self.mailConf = {"fromAddrs" : "readmail.py@gmail.com"}
        self.subj = re.compile("Subject: ")
        self.fromM = re.compile("From: ")
        
    def sendMail(self, subject, toAddr, message):
        smtp = smtplib.SMTP(self.mailServer["smtp"], self.mailServer["sPort"])
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.mailAccount["login"], self.mailAccount["pass"])
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n") % (self.mailConf["fromAddrs"], toAddr, subject, message)
        smtp.sendmail(self.mailConf["fromAddrs"], toAddr, msg)
        smtp.quit()
        
    def readMail(self):
        pop = poplib.POP3_SSL(self.mailServer["pop"], self.mailServer["pPort"])
        pop.set_debuglevel(1)
        pop.user(self.mailAccount["login"])
        pop.pass_(self.mailAccount["pass"])
        numMessages = pop.stat()[0]
        for i in range(numMessages):
            for line in pop.retr(i + 1)[1]:
                fro = re.findall(self.fromM, line)
                sub = re.findall(self.subj, line)
                if fro:
                    toAddr = line.split(": ")[1]
                if sub:
                    print line
                    if len(line.split(": ")) > 1:
                        isCmd = line.split(": ")[1]
                        if isCmd.split("=")[0] == "Cmd":
                            start = time.ctime()
                            cmd = os.popen(isCmd.split("=")[1], "r")
                            self.sendMail(isCmd.split("=")[1], toAddr, start + "\r\n\r\n" + cmd.read() + time.ctime())
        pop.quit()

rmc = RMC()
rmc.readMail()