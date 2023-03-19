from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import ConexionEst as CE
import datetime as dt

valor = True

def destroy(nw):
	nw.destroy()
	tabla.delete(*tabla.get_children())
	MostrarTabla()

def MostrarTabla():
	tabla.delete(*tabla.get_children())
	for row in CE.obtenerLista():
		if row[5] == 1:
			tabla.insert("",'end',iid=row[0],values=(row[1],row[2],row[3],row[4],"pago"))
		else:
			tabla.insert("",'end',iid=row[0],values=(row[1],row[2],row[3],row[4],"pendiente"))

	
	

def AgregarPatente():
	
	if TxtPatente.get() != "":
		date = dt.datetime.now()
		format_date=f"{date:%d-%m-%Y %H:%M}"
		tiempo = [entrymin.get(),entryhor.get(),entrydia.get(),entrymes.get()]
		
		if BuscarRepeticion(TxtPatente.get()) == 0:
			CE.AgregarPatenteLista(TxtPatente.get(),format_date,"dd-mm-aaaa HH:MM","0","0",tiempo)
			tabla.insert("",'end',iid=CE.ObtenerSiguienteIdPatente(),values=(TxtPatente.get(),format_date,"dd-mm-aaaa HH:MM","0","pendiente"))
			
			
		else:
			messagebox.showwarning("pendiente","La patente todavia tiene una deuda pendiente")
			
	TxtPatente.delete(0,END)


def EliminarPatente():
	if tabla.selection():
		CE.EliminarPatenteLista(tabla.selection()[0])
		
		MostrarTabla()
	else:
		return messagebox.showwarning("No seleccionado","Elija una patente a eliminar")
			
def ModificarPatente():
	
	if tabla.selection():
		
		NW = Toplevel(ventana,takefocus=True)
		NW.title("Modificar")
		NW.grab_set()
		TxtModPatente = Label(NW,text="Patente")
		EntryModPatente = Entry(NW)
		selected = tabla.focus()
		values = tabla.item(selected, 'values')
		EntryModPatente.insert(0,values[0])
		
		
		
		TxtModPrecio = Label(NW,text="Precio")
		EntryModPrecio = Entry(NW)
		EntryModPrecio.insert(0, values[3])
		
		
		
		
		FechaHoraInicial = values[1].split()
		
		TxtModFechaInicial = Label(NW,text="Fecha Inicial")
		EntryModFechaInicial = Entry(NW)
		EntryModFechaInicial.insert(0, FechaHoraInicial[0])
		
		
		TxtModHoraInicial = Label(NW,text="Hora Inicial")
		EntryModHoraInicial = Entry(NW)
		EntryModHoraInicial.insert(0, FechaHoraInicial[1])
		
		
		FechaHoraFinal = values[2].split()
		
		TxtModFechaFinal = Label(NW,text="Fecha Final")
		EntryModFechaFinal = Entry(NW)
		EntryModFechaFinal.insert(0, FechaHoraFinal[0])
		
		TxtModHoraFinal = Label(NW,text="Hora Final")
		EntryModHoraFinal = Entry(NW)
		EntryModHoraFinal.insert(0, FechaHoraFinal[1])
			
		CBPago = IntVar()
		CBModPago = Checkbutton(NW,text="pago",variable=CBPago)
		if(values[4] == 'pago'):
			CBModPago.select()
			
		PrecioAnterior = values[3]
		BtnMod = Button(NW,text="Modificar",command=lambda:Modificar(tabla.selection()[0],EntryModPatente.get(),EntryModFechaInicial.get(),EntryModHoraInicial.get(),EntryModFechaFinal.get(),EntryModHoraFinal.get(),EntryModPrecio.get(),CBPago.get(),PrecioAnterior))
		
		TxtModPatente.grid(row=0,column=0)
		EntryModPatente.grid(row=1,column=0)
		
		TxtModPrecio.grid(row=0,column=1)
		EntryModPrecio.grid(row=1,column=1)
		
		TxtModFechaInicial.grid(row=2,column=0)
		EntryModFechaInicial.grid(row=3,column=0)
		
		TxtModHoraInicial.grid(row=2,column=1)
		EntryModHoraInicial.grid(row=3,column=1)
		
		TxtModFechaFinal.grid(row=4,column=0)
		EntryModFechaFinal.grid(row=5,column=0)
		
		TxtModHoraFinal.grid(row=4,column=1)
		EntryModHoraFinal.grid(row=5,column=1)
		
		CBModPago.grid(row=6,column=0)
		BtnMod.grid(row=6,column=1)
		
		
		
	else:
		return messagebox.showwarning("No seleccionado","Elija una patente a modificar")
		
	NW.protocol("WM_DELETE_WINDOW",lambda:destroy(NW))

