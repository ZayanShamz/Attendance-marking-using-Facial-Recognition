import os
import face_recognition as fr
import cv2
import pymysql
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session
import threading


app = Flask(__name__)
app.secret_key = "scene aan"


con = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='attendance')
cmd = con.cursor()

res = 'invalid'
knownEncodings = []
nameList = []

presentList = []


def check(clss):
    path = 'static/classes/' + clss
    img_names = os.listdir(path)

    for i in img_names:
        imgTest = fr.load_image_file(os.path.join(path, i))
        # imgTest=cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
        encodeImgTest = fr.face_encodings(imgTest)[0]
        knownEncodings.append(encodeImgTest)

        split = os.path.splitext(i)  # to remove only the extension
        nameList.append(split[0])


def faceCheck():
    global res, presentList, nameList
    res = 'invalid'
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        resizeImg = cv2.resize(img, (0, 0), None, .25, .25)
        resizeImg = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2RGB)

        curFaces = fr.face_locations(resizeImg)
        encodeCurFaces = fr.face_encodings(resizeImg, curFaces)

        for faceEncode, faceLoc in zip(encodeCurFaces, curFaces):
            matches = fr.compare_faces(knownEncodings, faceEncode)
            faceDist = fr.face_distance(knownEncodings, faceEncode)

            matchIndex = np.argmin(faceDist)
            name = 'unknown'

            if matches[matchIndex] and faceDist[matchIndex] < 0.5:
                name = nameList[matchIndex]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2+25), (x2, y2), (0, 255, 0), -1)
                cv2.putText(img, name, (x1 + 6, y2+20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
                if name not in presentList:
                    presentList.append(name)
                else:
                    pass
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,0, 255), 2)
                cv2.rectangle(img, (x1, y2 + 25), (x2, y2), (0, 0, 255), -1)
                cv2.putText(img, name, (x1 + 6, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)
        #  need to adjust font

        cv2.imshow('Say Cheese :)', img)

        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def attendance(clss):
    global presentList, knownEncodings, nameList
    print("present", clss, presentList)
    cmd.execute(f"INSERT INTO `{clss}`(`date`,`time`) VALUES(CURDATE(),CURTIME())")
    aid = con.insert_id()
    con.commit()
    cmd.execute("SELECT `name` FROM `0_students` WHERE `class`='"+clss+"'")
    stud = cmd.fetchall()
    print(stud)

    for i in stud:
        if i[0] in presentList:
            cmd.execute(f"UPDATE `{clss}` SET `{i[0]}`=1 where `id`='"+str(aid)+"' ")
            con.commit()
        else:
            cmd.execute(f"UPDATE `{clss}` SET `{i[0]}`=0 where `id`='"+str(aid)+"' ")
            con.commit()

    print("Marked")
    presentList = []
    knownEncodings = []
    nameList = []


def main(clss):
    check(clss)
    threading.Thread(target=faceCheck).start()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']
        # print(f"entered Username = {user}, Password = {passwd}")

        cmd.execute("SELECT * FROM `0_login` WHERE `username`='"+user+"' AND `password`='"+passwd+"' ")
        acc = cmd.fetchone()
        if acc:
            usertype = acc[3]
            session['fac'] = acc[0]
            session['ut'] = usertype
            if usertype == 'faculty':
                return redirect(url_for('faculty'))
            else:
                return redirect(url_for('admin'))
        else:
            return "<script>alert('Username Or Password in Incorrect');window.location='/'</script>"
    else:
        return render_template('login.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    fac = session['fac']
    cmd.execute("SELECT `class` FROM `0_class` WHERE `fac`='"+str(fac)+"'")
    clss = cmd.fetchone()[0]
    print(clss)
    print("starting camera")
    main(clss)
    return redirect(request.referrer)


@app.route('/submit')
def submit():
    fac = session['fac']
    cmd.execute("SELECT `class` FROM `0_class` WHERE `fac`='"+str(fac)+"'")
    clss = cmd.fetchone()[0]
    attendance(clss)
    return redirect(request.referrer)


@app.route('/history')
def history():
    fac = session['fac']
    cmd.execute("SELECT `class` FROM `0_class` WHERE `fac`='"+str(fac)+"'")
    clss = cmd.fetchone()[0]

    cmd.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME ='{clss}'")
    head = cmd.fetchall()
    heads = [i[0] for i in head]
    print(heads)

    cmd.execute(f"SELECT * FROM `{clss}`")
    result = cmd.fetchall()
    print(result)

    return render_template('attendance.html', head=heads, data=result)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/faculty')
def faculty():
    return render_template('faculty.html')


@app.route('/addClass', methods=['GET','POST'])
def addClass():
    if request.method == 'POST':
        cname = request.form['c']
        fac = request.form['fac']
        cmd.execute(f"CREATE TABLE `{cname}`(`id` INT NOT NULL AUTO_INCREMENT,`date` VARCHAR(50),`time` VARCHAR(50), \
        PRIMARY KEY (`id`));")
        cmd.execute("INSERT INTO `0_class`(`class`,`fac`) VALUE('"+cname+"', '"+fac+"')")
        con.commit()

        directory = cname
        parent_dir = "static\\classes\\"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        return redirect(url_for('admin'))
    else:
        cmd.execute("SELECT `login_id`,`name` FROM `0_faculty`")
        result = cmd.fetchall()
        return render_template('addClass.html', data=result)


@app.route('/studentRegister', methods=['GET', 'POST'])
def studentRegister():
    if request.method == 'POST':
        reg = request.form['reg'].upper()
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        addr = request.form['address']
        clss = request.form['class']
        f = request.files['photo']

        spl = str.split(f.filename, '.')
        photo = name + '.' + spl[len(spl) - 1]

        path = "static\\classes\\" + clss + "\\" + photo
        f.save(path)

        cmd.execute("INSERT INTO `0_students` VALUES(NULL, '"+reg+"', '"+name+"', '"+dob+"', '"+gender+"', '"+email+"', \
        '"+phone+"', '"+addr+"', '"+clss+"', '"+photo+"')")
        con.commit()

        cmd.execute(f"ALTER TABLE {clss} ADD COLUMN `{name}` INT(15)")
        con.commit()

        return "<script>alert('Registered');window.location='/studentRegister'</script>"
    else:
        user = session['ut']
        cmd.execute("SELECT `class` FROM `0_class`")
        classs = cmd.fetchall()
        return render_template('student-register.html', data=classs, ut=user)


@app.route('/studentList', methods=['GET','POST'])
def studentList():
    user = session['ut']
    fac = session['fac']
    if request.method == 'POST':
        thing = 1
        name = request.form['search']
        if user == 'admin':
            cmd.execute("SELECT *, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
            FROM `0_students` WHERE `name` LIKE '%"+name+"%' ")
            result = cmd.fetchall()
            return render_template('student-list.html', data=result, ut=user, val=thing)
        else:
            cmd.execute("SELECT `0_students`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age FROM \
            `0_students`,`0_class` WHERE `0_students`.`class`=`0_class`.`class` AND `0_class`.`fac`=3 AND `name` LIKE '%"+name+"%' ")
            result = cmd.fetchall()
            return render_template('student-list.html', data=result, ut=user, val=thing)
    else:
        thing = 0
        if user == 'admin':
            cmd.execute("SELECT `0_students`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age FROM `0_students`")
            students = cmd.fetchall()
            return render_template('student-list.html', data=students, ut=user, val=thing)
        else:
            cmd.execute("SELECT `0_students`.*, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age FROM \
            `0_students`, `0_class` WHERE `0_students`.`class`=`0_class`.`class` AND `0_class`.`fac`='"+str(fac)+"'")
            students = cmd.fetchall()
            return render_template('student-list.html', data=students, ut=user, val=thing)


@app.route('/removeStudent/<sid>')
def removeStudent(sid):
    cmd.execute("SELECT `name`,`photo`,`class` FROM `0_students` WHERE `id`='"+sid+"'")
    name, photo, clss = cmd.fetchone()

    cmd.execute("DELETE FROM `0_students` WHERE `id`='"+sid+"'")
    cmd.execute(f"ALTER TABLE `{clss}` DROP COLUMN `{name}`")
    os.remove(f'static\\classes\\{clss}\\{photo}')
    con.commit()
    return redirect(request.referrer)


@app.route('/facultyRegister', methods=['GET', 'POST'])
def facultyRegister():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        qual = request.form['qual']
        dep = request.form['dep']
        exp = request.form['exp']
        addr = request.form['address']

        cmd.execute("INSERT INTO `0_login` VALUES(NULL, '"+email+"', '"+phone+"', 'faculty')")
        lid = str(con.insert_id())

        cmd.execute("INSERT INTO `0_faculty` VALUES(NULL, '"+lid+"', '"+name+"', '"+dob+"', '"+gender+"', '"+email+"', '"+phone+"', '"+qual+"', '"+dep+"', '"+exp+"', '"+addr+"')")
        con.commit()

        return "<script>alert('Registered');window.location='/admin'</script>"
    else:
        user = session['ut']
        return render_template('faculty-register.html',ut=user)


@app.route('/facultyList', methods=['GET','POST'])
def facultyList():
    if request.method == 'POST':
        thing = 1
        name = request.form['search']
        cmd.execute("SELECT *, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age \
        FROM `0_faculty` WHERE `name` LIKE '%"+name+"%' ")
        result = cmd.fetchall()
        return render_template('faculty-list.html', data=result, val=thing)
    else:
        thing = 0
        cmd.execute("SELECT *, DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(),`dob`)), '%Y') + 0 AS age FROM `0_faculty`")
        result = cmd.fetchall()
        return render_template('faculty-list.html', data=result, val=thing)


@app.route('/removeFaculty/<lid>')
def removeFaculty(lid):
    cmd.execute("DELETE FROM `0_login` WHERE `login_id`='"+lid+"'")
    cmd.execute("DELETE FROM `0_faculty` WHERE `login_id`='"+lid+"'")
    con.commit()
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
