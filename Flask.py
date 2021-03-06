from flask import Flask, request, jsonify, escape, render_template, make_response, sessions
import os

from flask.globals import session           # import flask
import SVM
import json
import gmail

app = Flask(__name__)
doctor, date, time, mail = "","","",""
age1, gender, name = "","",""
pred, prt, speech = "","",""
problem, sym_duration = "",""
q1,q2,q3,q4,q5,q6 = 0,0,0,0,0,0
sym1,sym2,sym3 = "","",""
new_report, tips, soln = "","",""



# @app.route("/")                   # at the end point /
# def hello():                      # call method hello
# return "Hello World!"
@app.route('/Home')
def Home():
    return render_template('Home.html')

@app.route('/Home', methods=['POST'])
def Home_Value():
    global mail
    mail = request.form['mail']
    return render_template('Frame.html')

@app.route('/')
def index():
    if mail =="": return render_template('Home.html')
    else: return render_template('Frame.html')

@app.route('/Form')
def Form():
    if mail == "": return render_template('Home.html')
    else: return render_template('Form.html')

@app.route('/Chatbot')
def Chatbot():
    if mail == "": return render_template('Home.html')
    else: return render_template('Chatbot.html')

@app.route('/', methods=['POST'])
def getvalue():
    age = age1
    #sex = request.form['sex']
    sex = gender
    if sex == 'Nam': sex = 1
    elif sex == 'Nữ': sex = 0

    cp = request.form['cp']
    if cp == 'Typical Angina': cp = 0
    elif cp == 'Atypical Angina': cp = 1
    elif cp == 'Non-anginal Pain': cp = 2
    elif cp == 'Asymptomatic': cp = 3

    trestbps = request.form['trestbps']
    chol = request.form['chol']

    fbs = request.form['fbs']
    if fbs == 'Yes': fbs = 1
    elif fbs == 'No': fbs = 0

    restecg = request.form['restecg']
    if restecg == 'Normal': restecg = 0
    elif restecg == 'Having ST-T Wave Abnormality': restecg = 1
    elif restecg == 'Left Ventricular Hyperthrophy': restecg = 2

    thalach = request.form['thalach']

    exang = request.form['exang']
    if exang == 'Yes': exang = 1
    elif exang == 'No': exang = 0

    oldpeak = request.form['oldpeak']

    slope = request.form['slope']
    if slope == 'Upsloping': slope = 0
    elif slope == 'Flat': slope = 1
    elif slope == 'Downsloping': slope = 2

    ca = request.form['ca']

    thal = request.form['thal']
    if thal == 'Normal': thal = 1
    elif thal == 'Fixed Defect': thal = 2
    elif thal == 'Reversible Defect': thal = 3
    
    # lỗi không dự đoán vì đầu ra là chuỗi kí tự
    print(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
    global pred
    try:
        pred = SVM.svm_pred(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
    except Exception as e:
        print(type(e).__name__)
    global speech
    # global prt
    if pred == 0:
        speech = "Báo cáo của bạn trông ổn."
    if pred == 1:
        speech = "Bạn có thể đang có vấn đề tim mạch!"
    print(pred)
    return render_template('pass.html', n=pred, s=prt)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    # Get all the Query Parameter
    query_response = req["queryResult"]
    
    res = {  "fulfillmentText": "", }
    global name
    global gender
    global age1
    global sym1
    global sym2
    global new_report

    # Patient_Name
    # tên parameter trong diagflow
    if query_response.get("action") == "user_name":
        r = query_response.get("parameters")
        r1 = r.get("given_name")
        global name
        name = r1

    # Patient_Age
    if query_response.get("action") == "user_age":
        r = query_response.get("parameters")
        # note lỗi
        # age sẽ được lấy khi người dùng nhập tuổi
        r2 = r.get("age")
        r1 = r2.get("amount")
        global age1
        age1 = int(r1)

    # kiểm tra tuổi bệnh nhân (Checkup_Patient_gender)
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Checkup_Patient-custom":
        r = query_response.get("parameters")
        r1 = r.get("Gender")
        global gender
        gender = r1
        a1 = "OK" + name + "(" + str(age1) + "), Vui lòng điền vào biểu mẫu báo cáo ở phía bên phải ...."
        res = { "fulfillmentText": a1, }

    # Checkup_Patient_filling
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Checkup_Patient-custom.Checkup_Patient_gender-custom":
        a2 = "Cảm ơn " + name + ", sau khi phân tích thông tin bạn đã cung cấp cho chúng tôi, Hệ thống dự đoán rằng "+ speech +" Xin lưu ý, đây không phải là chẩn đoán. Hãy đến gặp bác sĩ nếu bạn nghi ngờ, hoặc nếu các triệu chứng của bạn trở nên tồi tệ hơn hoặc không cải thiện. Nếu tình hình của bạn nghiêm trọng, hãy luôn gọi dịch vụ khẩn cấp. Bạn có muốn đặt lịch hẹn với bác sĩ không?" 
        res = {  "fulfillmentText": a2, }
        
    ############ Suffering Patient ##########################
    
    # Suffering_Patient
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom":
        # Main Problem
        global problem
        global soln
        r = query_response.get("parameters")
        problem = r.get("Symptoms")
        if problem == "Tức Ngực": soln = "Thuốc giảm đau, chẳng hạn như aspirin, có thể giúp giảm đau tim / ngực liên quan đến các trường hợp ít nghiêm trọng hơn. Khi cơn đau tim ập đến, nằm ngay lập tức với đầu nâng cao hơn cơ thể có thể giúp giảm đau. Tư thế hơi thẳng đứng sẽ giúp ích khi cơn đau do trào ngược."
        elif problem == "Cao Huyết Áp": soln = "Huyết áp thường tăng khi cân nặng (Béo phì) tăng. Hoạt động thể chất thường xuyên như 150 phút mỗi tuần có thể làm giảm huyết áp của bạn khoảng 5 đến 8 mm Hg nếu bạn bị huyết áp cao. Ăn một chế độ ăn nhiều ngũ cốc nguyên hạt, trái cây, rau và các sản phẩm từ sữa ít béo, đồng thời loại bỏ chất béo bão hòa và cholesterol có thể làm giảm huyết áp của bạn lên đến 11 mm Hg nếu bạn bị huyết áp cao. Căng thẳng mãn tính và hút thuốc cũng có thể góp phần làm tăng huyết áp, vì vậy hãy tránh điều đó."
        elif problem in("vấn đề về hô hấp", "khó thở"): soln = "Hít vào sâu bằng bụng và thở ngửa cũng có thể giúp kiểm soát tình trạng khó thở của bạn. Tìm một vị trí thoải mái và được hỗ trợ để đứng hoặc nằm có thể giúp bạn thư giãn và lấy lại hơi thở. Hít hơi có thể giúp đường mũi thông thoáng, giúp thở dễ dàng hơn. Uống cà phê đen có thể giúp điều trị chứng khó thở, giảm mệt mỏi ở các cơ đường thở. Thừa cân cũng có thể gây ra gián đoạn hô hấp khi bạn ngủ (ngưng thở khi ngủ)."
        elif problem in("Buồn ngủ", "ngủ", "giấc ngủ"): soln = "Thiết lập cho mình một giấc ngủ thoải mái: Hãy tuân theo một lịch trình ngủ / thức đều đặn. Tắt TV, máy tính và các thiết bị khác trước khi đi ngủ. Giữ phòng ngủ của bạn mát mẻ và tối. Tránh uống rượu trước khi đi ngủ và uống cà phê vào buổi chiều hoặc buổi tối. Tập thể dục mỗi sáng."
        
    # Suffering_Patient_symp_dur
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom":
        # Duration
        global sym_duration
        sym_duration = query_response.get("queryText")
    
    # Hỏi thông tin về căn bệnh
    # Suffering_Patient_Q2
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom":
        # Q. Heart Disease
        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q1
        if r1 == 'Có': q1 = 1
        
    # Suffering_Patient_Q3
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom.Suffering_Patient_Q2-custom":
        # Q. Diabetes
        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q2
        if r1 == 'Có': q2 = 1
        
    # Suffering_Patient_Q4
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom.Suffering_Patient_Q2-custom.Suffering_Patient_Q3-custom":
        # Q. High Blood Pressure
        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q3
        if r1 == 'Có': q3 = 1
        
    # Suffering_Patient_Q5
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom.Suffering_Patient_Q2-custom.Suffering_Patient_Q3-custom.Suffering_Patient_Q4-custom":
        # Q. Chronic Obstructive Lung Disease/Asthma
        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q4
        if r1 == 'Có': q4 = 1
        
    # Suffering_Patient_Q6
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom.Suffering_Patient_Q2-custom.Suffering_Patient_Q3-custom.Suffering_Patient_Q4-custom.Suffering_Patient_Q5-custom":
        # Q. Smoking
        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q5
        if r1 == 'Có': q5 = 1
        
    # Suffering_Patient_sym1
    if query_response.get("action") == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.Suffering_Patient-custom.Suffering_Patient_symp_dur-custom.Suffering_Patient_Q2-custom.Suffering_Patient_Q3-custom.Suffering_Patient_Q4-custom.Suffering_Patient_Q5-custom.Suffering_Patient_Q6-custom":

        r = query_response.get("parameters")
        r1 = r.get("Confirmation")
        global q6
        if r1 == 'Có': q6 = 1
        
    # Suffering_Patient_sym2
    if query_response.get("action") == "symp1":
        ''' Q. - Đau ngực khi thở vào.
            - Đau rát ở ngực / bụng trên.
            - Đau ngực do ấn vào lồng ngực.
            - Đau ngực nặng hơn khi cử động. 
            - không có '''
        global sym1
        sym1 = query_response.get("queryText")
    
    # Suffering_Patient_sym3
    if query_response.get("action") == "Suffering_Patient_sym2.Suffering_Patient_sym2-custom":
        ''' Q. - Đau tức ngực khi nghỉ ngơi. 
            - Đau ngực đột ngột. 
            - Khó thở. 
            - Thở nhanh hoặc nông. 
            - không có ''' 
        global sym2
        sym2 = query_response.get("queryText") 
        
    # Suffering_Patient_sym_final
    if query_response.get("action") == "Suffering_Patient_sym2.Suffering_Patient_sym2-custom.Suffering_Patient_sym3-custom":
        ''' Q. - Cảm thấy tim của bạn đang đập nhanh hoặc lệch nhịp.
            - Đau ngực lan xuống cánh tay trái.
            - Đau ngực lan tỏa khi gắng sức.
            - Đau khớp / bụng. 
            - không có
            
            - Tức ngực.
            - Mệt mỏi bất thường.
            - Sự lo ngại .
            - Đau ngực lan rộng quai hàm. 
            - không có '''
        global sym3
        sym3 = query_response.get("queryText")
        
        ###### Create Report ############
        # sym_duration về thời gian bị mắc
        # nếu chọn có thì xuất ra phần đã hỏi
        new_report = ""
        new_report += "Tóm tắt: Bạn đang có vấn đề về / đang bị "+problem+" trong "+sym_duration+"."
        if q1 == 1: new_report += "Bạn đã bị bệnh tim trước đây, "
        if q2 == 1: new_report += "Bạn bị / mắc bệnh tiểu đường, "
        if q3 == 1: new_report += "Bạn bị / bị cao huyết áp, "
        if q4 == 1: new_report += "Bạn đã bị hen suyễn HOẶC bệnh phổi tắc nghẽn mãn tính, "
        if q5 == 1: new_report += "Bạn đang hút thuốc (hoặc đã từng hút thuốc), "
        if q6 == 1: new_report += "Bạn đã / đang mắc: Đột quỵ não HOẶC Bệnh thận HOẶC Béo phì, "
        if sym1 not in("none","None") or sym2 not in("none","None") or sym3 not in("none","None"): new_report += "và cũng có các triệu chứng như "
        if sym1 not in("none","None"): new_report += sym1+", "
        if sym2 not in("none","None"): new_report += sym2+", "
        if sym3 not in("none","None"): new_report += sym3
        if (q1,q2,q3,q4,q5,q6) == 0: new_report += "Bạn không có bất kỳ triệu chứng đã đề cập ở trên!"
    
    # phần khai báo tên sau khi kết thúc phiên tư vấn và nhập thông tin
    # Suffering_Patient_sym_report_filling
    if query_response.get("action") == "Suffering_Patient_sym2.Suffering_Patient_sym2-custom.Suffering_Patient_sym3-custom.Suffering_Patient_sym_final-custom.Suffering_Patient_sym_report_yes-custom":
        r = query_response.get("parameters")
        name = r.get("given-name")
        gender = r.get("Gender")
        r2 = r.get("age")
        r1 = r2.get("amount")
        age1 = int(r1)
        # print("Bệnh nhân:", name, age1, gender )
        
    # Suffering_Patient_sym_report_results
    if query_response.get("action") == "Suffering_Patient_sym2.Suffering_Patient_sym2-custom.Suffering_Patient_sym3-custom.Suffering_Patient_sym_final-custom.Suffering_Patient_sym_report_yes-custom.Suffering_Patient_sym_report_filling-custom":
        ans2 = "Cảm ơn " + name + ", sau khi phân tích thông tin bạn đã cung cấp cho chúng tôi, Hệ thống dự đoán rằng "+ speech +" "+ new_report + ". Một số cách bạn có thể tránh vấn đề này là: " + soln + "--> Xin lưu ý, đây không phải là chẩn đoán. Luôn đến gặp bác sĩ nếu bạn nghi ngờ, hoặc nếu các triệu chứng của bạn trở nên tồi tệ hơn hoặc không cải thiện. Nếu tình hình của bạn nghiêm trọng, hãy luôn gọi dịch vụ khẩn cấp. Bạn có muốn đặt lịch hẹn với bác sĩ không?"
        res = {  "fulfillmentText": ans2, }
    
    # Suffering_Patient_sym_report_no nếu ko sẽ cho lời khuyên
    if query_response.get("action") == "Suffering_Patient_sym2.Suffering_Patient_sym2-custom.Suffering_Patient_sym3-custom.Suffering_Patient_sym_final-custom":
        r = "OK, "+ new_report + ". Một số cách bạn có thể tránh vấn đề này là: " + soln + "--> Xin lưu ý, đây không phải là chẩn đoán. Luôn đến gặp bác sĩ nếu bạn nghi ngờ, hoặc nếu các triệu chứng của bạn trở nên tồi tệ hơn hoặc không cải thiện. Nếu tình hình của bạn nghiêm trọng, hãy luôn gọi dịch vụ khẩn cấp. Bạn có muốn đặt lịch hẹn với bác sĩ không?"
        res = {  "fulfillmentText": r, }
        
    ######## DOCTOR ##########
    
    # app_date_time
    if query_response.get("action") == "doctors_list.doctors_list-custom":
        r1 = query_response.get("queryText")
        global doctor
        doctor = r1
        
    
    # app_booked
    if query_response.get("action") == "doctors_list.doctors_list-custom.app_date_time-custom":
        r = query_response.get("parameters")
        r1 = r.get("date")
        r2 = r.get("time")
        global date
        global time
        date = r1
        time = r2
        #print("Date: ", date, "   Time: ", time)
        gmail.sendEmail( mail, doctor, date, time, name, new_report )
        
    return res
        

if __name__ == "__main__":               
    port = int(os.getenv('PORT', 5000))
    # debug=True giống như hot reloading
    app.run(debug=True, port=port, host='0.0.0.0')        