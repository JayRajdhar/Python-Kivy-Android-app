import shutil
import os
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.uix.picker import MDDatePicker , MDThemePicker
from kivy.uix.button import Button
from datetime import date, datetime
from database import *
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.toast.kivytoast import toast
from kivymd.uix.dialog import MDDialog, MDInputDialog
from kivymd.theming import ThemeManager

import kivy
kivy.require('1.11.1')



Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

name_pass = ''
name_id = ''
scrn = ''


class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)


    def show_themepicker(self, temp):
        picker = MDThemePicker()
        picker.open()

    def newentrybtn(self):
        sm.current = 'newentry'

    def searchentrybtn(self):
        sm.current = 'searchname'

    def due_btn(self):
        sm.current = 'duescreen'

    def csvfun(self):

        os.makedirs('Shop')
        self.time = str(date.today())
        shutil.copy('data.db', 'BACKUP_' + self.time + '.db')


        # try:
        #
        #     gc = pygsheets.authorize('client_secret.json')
        #     sh = gc.open('test1')
        #     wk1 = sh.sheet1
        #     df1 = pd.read_csv('database.csv')
        #     wk1.set_dataframe(df1, 'A1')
        #     toast('Uploaded')
        # except:
        #     toast('failed')



################################################################################################################################


class NewEntry(Screen):
    dialog = None

    def samplebtn(self, text):
        sm.current = 'main'

    def show_datepicker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

    def got_date(self, the_date):
        self.datee_a.text = str(the_date)

    def on_pre_enter(self, *args):
        self.datee_a.text = str(date.today())
        self.rate_a.text = '3'
        self.gs_a.text = 'G'
        self.namee_a.text = ''
        self.phone_a.text = ''
        self.add_a.text = ''
        self.type_a.text = ''
        self.wt_a.text = ''
        self.totalamt_a.text = ''
        self.balamt_a.text = ''



    def add_entry(self):
        namee = self.namee_a.text
        phone = self.phone_a.text
        address = self.add_a.text
        type = self.type_a.text
        wt = self.wt_a.text
        datee = self.datee_a.text
        gs = self.gs_a.text
        totalamt = self.totalamt_a.text
        balamt = self.balamt_a.text
        rate = self.rate_a.text

        insert(namee, address, phone, type, wt, gs, datee, totalamt, balamt, rate)

        data_list = []
        res = search_add(namee, phone)
        for i in range(14):
            data_list.append(res[0][i])
        append_list_as_row('database.csv', data_list)

        sm.current = 'main'
        toast(' Successfully Entry Added ')



    def new_diag(self, temp):

        if not bool(self.namee_a.text):
            toast('Enter Name')
            return
        elif not bool(self.balamt_a.text):
            toast('Enter Bal Amount')
            return
        elif not bool(self.datee_a.text):
            toast('Enter Date')
            return
        elif not bool(self.wt_a.text):
            toast('Enter Weight')
            return
        elif bool(self.phone_a.text):
            if len(self.phone_a.text) != 10:
                toast('Phone Number Digits must be 10')
                return
        elif not bool(self.rate_a.text):
            toast('Enter rate')
            return

        self.dialog = MDDialog(title='Do you want to confirm?',
            text="Add New Entry",
            size_hint=[.8,.4], events_callback=self.mycallback,
            text_button_cancel='CANCEL', text_button_ok='CONFIRM'
            )
        self.dialog.open()


    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            self.add_entry()


################################################################################################################################