def Modificar(idpatente,patente,fechainicial,horainicial,fechafinal,horafinal,precio,pago,precioanterior):
	
	
	
	try:
		
		fechahorainicial = fechainicial + " " + horainicial
		fechahorafinal = fechafinal + " " + horafinal
		
		diai,mesi,anioi = fechainicial.split("-")
		diaf,mesf,aniof = fechafinal.split("-")
		
		horai,mini = horainicial.split(":")
		horaf,minf = horafinal.split(":")
		
		
		if(len(diai) == 2 and len(mesi) == 2 and len(anioi) == 4 and len(diaf) == 2 and len(mesf) == 2 and len(aniof) == 4 and len(horai) == 2 and len(mini) == 2 and len(horaf) == 2 and len(minf) == 2):
			
		
			startdate =  datetime.strptime(fechahorainicial, '%d-%m-%Y %H:%M')
			enddate =  datetime.strptime(fechahorafinal,'%d-%m-%Y %H:%M')
			dif = abs((enddate - startdate).total_seconds()/60)
			
			
			
			if(fechahorafinal > fechahorainicial):
				
				
				mes  = int(dif / 43200)
				dia  = int((dif % 43200) / 1440)
				hora = int((dif % 1440) / 60)
				minuto = int(dif % 60)
					
				LPxT = CE.ObtenerPreciosXTiempo()
					
				pmes = mes * LPxT[0][3]
				pdia = dia * LPxT[0][2]
				phora = hora * LPxT[0][1]
				pmin =  minuto * LPxT[0][0]
				
				total = 0
				
				if pmes > 0:
					total = pmes
				elif pdia > 0:
					total = pdia
				elif phora > 0:
					total = phora
				else:
					total = pmin
					
			
				if int(precio) != int(precioanterior):
					
					Lista =  [idpatente,patente,fechahorainicial,fechahorafinal,precio,pago]
					
				else:
				
					Lista = [idpatente,patente,fechahorainicial,fechahorafinal,total,pago]
				
				CE.ModificarPatenteLista(Lista)
				messagebox.showinfo(message="Modificacion exitosa", title="Modificacion")
				
			else:
				messagebox.showinfo(message="La fecha de entrada no puede ser mayor que la fecha de salida", title="Fecha Erronea" )
		else:
			messagebox.showinfo(message="Por favor corrija la fecha u hora",title="Formato Erroneo")
			
			
	except:
		messagebox.showinfo(message="Por favor corrija la fecha u hora",title="Formato Erroneo")

def CobrarPatente():
	if tabla.selection():
		
		
		selected = tabla.focus()
		values = tabla.item(selected, 'values')

		if(values[4] == "pendiente"):
			
			date = dt.datetime.now()	
			FFinal=f"{date:%d-%m-%Y %H:%M}"
			
			startdate =  datetime.strptime(values[1], '%d-%m-%Y %H:%M')
			enddate =  datetime.strptime(FFinal,'%d-%m-%Y %H:%M')
			dif = abs((enddate - startdate).total_seconds()/60)
			
			mes  = int(dif / 43200)
			dia  = int((dif % 43200) / 1440)
			hora = int((dif % 1440) / 60)
			minuto = int(dif % 60)
			
			LPxT = CE.ObtenerPreciosXTiempo()
			
			pmes = mes * LPxT[0][3]
			pdia = dia * LPxT[0][2]
			phora = hora * LPxT[0][1]
			pmin =  minuto * LPxT[0][0]
			
			if pmes > 0:
				total = pmes
			elif pdia > 0:
				total = pdia
			elif phora > 0:
				total = phora
			else:
				total = pmin
			
			
			if(messagebox.askyesno(message="Patente: " + values[0]  + "\nFecha de ingreso:\n" + values[1] + "\nFecha de salida:\n"  + FFinal +"\n------------------------"+ "\nTotal a cobrar:" + str(total) +"\nPrecio por mes:"+ str(pmes) + "\nPrecio por dia:" + str(pdia) + "\nPrecio por hora:" + str(phora) + "\nPrecio por minuto:"+ str(pmin) , title="Cobrar")):
				
				CE.CobrarPatenteLista([tabla.selection()[0],values[0],values[1],FFinal,total,1,pmes,pdia,phora,pmin])
				MostrarTabla()
		else:
			return messagebox.showwarning("Pago","Esta deuda ya esta saldada")
	else:
		return messagebox.showwarning("No seleccionado","Elija una patente a cobrar")
		

