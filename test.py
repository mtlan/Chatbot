# import smtplib

# sender_email = "maidangjapan@gmail.com"
# rec_email = "beu123k@gmail.com"
# password = input(str("Please enter your password : "))
# message = "Hey, this was sent using python"

# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(sender_email, password)
# print("Login success")
# server.sendmail(sender_email, rec_email, message)
# print("Email has been sent to ", rec_email)

import smtplib

mailto = ""
doctor = ""
date = ""
time = ""
name = ""
report = ""
gmailaddress = ""
gmailpassword = ""

sub = "Đã xác nhận: Đã đặt lịch hẹn với "
if (len(report) == 0): report = "Checkup"
msag = "Xin chào " + name + ",\n\nCuộc hẹn của bạn đã được đặt thành công với " + doctor + "\n\nNgày : " + date + "\nThời gian : " + time + "\nVấn đề : " + report + "\n\nCảm ơn bạn đã sử dụng Bác Sĩ Chatbot."
msg = 'Subject: {}\n\n{}'.format(sub, msag)

sub2 = "Cuộc hẹn đã được đặt trước với "+ doctor + " on "+ date
msag2 = "Email bệnh nhân: "+ mailto + "\n\nBáo cáo: " + report
msg2 = 'Subject: {}\n\n{}'.format(sub2, msag2)

mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
mailServer.starttls()
mailServer.login(gmailaddress , gmailpassword)
mailServer.sendmail(gmailaddress, mailto , msg.encode("utf8"))
print("Email người dùng đã được gửi!")
mailServer.sendmail(gmailaddress, gmailaddress , msg2.encode("utf8"))
print("Email quản trị viên đã gửi!")
mailServer.quit()

