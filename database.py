from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, or_, and_, func, asc, desc
from datetime import datetime
import datetime as dt
import jdatetime as jd
from unidecode import unidecode
engine = create_engine('sqlite:///TebNo.db', echo=True)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
Base = declarative_base()
# session = Session()


class Patient (Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    lastname = Column(String(35), nullable=False)
    phoneNumber = Column(String(20), unique=True)
    nationalCode = Column(String(11), unique=True)
    birth_date = Column(Date, nullable=False, default=datetime.now().date())
    visits = relationship('Visit', cascade='all', back_populates='patient')

class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    visit_date = Column(Date, nullable=False)
    visit_hour = Column(String(8), nullable=False)
    description = Column(String(250))
    status = Column(Integer, default=1)
    patient = relationship('Patient', back_populates='visits')


    






class PatientOperations(object):

    
    @staticmethod
    def addPatient(name, lastname, phoneNumber, nationalCode, birth_date):

        Session = sessionmaker(bind=engine)
        session = Session()
        
        if(name == '' or lastname == '' or phoneNumber == '' or nationalCode == '' or birth_date == ''):
            return f"فیلدهای اساسی را خالی گذاشته‌اید. آن‌ها را پر کنید."
        
        if len(birth_date) !=10:
             return f"تاریخ به درستی وارد نشده است."

        date_format = birth_date.split('/')

        if not(int(date_format[1])>=1 and int(date_format[1])<=12) or not(int(date_format[2])>=1 and int(date_format[2])<=31):
            return f"فرمت تاریخ را رعایت نکرده‌اید."
        
        if len(nationalCode) !=10:
            return f"کد ملی ۱۰ رقمی است. مقدار را درست وارد کنید."  
        
        patient = session.query(Patient).filter(or_(Patient.phoneNumber == phoneNumber, Patient.nationalCode == nationalCode)).first()

        if(patient):
            return f"فردی با این کد ملی یا شماره همراه وجود دارد."
        
        newPatient = Patient()
        newPatient.name = name
        newPatient.lastname = lastname
        newPatient.phoneNumber = phoneNumber
        newPatient.nationalCode = nationalCode
        newPatient.birth_date = PatientOperations.convert_to_gregorian(birth_date)
        session.add(newPatient)
        session.commit()
        session.close()
        
        return f"بیمار با مشخصات مورد نظر ثبت شد."
    
    @staticmethod
    def convert_to_gregorian(date):
        date=jd.datetime.strptime(date, '%Y/%m/%d').togregorian()
        return date
    
    @staticmethod
    def convert_to_jalali(date):
        date=jd.date.fromgregorian(day=date.day, month=date.month, year=date.year)
        return date
    
    @staticmethod
    def create_date(birth_date):
        birthDate = datetime.strptime(birth_date, '%Y/%m/%d').date()
        return birthDate

    @staticmethod
    def show_patients():
        Session = sessionmaker(bind=engine)
        session = Session()

        patients = session.query(Patient).with_entities(Patient.name, Patient.lastname, Patient.nationalCode, Patient.phoneNumber)
        session.close()
        patients_list=[]
        if (patients):
            for patient in patients:
                patient_list=[]
                for col in patient:
                    patient_list.append(col)
                patients_list.append(patient_list)
            return patients_list
        return list([])
    
    @staticmethod
    def show_patient(ncode):
        Session = sessionmaker(bind=engine)
        session = Session()
        patient = session.query(Patient).filter(Patient.nationalCode == ncode).first()
        session.close()

        if(patient):
            return patient
    
    @staticmethod
    def editPatient(name, lastname, phoneNumber, nationalCode, birth_date, patient_ncode):
        Session = sessionmaker(bind=engine)
        session = Session()
        patient_edit=session.query(Patient).filter(Patient.nationalCode == patient_ncode).first()
        patients = session.query(Patient).all()

        if(patient_edit):
            
            if(name == '' or lastname == '' or phoneNumber == '' or nationalCode == '' or birth_date == ''):
                return f"فیلد‌های اساسی خالی است. به روز رسانی منتفی است."
            
            if len(birth_date) !=10:
                return f"تاریخ به درستی وارد نشده است."

            date_format = birth_date.split('/')
            if not(int(date_format[1])>=1 and int(date_format[1])<=12) or not(int(date_format[2])>=1 and int(date_format[2])<=31):
                return f"فرمت تاریخ را رعایت نکرده‌اید."
            
            if len(nationalCode) !=10:
                return f"کد ملی ۱۰ رقمی است. مقدار را درست وارد کنید."  
            
            for patient in patients:
                if patient.nationalCode  == nationalCode and patient!=patient_edit:
                    return f"شما به اشتباه در حال ویرایش فرد دیگری هستید."
                if patient.phoneNumber  == phoneNumber and patient!=patient_edit:
                    return f"شما به اشتباه در حال ویرایش فرد دیگری هستید."
            patient_edit.name = name
            patient_edit.lastname = lastname
            patient_edit.phoneNumber = phoneNumber
            patient_edit.nationalCode = nationalCode
            patient_edit.birth_date = PatientOperations.convert_to_gregorian(birth_date)
            session.commit()
            session.close()

            return f"به روز رسانی انجام شد."
        return f"به روز رسانی با مشکل روبرو شد."
    
    @staticmethod
    def deletePatient(patient_ncode):
        Session = sessionmaker(bind=engine)
        session = Session()
        patient = session.query(Patient).filter(Patient.nationalCode == patient_ncode).first()

        if(patient):
            session.delete(patient)
            session.commit()
            session.close()
            return f"بیمار مورد نظر حذف شد."
        session.close()
        return f"در حذف بیمار، مشکل ایجاد شد."
    
    @staticmethod
    def return_age(date):
        now = dt.datetime.now().date()
        return int((now - date).days/365)
    
    
    @staticmethod
    def show_patients_ages():
        Session = sessionmaker(bind=engine)
        session = Session()
        patients = session.query(Patient).all()
        session.close()
        
        if(patients):
            patients_ages = []
            for patient in patients:
                patients_ages.append(PatientOperations.return_age(patient.birth_date))
            return patients_ages
        return None
    
    @staticmethod
    def patient_info_file(ncode):
        
        Session = sessionmaker(bind=engine)
        session = Session()
        patient = session.query(Patient).filter(Patient.nationalCode == ncode).first()

        visits = list()

        args = {
            'name': patient.name,
            'lastname': patient.lastname,
            'phoneNumber': patient.phoneNumber,
            'nationalCode': patient.nationalCode
        }

        for visit in patient.visits:
            if visit.status == 2:
                visits.append((visit.visit_hour, PatientOperations.convert_to_jalali(visit.visit_date).strftime('%Y-%m-%d'), visit.description))
        
        args['visits'] = visits

        session.close()

        return (args) 
    


    

    
    # @staticmethod
    # def patientsVisistsList():

    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     patients = session.query(Patient).with_entities(Patient.lastname, Patient.nationalCode)
    #     session.close()

    #     patients_list=[]
    #     if(patients):
    #         for patient in patients:
    #             patients_list.append(f"{patient.lastname} - {patient.nationalCode}")
    #         return patients_list
    #     return list([])
        


class VisitOperations(object):

    @staticmethod
    def addVisit(ncode, hour, date ):

        if (hour == '' or date == ''):

            return f"فیلدهای اساسی را پر نکرده‌اید." 
         
        
        if len(hour) < 5:

            return f"فرمت وارد کردن ساعت را رعایت کنید."
        
        hour_format = hour.split(':')

        if not (int(hour_format[0])>=0 and int(hour_format[0])<=23) or not(int(hour_format[1])>=0 and int(hour_format[1])<=59):

            return f"مقدار ساعت دچار مشکل است. آن را درست وارد کنید."

        if len(date) !=10:
                return f"تاریخ به درستی وارد نشده است."

        date_format = date.split('/')
        if not(int(date_format[1])>=1 and int(date_format[1])<=12) or not(int(date_format[2])>=1 and int(date_format[2])<=31):
                return f"فرمت تاریخ را رعایت نکرده‌اید."
        
        now = dt.datetime.now().date()
        our_date = PatientOperations.convert_to_gregorian(date).date()
        # our_date = VisitOperations.create_date(date)

        if our_date < now:

            return f"تاریخ مورد نظر منقضی شده است. تاریخ را به درستی وارد کنید."

        

        Session = sessionmaker(bind=engine)
        session = Session()

        visit = session.query(Visit).filter(and_(Visit.visit_date ==  PatientOperations.convert_to_gregorian(date).date(), Visit.visit_hour == hour, Visit.status!=3)).first()

        if(visit):
            session.close()
            return f"نوبتی با همین تاریخ و ساعت رزرو شده است."
        
        patient = session.query(Patient).filter(Patient.nationalCode == ncode).first()
        if(patient):
            if(patient.visits):
                for visit in patient.visits:
                    if (visit.status == 1):
                        session.close()
                        return f"این بیمار یک نوبت نامشخص دارد. فعلا نمی‌توانید نوبتی برایش رزرو کنید."
            visit = Visit()
            visit.visit_date =  PatientOperations.convert_to_gregorian(date)
            visit.visit_hour = hour
            patient.visits.append(visit)
            session.add(visit)
            session.commit()
            session.close()
            return f"نوبت با موفقیت ذخیره شد."
        
        session.close()
        return f"رزرو نوبت با مشکل روبرو شد."

    
    @staticmethod
    def create_date(date):
        date = datetime.strptime(date, '%Y/%m').date()
        return date   
    
    @staticmethod
    def show_visits(patient_ncode):

        Session = sessionmaker(bind=engine)
        session = Session()

        patient = session.query(Patient).filter(Patient.nationalCode == patient_ncode).first()
        visits = session.query(Visit).filter(Visit.patient_id == patient.id).with_entities(Visit.id,Visit.visit_date, \
            Visit.visit_hour, Visit.status)
        session.close()

        if(visits):
            visits_list = []
            for visit in visits:
                visits_list.append([visit.id, visit.visit_date, visit.visit_hour, visit.status])
            return visits_list
        return list([])
    
    @staticmethod
    def show_visit(visit_id):

        Session = sessionmaker(bind=engine)
        session = Session()

        visit = session.query(Visit).filter(Visit.id == visit_id).first()
        session.close()
        if (visit):
            data ={
                'visitStatus': VisitOperations.status_value(visit.status),
                'visitHour': visit.visit_hour,
                'visitDate': PatientOperations.convert_to_jalali(visit.visit_date).strftime('%Y/%m/%d'),
                'visitDescription': visit.description,
            }
            return data
        return None

    @staticmethod
    def status_value(value):

        if value == 1:
            return "نامشخص"
        if value == 2:
            return "تایید شده"
        if value == 3:
            return "لغو شده"
    
    @staticmethod
    def editVisit(visit_id, status, visit_hour, visit_date, description):

        Session = sessionmaker(bind=engine)
        session = Session()

        if len(visit_hour) < 5:

            return f"فرمت وارد کردن ساعت را رعایت کنید."
        
        hour_format = visit_hour.split(':')

        if not (int(hour_format[0])>=0 and int(hour_format[0])<=23) or not(int(hour_format[1])>=0 and int(hour_format[1])<=59):

            return f"مقدار ساعت دچار مشکل است. آن را درست وارد کنید."

        if len(visit_date) !=10:
                return f"تاریخ به درستی وارد نشده است."
        
        date_format = visit_date.split('/')
        if not(int(date_format[1])>=1 and int(date_format[1])<=12) or not(int(date_format[2])>=1 and int(date_format[2])<=31):
                return f"فرمت تاریخ را رعایت نکرده‌اید."

        visit = session.query(Visit).filter(Visit.id == visit_id).first()

        now = dt.datetime.now().date()
        our_date = PatientOperations.convert_to_gregorian(visit_date).date()

        other_visit = session.query(Visit).filter(and_(Visit.visit_date ==  PatientOperations.convert_to_gregorian(visit_date).date(), Visit.visit_hour == visit_hour)).first()

        if (status == "نامشخص"):
            if our_date < now:
                return f"تاریخ مورد نظر منقضی شده است. تاریخ را به درستی وارد کنید." 
            if(other_visit and other_visit.id != visit_id and other_visit.status!=3):
                session.close()
                return f"نوبتی با همین تاریخ و ساعت رزرو شده است."
       

    

        if(visit):

            visit.status = VisitOperations.value_of_status(status)
            visit.visit_hour = visit_hour
            visit.visit_date = PatientOperations.convert_to_gregorian(visit_date)
            visit.description = description
            session.commit()
            session.close()
            return f"به روز رسانی انجام شد."
            
        return f"به روز رسانی با مشکل روبرو شد." 
    
    @staticmethod
    def value_of_status(status):

        if status == "تایید شده":
            return 2
        if status == "لغو شده":
            return 3
        if status == "نامشخص":
            return 1
    
    @staticmethod
    def daily_visits():
        
        Session = sessionmaker(bind=engine)
        session = Session()

        now = dt.datetime.now().date()
        # #max_date = now + jd.timedelta(days=3)
        # now_str = now.strftime('%Y/%m/%d')
        # # max_date_str = max_date.strftime('%Y/%m/%d')
        # now_date = VisitOperations.create_date(now_str)
        # # max_date_new = VisitOperations.create_date(max_date_str)

        visits = session.query(Visit).filter(and_(Visit.status == 1, Visit.visit_date >= now, Visit.visit_date <= (now + dt.timedelta(days=3)))).all()
        patients = session.query(Patient).all()
        session.close()
        if(visits):
            patients_visit = []
            for visit in visits:
                for patient in patients:
                    if visit.patient_id == patient.id:
                        patients_visit.append([patient.lastname, patient.nationalCode, visit.visit_date, visit.visit_hour, visit.status])
            return patients_visit
        return list([])

    @staticmethod
    def show_visits_monthly():

        Session = sessionmaker(bind=engine)
        session = Session()

        visits = session.query(Visit.status, Visit.visit_date, func.count(Visit.visit_date)).\
            group_by(Visit.status, Visit.visit_date).order_by(asc(Visit.visit_date)).all()
        session.close()


        if(visits):
            results = dict()
            for visit in visits:
                if not results.get(visit[1].strftime('%Y/%m/%d')):
                    results[visit[1].strftime('%Y/%m/%d')] = dict({"نامشخص":0, "تایید شده":0, "لغو شده":0})
                results[visit[1].strftime('%Y/%m/%d')][VisitOperations.status_value(visit[0])] = visit[2]
            return results
        return None
    
    @staticmethod
    def show_visits_monthly_2():

        Session = sessionmaker(bind=engine)
        session = Session()

        visits = session.query(Visit.status, Visit.visit_date).order_by(desc(Visit.visit_date)).all()
        if(visits):
            results = dict()
            for visit in visits:
                date = PatientOperations.convert_to_jalali(visit[1]).strftime('%Y/%m')
                if not results.get(date):
                    results[date] = dict({"نامشخص":0, "تایید شده":0, "لغو شده":0})
                results[date][VisitOperations.status_value(visit[0])]+=1
            return results
        return None

        # visits = session.query(Visit.status, func.strftime('%Y-%m-%d',Visit.visit_date), func.count(func.strftime('%Y-%m-%d',Visit.visit_date))).\
        #     group_by(Visit.status, func.strftime('%Y-%m-%d',Visit.visit_date)).order_by(desc(func.strftime('%Y-%m-%d',Visit.visit_date))).limit(4).all()
        # session.close()

        # print(visits)
        # if(visits):
        #     results = dict()
        #     for visit in visits:
        #         date = dt.datetime.strptime(visit[1], '%Y-%m-%d').date()
        #         new_date = jd.date.fromgregorian( day=date.day, month=date.month, year=date.year).strftime('%Y/%m/%d')
        #         if not results.get(new_date):
        #             results[new_date] = dict({"نامشخص":0, "تایید شده":0, "لغو شده":0})
        #         results[new_date][VisitOperations.status_value(visit[0])] = visit[2]
        #     return results
        # return None
    
    
    @staticmethod
    def return_persian_month(date):

        months_list = ["فروردین", "اردیبهشت", "خرداد", \
                        "تیر", "مرداد", "شهریور", \
                        "مهر", "آبان", "آذر", \
                        "دی", "بهمن", "اسفند"]
        our_date = PatientOperations.convert_to_jalali(date)
        month = our_date.month - 1
        year = our_date.year
        day = our_date.day
        return (year, months_list[month], day)

    
    @staticmethod
    def show_visits_chart():
            
        Session = sessionmaker(bind=engine)
        session = Session()  

        now = dt.datetime.now().date()
        # max_date = now + jd.timedelta(days=3)
        # now_str = now.strftime('%Y/%m/%d')
        # max_date_str = max_date.strftime('%Y/%m/%d')
        # now_date = VisitOperations.create_date(now_str)
        # max_date_new = VisitOperations.create_date(max_date_str)

        visits = session.query(Visit).\
            filter(and_(Visit.status == 1, Visit.visit_date >= now, Visit.visit_date <= (now + dt.timedelta(days=3)))).\
            order_by(asc(Visit.visit_date)).all()
        session.close()
        

        if(visits):
            results = dict()
            for visit in visits:
                one_key = VisitOperations.return_persian_month(visit.visit_date)
                if not results.get(str(one_key[0]) + '-' +one_key[1] + '-' + str(one_key[2])):
                     results[str(one_key[0]) + '-' +one_key[1] + '-' + str(one_key[2])] = dict()
                results[str(one_key[0]) + '-' +one_key[1] + '-' + str(one_key[2])][visit.visit_hour] = \
                    dt.datetime.strptime(visit.visit_hour, '%H:%M').time().hour + \
                    dt.datetime.strptime(visit.visit_hour, '%H:%M').time().minute/100
            for key in results.keys():
                results[key] = dict(sorted(results[key].items(), key = lambda x:x[1]))
            return results
        return None


class TableHandling(object):

    @staticmethod
    def tablesCreating():
        Base.metadata.create_all(engine, checkfirst=True)



    


    






        
    
    # @staticmethod
    # def session(val):
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     session.add(val)
    #     session.commit()







        