def BuscarRepeticion(TxtPatente):
	
	for idpatente in tabla.get_children():
		
		var = tabla.item(idpatente)
		if(TxtPatente == var['values'][0]):
			if var['values'][4] == 'pendiente':
				return 1
			
	return 0
	
	
def Ordenar(var):
	global valor
	
	if tabla.get_children():
		if valor:
			consulta = "select idpatente,patente,fentrada,fsalida,precio, iif(pago == 1,'pago','pendiente') from estacionamiento order by " + var + " ASC"
			valor = False
		else:
			consulta = "select idpatente,patente,fentrada,fsalida,precio, iif(pago == 1,'pago','pendiente') from estacionamiento order by " + var  + " DESC"
			valor = True
		tabla.delete(*tabla.get_children())
		for row in CE.OrdenarLista(consulta):
			tabla.insert("",'end',iid=row[0],values=(row[1],row[2],row[3],row[4],row[5]))

def establecerPrecio():
	PxT = [entrymin.get(),entryhor.get(),entrydia.get(),entrymes.get()]
	CE.EstablecerPreciosxTiempo(PxT)
	messagebox.showinfo(message="Precio Establecido",title="Precio")


ventana = Tk()

ventana.title("Estacionamiento")
ventana.resizable(False,False)



parte1 = Frame(ventana,width=400,height=120)
parte2 = Frame(ventana,width=400,height=320)
parte3 = Frame(ventana,width=400,height=60)
parte4 = Frame(ventana,width=400,height=60)

TxtPatente = Entry(parte1)
TxtPatente.pack(side=LEFT)
btnadd = Button(parte1,text="Agregar Patente",command=AgregarPatente)
btnadd.pack(side=LEFT)


tabla = ttk.Treeview(parte2,selectmode='browse')
tabla.pack(side='left')


vsb =  Scrollbar(parte2,orient="vertical",command=tabla.yview)
vsb.pack(side='right', fill='y')
tabla.configure(yscrollcommand=vsb.set)

tabla["columns"] = ("1","2","3","4","5")
tabla["show"]="headings"
tabla.column("1",width = 120)
tabla.column("2",width = 140)
tabla.column("3",width = 150)
tabla.column("4",width = 80)
tabla.column("5",width = 120)

tabla.heading("1",text="Num. Patente",anchor=CENTER,command=lambda:Ordenar('Patente'))
tabla.heading("2",text="Fecha Entrada",anchor=CENTER,command=lambda:Ordenar('FEntrada'))
tabla.heading("3",text="Fecha Salida",anchor=CENTER,command=lambda:Ordenar('FSalida'))
tabla.heading("4",text="Precio",anchor=CENTER,command=lambda:Ordenar('Precio'))
tabla.heading("5",text="pago",anchor=CENTER, command=lambda:Ordenar('Pago'))

MostrarTabla()


btndrop = Button(parte3,text="Eliminar",command=lambda:EliminarPatente())
btnmod = Button(parte3,text="Modificar",command=ModificarPatente)
btncob = Button(parte3,text="Cobrar",command=CobrarPatente)

btndrop.pack(side=LEFT)
btnmod.pack(side=LEFT)
btncob.pack(side=LEFT)

PxT =  CE.ObtenerPreciosXTiempo()

txtprecmin = Label(parte4,text="Min: $").grid(row=0,column=0)
entrymin = Entry(parte4,width=5)
entrymin.insert(0, PxT[0][0])
entrymin.grid(row=0,column=1)

txtprechor = Label(parte4,text="Hr: $").grid(row=0,column=2)
entryhor = Entry(parte4,width=5)
entryhor.insert(0,PxT[0][1])
entryhor.grid(row=0,column=3)

txtprecdia = Label(parte4,text="Dia: $").grid(row=0,column=4)
entrydia = Entry(parte4,width=5)
entrydia.insert(0,PxT[0][2])
entrydia.grid(row=0,column=5)

txtprecmes = Label(parte4,text="Mes: $").grid(row=0,column=6)
entrymes = Entry(parte4,width=5)
entrymes.insert(0,PxT[0][3])
entrymes.grid(row=0,column=7)

btnPrec = Button(parte4,text="Establecer Precio",command=establecerPrecio).grid(row=0,column=8)

parte1.pack()
parte2.pack()
parte3.pack()
parte4.pack()

if __name__ == '__main__':
	
	ventana.mainloop()
