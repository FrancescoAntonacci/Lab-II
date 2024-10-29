import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import serial
import numpy as np
import pylab as py
import time
from matplotlib.backends.backend_tkagg import *

global go_button
global Directory

Directory='/home/studentelab2/dati_arduino/' # name of the directory where the file will be stored
global filenamedef
filenamedef='data' # default name of the data file (w/out extension)
global datadef
datadef=1 # set the default
global samprdef
samprdef='100' # set the default sampling interval (nominal)
global syncdef
syncdef = 0 # set the default to asynchronous acquisition
global avedef
avedef = 0 # set the default to single sweep acquisition
global prec
prec = 100 # set the accuracy in average calculations
global averagedsweeps

# create the panel
root=tk.Tk()
root.title('Parameters input')
root.geometry('850x600+50+50')
root.attributes('-topmost',1)
root.columnconfigure(4,weight=1)
root.rowconfigure(4,weight=1)

def go_clicked(): # define operations to be taken when the GO button is pressed
    go_button.state(['disabled']) # disable the button (it does not work properly!)
    # startflag=1
    # errorflag=0
    sampl=samp.get() # read number of points
    samplog=np.log(int(sampl))/np.log(2) # take the base 2 exponent
    samplogstr=str(int(samplog-7)) # encode it for transmission
    datapoints=int(sampl) # put the number of points into variable datapoints
    samprl=sampr.get() # read sampling interval
    deltati=int(samprl) # put it into the deltati variable
    if (deltati>9999) or (deltati<10):
        showinfo(title='Error',message='Sampling interval out of range') # check for out of range
    deltatnom=str(round(int(samprl)/10)) # do a roundoff
    if (len(deltatnom)==1): # here and in the following prepare the encoded byte sequence
        deltatnom=('00'+deltatnom)
    if (len(deltatnom)==2):                 deltatnom=('0'+deltatnom)
    deltat3=deltatnom[2]
    deltat2=deltatnom[1]
    deltat1=deltatnom[0]
    # if (sync.get()=='syncon'): # look at sync checkbox
    #     syncflag = '1'
    # else:
    #     syncflag= '0'
    syncro=syncr.get() # read the syncronous setting
    syncflag='0'
    if (syncro == 'Trigger Pos.Slope'): syncflag='1'
    if (syncro == 'Trigger Neg.Slope'): syncflag='2'
    avera=aver.get()
    if (avera == 'Single Sweep'):
        averflag='0'

    if (avera == 'Average on 4 Sweeps'):
        averflag='2'
    if (avera == 'Average on 8 Sweeps'):
        averflag='3'
    if (avera == 'Average on 16 Sweeps'):
        averflag='4'
    if (avera == 'Average on 32 Sweeps'):
        averflag='5'
    if (avera == 'Average on 64 Sweeps'):
        averflag='6'

    if (avera != 'Single Sweep') and (samplog>11):
        showinfo(title='Error',message='Set back to 2048 data points (maximum for averaged samples)')
        samp.set('2048')
        samplogstr = '4'
        datapoints = 2048

    if (avera != 'Single Sweep') and (syncflag == '0'):
        showinfo(title='Warning',message='You have selected averaged and asynchronous acquisition: I will do it, but are you sure this is what you need?')

    if (hires.get()=='hireson'): # look at hires checkbox
        hiresflag = '1'
    else:
        hiresflag= '0'

    iwrite=0


    FileName=Directory+filename.get()+'.txt' # prepare the filename

    #startflag=0

    ard=serial.Serial('/dev/ttyACM0',119200) # define the serial port (depends on the operating system!) and sets the communicaton speed /dev/ttyACM0
    time.sleep(2) # wait 2 s to prevent casini

    ard.write(bytes(deltat3,'utf-8')) # here and in the following write the encoded sequence of bytes to arduino via serial communication. Bytes are sent as utf-8 characters
    ard.write(bytes(deltat2,'utf-8'))
    ard.write(bytes(deltat1,'utf-8'))
    ard.write(bytes(samplogstr,'utf-8'))
    ard.write(bytes(syncflag,'utf-8'))
    ard.write(bytes(hiresflag,'utf-8'))

    ard.write(bytes(averflag,'utf-8'))

    print ("start") # print to console

    runningtime=np.zeros(datapoints) # prepare running arrays
    runningetime=np.zeros(datapoints)
    runningvolt=np.zeros(datapoints)
    runningevolt=np.zeros(datapoints)

    if (hiresflag=='1'):
        print ('transferring 12-bit data') # print to console
    else:
        print ('transferring 10-bit data') # print to console

    averagedsweeps=2**int(averflag)
    message = ('data averaged on '+ str(averagedsweeps) + ' sweeps')
    print (message)

    if (avera == 'Single Sweep'): # read and file write loop for non averaged data
        outputFile = open(FileName, "w" ) # open the file for writing
        for i in range (0,datapoints): # reading loop
            data = ard.readline().decode() # read every data and decode it
            if data:
                outputFile.write(data) # when data are present, they are written to the file
                runningtime[i]=float(data[0:data.find(' ')])
                runningvolt[i]=float(data[data.find(' '):])
        outputFile.close() # close the file
        ard.close() # close serial communication with Arduino



        deltat=np.zeros(datapoints-1) # determine average and std of the sampling interval and write them to console
        for i in range (0,datapoints-1):
            deltat[i]=runningtime[i+1]-runningtime[i]
        deltatavg=np.average(deltat)
        deltatstd=np.std(deltat)
        print("Delta t average = %.3f " %deltatavg," us")
        print("Delta t stdev = %.3f" %deltatstd," us")