class SearchName(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SearchName, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.namesearch_d.text = ""

    def nameclick(self):
        self.ids.container.clear_widgets()
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_text_inputs()


    def add_text_inputs(self):

        namedval = self.namesearch_d.text
        namedval = '%' + namedval + '%'
        try:
            entryd = search(namedval, '%%')
        except:
            toast('No Entry Found')

        leng = len(entryd)

        for x in range(leng):
            name_phone = str(entryd[x][0]) + " " + str(entryd[x][1])
            btn = Button(text=name_phone,
                         size_hint_y=None, background_color=[0,0,1,0.5], border=[1,0,0,1],
                         size_hint_x=1, height=140, on_release=self.open_btn)
            self.ids.container.add_widget(btn)

    def open_btn(self, instance):
        global name_pass
        global name_id
        name_pass = ' '.join(str(elem) for elem in instance.text.split(" ")[1:])
        name_id = instance.text.split(" ")[0]
        sm.current = 'settlescreen'

    def func(self, temp):
        self.ids.container.clear_widgets()
        sm.current = 'main'





################################################################################################################################


class SettleScreen(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettleScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):

        name_val = '%' + name_pass + '%'

        try:
            entrys = search(name_val, name_id)
        except:
            toast('No Entry Found')

        self.namee_z.text = entrys[0][1]
        self.phone_z.text = entrys[0][3]
        self.type_z.text = entrys[0][4]
        self.wt_z.text = str(entrys[0][5])
        self.gs_z.text = entrys[0][6]

        self.name_s = entrys[0][1]

        self.value_lbl.text = 'Value: ' + str(entrys[0][9])
        self.rate_lbl.text = 'Rate: ' + str(entrys[0][11]) + '%'

        self.settle_flag = entrys[0][13]

        dur_date = entrys[0][7].split(':')[0]
        dur_date = datetime.strptime(dur_date, '%Y-%m-%d')
        dur_date = dur_date.date()

        if self.settle_flag == '1':
            end_date = datetime.strptime(entrys[0][8], '%Y-%m-%d')
            end_date = end_date.date()
            dur_date = end_date - dur_date
        else:
            dur_date = date.today() - dur_date

        mnths = int(dur_date.days/30)
        dys = int(dur_date.days%30)
        self.duration_lbl.text = 'Duration: ' + str(mnths) + 'm ' + str(dys) + 'd'



        if self.settle_flag != '0':
            self.settle_btn.text = 'OPEN'
            self.close_lbl.text = 'Entry Closed On:' + entrys[0][8]
            self.tick_lbl.source = "vector61.jpg"
        else:
            self.settle_btn.text = 'CLOSE'
            self.close_lbl.text = ' '
            self.tick_lbl.source = ""

        arr_bal = entrys[0][10].split(':')

        bal_txt = 'Amounts: \n'
        for i in range(len(arr_bal)):
            bal_txt = bal_txt + '    ' + arr_bal[i] + '\n'
        self.amt_lbl.text = bal_txt

        arr_date = entrys[0][7].split(':')

        date_txt = 'Date: \n'
        for i in range(len(arr_date)):
            date_txt = date_txt + arr_date[i] + '\n'
        self.date_lbl.text = date_txt

        def interest(amt, dt):
            date_s = datetime.strptime(dt, '%Y-%m-%d')
            date_s = date_s.date()
            dt_elap = date.today() - date_s
            if dt_elap.days % 30 > 10:
                dt_elap = (dt_elap.days / 30) + 1
            else:
                dt_elap = dt_elap.days / 30
            amt = int(amt) * (int(entrys[0][11]) / 100)
            return amt * int(dt_elap)

        interest_arr = []

        for i in range(len(arr_bal)):
            if arr_bal[i][-1] != '^':
                interest_arr.append(interest(arr_bal[i], arr_date[i]))


        tot_amt = 0
        int_amt = 0
        for j in range(len(arr_bal)):
            if arr_bal[j][-1] != '^':
                tot_amt = tot_amt + int(arr_bal[j])
            else:
                tot_amt = tot_amt + int(arr_bal[j][:-1])
        for j in range(len(interest_arr)):
            int_amt = int_amt + int(interest_arr[j])

        tot_amt = tot_amt + int_amt
        self.final_amt = tot_amt
        self.amount_lbl.text = "Rs: " + str(tot_amt)
        self.int_lbl.text = "Total Interest: " + str(int_amt)

    def settlebtn(self):

        try:
            settle(str(name_pass), name_id, str(date.today()), str(self.final_amt))
            toast('Entry Settled')
            sm.current = 'main'
        except:
            toast('Data Error')

    def settle_pps(self):
        self.dialog = MDDialog(title="Settle Selected Customer",
                               text="Received payment from "+self.name_s+" ?",
                               size_hint=[.8, .4], events_callback=self.mycallback,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )
        self.dialog.open()

    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            self.settlebtn()



    def backbtn(self, temp):
        sm.current = 'searchname'

    def updatebtn(self):
        if self.settle_flag == '1':
            toast('Cannot update closed entry')
        else:
            sm.current = 'updatescreen'

################################################################################################################################


class UpdateScreen(Screen):
    def __init__(self, **kwargs):
        super(UpdateScreen, self).__init__(**kwargs)


    def on_pre_enter(self, *args):
        name_val = '%' + name_pass + '%'

        try:
            entrys = search(name_val, name_id)
        except:
            toast('No Entry Found')
        self.namee_z.text = entrys[0][1]

        self.phone_z.text = entrys[0][3]
        self.type_z.text = entrys[0][4]
        self.wt_z.text = str(entrys[0][5])
        self.gs_z.text = entrys[0][6]

        self.namee_temp = entrys[0][1]
        self.phone_temp = entrys[0][3]
        self.balamt_temp = entrys[0][10]
        self.sdate_temp = entrys[0][7]

        self.value_lbl.text = 'Value: ' + str(entrys[0][9])
        self.rate_lbl.text = 'Rate: ' + str(entrys[0][11]) + '%'

        dur_date = entrys[0][7].split(':')[0]
        dur_date = datetime.strptime(dur_date, '%Y-%m-%d')
        dur_date = dur_date.date()
        dur_date = date.today() - dur_date
        mnths = int(dur_date.days / 30)
        dys = int(dur_date.days % 30)

        self.duration_lbl.text = 'Duration: ' + str(mnths) + 'm ' + str(dys) + 'd'

        arr_bal = entrys[0][10].split(':')
        bal_txt = 'Amounts: \n'
        for i in range(len(arr_bal)):
            bal_txt = bal_txt + '    ' + arr_bal[i] + '\n'
        self.amt_lbl.text = bal_txt

        arr_date = entrys[0][7].split(':')
        date_txt = 'Date: \n'
        for i in range(len(arr_date)):
            date_txt = date_txt + arr_date[i] + '\n'
        self.date_lbl.text = date_txt

    def show_datepicker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

    def got_date(self, the_date):
        self.datee_z.text = str(the_date)

    def backbtn(self, temp):
        sm.current = 'settlescreen'

    def update_btn(self):
        fin_amt = self.balamt_temp+':'+self.pop_amt_add
        fin_date = self.sdate_temp+':'+str(date.today())
        update_add(fin_amt, fin_date, self.namee_temp, name_id)
        self.balamt_temp = fin_amt
        self.sdate_temp = fin_date




    def add_diag(self):

        self.dialog = MDInputDialog(title='Add Amount',
                               hint_text="Given Amount",
                               size_hint=[.8, .4], events_callback=self.mycallback,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )

        self.dialog.open()

    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            try:
                int(pop.text_field.text)
                self.pop_amt_add = pop.text_field.text
                self.update_btn()
                self.on_pre_enter()
                toast('Amount Added Successfully')
            except:
                self.add_diag()
                toast('ENTER NUMERIC INPUT')

    def minus_diagA(self):

        self.dialog = MDDialog(title='Select Amount Type',
                               text="Received Amount To Remove from \nInterest or Balance Amounts?",
                               size_hint=[.8, .4], events_callback=self.mycallback_m,
                               text_button_cancel='INTEREST', text_button_ok='BALANCE'
                               )

        self.dialog.open()

    def mycallback_m(self, text_s, pop):
        if text_s == 'BALANCE':
            self.minus_diagBA()
        elif text_s == 'INTEREST':
            self.minus_diagBB()

    def minus_diagBA(self):

        self.dialog = MDInputDialog(title='Balance Amount Received',
                               hint_text="Received Amount",
                               size_hint=[.8, .4], events_callback=self.mycallback_BA,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )

        self.dialog.open()

    def mycallback_BA(self, text_s, pop):
        if text_s == 'CONFIRM':
            try:
                int(pop.text_field.text)
                self.pop_amt_add = '-'+pop.text_field.text
                self.update_btn()
                self.on_pre_enter()
                toast('Amount Added Successfully')
            except:
                toast('Wrong Input')
                self.minus_diagBA()


    def minus_diagBB(self):

        self.dialog = MDInputDialog(title='Interest Amount Received',
                               hint_text="Received Amount",
                               size_hint=[.8, .4], events_callback=self.mycallback_BB,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )

        self.dialog.open()


    def mycallback_BB(self, text_s, pop):
        if text_s == 'CONFIRM':
            try:
                int(pop.text_field.text)
                self.pop_amt_add = '-' + pop.text_field.text + '^'
                self.update_btn()
                self.on_pre_enter()
                toast('Amount Added Successfully')
            except:
                toast('Wrong Input')
                self.minus_diagBB()

    def edit_bal(self, temp):
        global scrn
        scrn = 'Non_Due'
        sm.current = 'amtupdate'


################################################################################################################################


class DueEntry(Screen):

    def __init__(self, **kwargs):
        super(DueEntry, self).__init__(**kwargs)
        self.datee_d.text = str(date.today())


    def on_pre_enter(self, *args):
        self.datee_d.text = str(date.today())
        self.namee_d.text = ''
        self.phone_d.text = ''
        self.add_d.text = ''
        self.amt_d.text = ''
        self.reason_d.text = ''

    def show_datepicker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

    def got_date(self, the_date):
        self.datee_d.text = str(the_date)

    def back_btn(self, temp):
        sm.current = 'main'

    pass


################################################################################################################################

class DueScreen(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DueScreen, self).__init__(**kwargs)
        self.obj = DueEntry(name='dueentry')
        self.flag = 0
        self.ids.container.add_widget(self.obj)

    def reset_screen(self):
        self.obj.ids.datee_d.text = str(date.today())
        self.obj.ids.namee_d.text = ''
        self.obj.ids.phone_d.text = ''
        self.obj.ids.add_d.text = ''
        self.obj.ids.amt_d.text = ''
        self.obj.ids.reason_d.text = ''


    def search_btn(self):
        self.ids.container.clear_widgets()
        self.flag = 1
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_text_inputs()

    def add_text_inputs(self):

        namedval = self.namesearch_d.text
        namedval = '%' + namedval + '%'
        try:
            entryd = search_due(namedval, '%%')
        except:
            toast('No Entry Found')

        leng = len(entryd)

        self.ids.container.size_hint_y = None
        # self.ids.container.pos_hint_y = 0.2

        for x in range(leng):
            name_phone = str(entryd[x][0]) + " " + str(entryd[x][1])
            btn = Button(text=name_phone,
                         size_hint_y=None, background_color=[0,0,1,0.5], border=[1,0,0,1],
                         size_hint_x=1, height=140, on_release=self.open_btn)
            self.ids.container.add_widget(btn)

    def open_btn(self, instance):
        global name_pass
        global name_id
        name_pass = ' '.join(str(elem) for elem in instance.text.split(" ")[1:])
        name_id = instance.text.split(" ")[0]
        sm.current = 'updatedue'



    def due_entry(self):
        namee = self.obj.ids.namee_d.text
        phone = self.obj.ids.phone_d.text
        address = self.obj.ids.add_d.text
        sdate = self.obj.ids.datee_d.text
        amt = self.obj.ids.amt_d.text
        reason = self.obj.ids.reason_d.text

        try:
            insert_due(namee, address, phone, sdate, amt, reason)
            sm.current = 'main'
            toast(' Successfully Entry Added ')
        except:
            toast('Cannot add')

        # data_list = []
        # res = search_add(namee, phone)
        # for i in range(14):
        #     data_list.append(res[0][i])
        # append_list_as_row('database.csv', data_list)


    def due_diag(self, temp):
        if self.flag == 1:
            self.reset_screen()
            self.ids.container.clear_widgets()
            self.ids.container.size_hint_y = 1
            self.ids.container.add_widget(self.obj)
            self.flag = 0

        if not bool(self.obj.ids.namee_d.text):
            toast('Enter Name')
            return
        elif not bool(self.obj.ids.amt_d.text):
            toast('Enter Due Amount')
            return
        elif not bool(self.obj.ids.datee_d.text):
            toast('Enter Date')
            return
        elif bool(self.obj.ids.phone_d.text):
            if len(self.obj.ids.phone_d.text) != 10:
                toast('Phone Number Digits must be 10')
                return
        elif not bool(self.obj.ids.reason_d.text):
            toast('Enter Reason for Due')
            return

        self.dialog = MDDialog(title='Do you want to confirm?',
            text="Add New Entry",
            size_hint=[.8,.4], events_callback=self.mycallback,
            text_button_cancel='CANCEL', text_button_ok='CONFIRM'
            )
        self.dialog.open()

    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            self.due_entry()

    def back_btn(self, temp):
        sm.current = "main"



################################################################################################################################

class UpdateDue(Screen):

    def on_pre_enter(self, *args):
        name_val = '%' + name_pass + '%'

        try:
            entrys = search_due(name_val, name_id)
        except:
            toast('No Entry Found')


        self.namee_d.text = entrys[0][1]
        self.phone_d.text = entrys[0][3]
        self.add_d.text = entrys[0][2]
        self.reason_d.text = entrys[0][7]

        self.namee_temp = entrys[0][1]
        self.phone_temp = entrys[0][3]
        self.balamt_temp = entrys[0][6]
        self.sdate_temp = entrys[0][4]
        self.settle_flag = entrys[0][-1]

        self.value_lbl.text = 'Value: ' + str(entrys[0][6].split(':')[0])

        dur_date = entrys[0][4].split(':')[0]
        dur_date = datetime.strptime(dur_date, '%Y-%m-%d')
        dur_date = dur_date.date()
        dur_date = date.today() - dur_date
        mnths = int(dur_date.days / 30)
        dys = int(dur_date.days % 30)

        self.duration_lbl.text = 'Duration: ' + str(mnths) + 'm ' + str(dys) + 'd'

        arr_bal = entrys[0][6].split(':')
        bal_txt = 'Amounts: \n'
        for i in range(len(arr_bal)):
            bal_txt = bal_txt + '    ' + arr_bal[i] + '\n'
        self.amt_lbl.text = bal_txt

        arr_date = entrys[0][4].split(':')
        date_txt = 'Date: \n'

        for i in range(len(arr_date)):
            date_txt = date_txt + arr_date[i] + '\n'
        self.date_lbl.text = date_txt

        if self.settle_flag == '1':
            self.close_btn_lbl.text = 'Open'
            self.close_lbl.text = 'Entry Closed on:  ' + entrys[0][5]
            self.tick_lbl.source = "vector61.jpg"
        else:
            self.close_btn_lbl.text = 'Close'
            self.close_lbl.text = ' '
            self.tick_lbl.source = ""


        self.tot_amt = 0
        for i in range(len(arr_bal)):
            self.tot_amt = self.tot_amt + int(arr_bal[i])
        self.amount_lbl.text = "Rs: " + str(self.tot_amt)



    def update_btn(self):
        fin_amt = self.balamt_temp + ':' + self.pop_amt_add
        fin_date = self.sdate_temp + ':' + str(date.today())
        try:
            due_update_add(fin_amt, fin_date, self.namee_temp, name_id)
        except:
            toast('Data Error')
        self.balamt_temp = fin_amt
        self.sdate_temp = fin_date

    def minus_diag(self):

        self.dialog = MDInputDialog(title='Amount Received',
                                    hint_text="Given Amount",
                                    size_hint=[.8, .4], events_callback=self.mycallback,
                                    text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                                    )

        self.dialog.open()

    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            try:
                int(pop.text_field.text)
                self.pop_amt_add = '-'+pop.text_field.text
                self.update_btn()
                self.on_pre_enter()
                toast('Amount Added Successfully')
            except:
                self.minus_diag()
                toast('ENTER NUMERIC INPUT')

    def edit_bal(self, temp):
        global scrn
        scrn = 'Due'
        sm.current = 'amtupdate'

    def diag(self):

        self.dialog = MDDialog(title='Close Entry..?',
                               text="Received Amount from "+name_pass+" ?",
                               size_hint=[.8, .4], events_callback=self.mycallback_m,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )

        self.dialog.open()

    def mycallback_m(self, text_s, pop):
        if text_s == 'CONFIRM':
            self.settle_due()

    def settle_due(self):
        try:
            settle_due(name_pass, name_id, str(date.today()), str(self.tot_amt))
            toast('entry settled')
            self.on_pre_enter()
        except:
            toast('Data Error')

    def bck(self, temp):
        sm.current = 'duescreen'

################################################################################################################################
class AmtUpdate(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_pre_enter(self, *args):
        name_val = '%' + name_pass + '%'

        try:
            if scrn == 'Due':
                entrys = search_due(name_val, name_id)
                self.namee_d.text = entrys[0][1]
                self.phone_d.text = entrys[0][3]

                self.arr_amt = entrys[0][6].split(':')
                self.arr_date = entrys[0][4].split(':')

                for x in range(len(self.arr_amt), 5):
                    amt = 'amt_' + str(x + 1)
                    dt = 'date_' + str(x + 1)
                    self.ids[amt].readonly = True
                    self.ids[dt].readonly = True

            elif scrn == 'Non_Due':
                entrys = search(name_val, name_id)
                self.namee_d.text = entrys[0][1]
                self.phone_d.text = entrys[0][3]

                self.arr_amt = entrys[0][10].split(':')
                self.arr_date = entrys[0][7].split(':')

                for x in range(len(self.arr_amt), 5):
                    amt = 'amt_' + str(x + 1)
                    dt = 'date_' + str(x + 1)
                    self.ids[amt].readonly = True
                    self.ids[dt].readonly = True

        except:
            toast('No Entry Found')



        for i in range(len(self.arr_amt)):
            amt = 'amt_'+str(i+1)
            dt = 'date_'+str(i+1)
            self.ids[amt].text = self.arr_amt[i]
            self.ids[dt].text = self.arr_date[i]

    def chip_c(self, instance, value):
        try:
            if scrn == 'Non_Due':
                amt = 'amt_' + str(value)
                amt_list = list(self.ids[amt].text)
                if amt_list[-1] == '^':
                    self.ids[amt].text = ''.join(str(elem) for elem in amt_list[:-1])
                else:
                    self.ids[amt].text = self.ids[amt].text + '^'
            elif scrn == 'Due':
                toast('Interest Cannot be added for Due')
        except:
            toast('Edit existing amounts only')

    def update_call(self):
        arr_uamt = []
        arr_udt = []

        for i in range(len(self.arr_amt)):
            amt = 'amt_' + str(i + 1)
            dt = 'date_' + str(i + 1)
            arr_uamt.append(self.ids[amt].text)
            arr_udt.append(self.ids[dt].text)

        arr_uamt = ':'.join(str(elem) for elem in arr_uamt)
        arr_udt = ':'.join(str(elem) for elem in arr_udt)

        try:

            if scrn == 'Due':
                due_update_add(arr_uamt, arr_udt, name_pass, name_id)
                sm.current = 'updatedue'
                toast('Succesfully Added')
            elif scrn == 'Non_Due':
                update_add(arr_uamt, arr_udt, name_pass, name_id)
                sm.current = 'updatescreen'
                toast('Succesfully Added')

        except:
            toast('Data Error')


    def update_diag(self, temp):
        for i in range(len(self.arr_amt)):
            amt = 'amt_' + str(i + 1)
            dt = 'date_' + str(i + 1)
            if not bool(self.ids[amt].text):
                toast('Enter Amount')
                return
            elif not bool(self.ids[dt].text):
                toast('Enter Date')
            elif bool(self.ids[dt].text):
                try:
                    datetime.strptime(self.ids[dt].text, '%Y-%m-%d')
                except:
                    toast('Enter Valid Date (yyyy-mm-dd)')
                    return

        self.dialog = MDDialog(title='Do you want to confirm?',
                               text="Update Entry",
                               size_hint=[.8, .4], events_callback=self.mycallback,
                               text_button_cancel='CANCEL', text_button_ok='CONFIRM'
                               )
        self.dialog.open()

    def mycallback(self, text_s, pop):
        if text_s == 'CONFIRM':
            self.update_call()





    def bck(self, temp):
        if scrn == 'Due':
            sm.current = 'updatedue'
        if scrn == 'Non_Due':
            sm.current = 'updatescreen'

    def on_leave(self, *args):
        for i in range(len(self.arr_amt)):
            amt = 'amt_' + str(i + 1)
            dt = 'date_' + str(i + 1)
            self.ids[amt].text = ''
            self.ids[dt].text = ''

################################################################################################################################
class Test(Screen):
    def bck(self, temp):
        sm.current = 'main'





################################################################################################################################


class WindowManager (ScreenManager):
    pass


sm = WindowManager()

################################################################################################################################


class MyMainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)
        theme_cls = ThemeManager()


    create()
    create_due()



    def android_back_click(self, window, key, *largs):
        if key == 27:
            sm.current = 'main'
            return True

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        Builder.load_file("my.kv")
        screens = [MainPage(name="main"), NewEntry(name="newentry"), UpdateScreen(name='updatescreen'),
                   DueScreen(name='duescreen'), AmtUpdate(name='amtupdate'),Test(name='test'),
                   SearchName(name='searchname'), SettleScreen(name='settlescreen'), UpdateDue(name='updatedue')]
        for screen in screens:
            sm.add_widget(screen)

        sm.current = "main"
        return sm


if __name__ == "__main__":
    MyMainApp().run()

