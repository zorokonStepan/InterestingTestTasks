import smtplib


class EmailYandex:
    """A class EmailYandex for sending a letter to an employee"""
    __server: str = "smtp.yandex.ru"
    __port: int = 587
    __charset = 'Content-Type: text/plain; charset=utf-8'  # encoding of the letter
    __mime = 'MIME-Version: 1.0'  # encoding of the letter
    __encode = 'utf-8'

    def __init__(self, user, passwd):
        # mail service data
        self.user = user
        self.passwd = passwd

    def send_message(self, adress: str, subject: str, message: str):
        """
        adress - the addressee of the letter
        subject - subject of the letter
        message - the text of the letter
        """
        # forming the body of the letter
        body = "\r\n".join((f"From: {self.user}", f"To: {adress}", f"Subject: {subject}", self.__mime, self.__charset,
                              "", message))
        try:
            # connecting to the mail service
            smtp = smtplib.SMTP(self.__server, self.__port)
            smtp.starttls()
            smtp.ehlo()
            # log in to the mail server
            smtp.login(self.user, self.passwd)
            # trying to send a letter
            smtp.sendmail(self.user, adress, body.encode(self.__encode))
            smtp.quit()
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
