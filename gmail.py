import smtplib

def sendEmail( mailto, doctor, date, time, name, report ):
    # gmailaddress = "điền email"  # Địa chỉ email 
    # gmailpassword = "điền password"  # Mật khẩu gmail
    gmailaddress = "beu123k@gmail.com"  # Địa chỉ email 
    gmailpassword = "090861lan"  # Mật khẩu gmail

    sub = "Đã xác nhận: Đã đặt lịch hẹn với bác sĩ"
    if (len(report) == 0): report = "Checkup"
    msag = "Xin chào " + name + ",\n\nCuộc hẹn của bạn đã được đặt thành công với " + doctor + "\n\nNgày : " + date + "\nThời gian : " + time + "\n" + report + "\n\nCảm ơn bạn đã sử dụng Bác Sĩ Chatbot."
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
    return