# avg and std calculations
        voltaavg=np.average(runningvolt)
        voltastd=np.std(runningvolt)
        print("Digitized data average = %.3f" %voltaavg, " digit")
        print("Digitized data std = %.3f" %voltastd, " digit")

    if (avera != 'Single Sweep'): # read and file write loop for averaged data
        for i in range (0,datapoints): # reading loop
            data = ard.readline().decode() # read every data and decode it
            if data:
                pos1=data.find(' ')
                pos2=data.find(' ',pos1+1,len(data))
                pos3=data.find(' ',pos2+1,len(data))
                runningtime[i]=int(data[0:pos1])/prec
                runningetime[i]=np.sqrt(abs(int(data[pos1:pos2])))/(prec)
                runningvolt[i]=int(data[pos2:pos3])/prec
                runningevolt[i]=np.sqrt(abs(int(data[pos3:len(data)])))/(prec)
                if (runningevolt[i]==0): runningevolt[i]=1/np.sqrt(averagedsweeps) # avoid zeroes in the error array
                if (runningetime[i]==0): runningetime[i]=1/np.sqrt(averagedsweeps) # avoid zeroes in the error array
                #print (i,runningtime[i],runningetime[i],runningvolt[i],runningevolt[i])

        ard.close() # close serial communication with Arduino

        deltat=np.zeros(datapoints-1) # determine average and std of the sampling interval and write them to console
        for i in range (0,datapoints-1):
            deltat[i]=runningtime[i+1]-runningtime[i]
        deltatavg=np.average(deltat)
        deltatstd=np.std(deltat)
        print("Delta t average = %.3f" %deltatavg," us")
        print("Delta t stdev = %.3f" %deltatstd," us")

# avg and std calculations
        voltaavg=np.average(runningvolt)
        voltastd=np.std(runningvolt)
        print("Digitized data average = %.3f" %voltaavg, " digit")
        print("Digitized data std = %.3f" %voltastd, " digit")

        np.savetxt(FileName,np.c_[runningtime,runningetime,runningvolt,runningevolt],fmt='%.2f')

    go_button.state(['!disabled'])
    # startflag=0
    # goflag=1
    print ('file written: ',FileName)
    if (avera !='Single Sweep'):
        print ('file contains four columns: time in us, error on time, signal in digit, error on signal')
    else:
        print ('file contains two columns: time in us, signal in digit')
    print('end') # write to console
    print('')

    if (displ.get()=='displon'): # when display checkbox is selected, display the arrays
        fig = py.Figure()
        plot1 = fig.add_subplot(111)
        if (avera != 'Single Sweep'):
            x, dx, y, dy = py.loadtxt(FileName,unpack='True')
            if (errorb.get()=='erroron'):
                plot1.errorbar(x,y,dy, dx,color='red')
            else:
                plot1.errorbar(x,y,linestyle='-',color='blue')
        else:
            x,y= py.loadtxt(FileName,unpack='True')
            plot1.errorbar(x,y,linestyle='-',color='blue')
        plot1.set_xlabel('Time  [us]')
        plot1.set_ylabel('Signal  [digit]')
        canvas=FigureCanvasTkAgg(fig,master=root) # put the plot onto the panel
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=4,columnspan=4)


# the following instructions are needed to define buttons, text, labels, and data entries in the panel
filename=tk.StringVar()
filename_label=ttk.Label(root,text='Filename (w/out extension):')
filename_label.grid(column=0,row=0)
filename_entry=ttk.Entry(root,textvariable=filename)
filename_entry.grid(column=1,row=0)
filename_entry.insert(0,filenamedef)
filename_label2=ttk.Label(root,text='It will overwrite with no warnings!')
filename_label2.grid(column=2,row=0)

samp=tk.StringVar()
sampr=tk.StringVar()
syncr=tk.StringVar()
aver=tk.StringVar()

sampr_label=ttk.Label(root,text='Sampling Interval [us]')
sampr_label2=ttk.Label(root,text='Greater than 10 us and smaller than 9999 us')
sampr_label.grid(column=0,row=1)
sampr_label2.grid(column=2,row=1)
sampr_entry=ttk.Entry(root,textvariable=sampr,width=8)
sampr_entry.grid(column=1,row=1)
sampr_entry.insert(0,samprdef)

combobox=ttk.Combobox(root,textvariable=samp,width=5) # a combobox is created for the number of points
combobox_label=ttk.Label(root,text='Number of data points:')
combobox_label.grid(column=0,row=2)

combobox['values']=['128','256','512','1024','2048','4096','8192']
combobox['state']='readonly'
combobox.grid(column=1,row=2)
combobox.current(datadef)

combobox1=ttk.Combobox(root,textvariable=syncr,width=15) # a combobox is created for synchronous acquisitions
combobox1_label=ttk.Label(root,text='Trigger:')
#combobox1_label.grid(column=0,row=3)
combobox1['values']=['Asynchronous','Trigger Pos.Slope','Trigger Neg.Slope']
combobox1['state']='readonly'
combobox1.grid(column=0,row=3)
combobox1.current(syncdef)

combobox2=ttk.Combobox(root,textvariable=aver,width=20) # a combobox is created for averaged acquisitions
combobox2_label=ttk.Label(root,text='Max 2048 data points for averaged samples!')
combobox2_label.grid(column=2,row=2)
combobox2['values']=['Single Sweep','Average on 4 Sweeps','Average on 8 Sweeps','Average on 16 Sweeps','Average on 32 Sweeps','Average on 64 Sweeps']
combobox2['state']='readonly'
combobox2.grid(column=1,row=3)
combobox2.current(avedef)

sync=tk.StringVar()
displ=tk.StringVar()
displ.set('displon') # display data by default
hires=tk.StringVar()
hires.set('hireson') # 12-bit data by default
errorb=tk.StringVar()
errorb.set('erroroff') # error bars off on display by default



# checkbutton=ttk.Checkbutton(root,text='Synchronous',variable=sync,onvalue='syncon',offvalue='syncoff')
# checkbutton.grid(column=0,row=3)

checkbutton=ttk.Checkbutton(root,text='12-bit data',variable=hires,onvalue='hireson',offvalue='hiresoff')
checkbutton.grid(column=3,row=1)

displaybutton=ttk.Checkbutton(root,text='Display data',variable=displ,onvalue='displon',offvalue='disploff')
displaybutton.grid(column=3,row=0)

errorbarbutton=ttk.Checkbutton(root,text='Show error bars if available',variable=errorb,onvalue='erroron',offvalue='erroroff')
errorbarbutton.grid(column=3,row=3)

go_button=ttk.Button(root,text='GO!',command=go_clicked)
go_button.grid(column=2,row=3)

root.mainloop() # creates the panel