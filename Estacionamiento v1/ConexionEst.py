import sqlite3
import datetime as dt

def AgregarPatenteLista(Patente,finicio,ffinal,precio,pago,tiempo):
	date = dt.datetime.now()
	format_date=f"{date:%d-%m-%Y %H:%M}"
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("Insert into estacionamiento (Patente,Fentrada,Fsalida,Precio,Pago,minuto,hora,dia,mes) values ('"+ Patente  +"','" + finicio  +"','"+ ffinal +"',"+ precio +","+ pago + ","+ tiempo[0] +"," + tiempo[1] + "," + tiempo[2] + "," + tiempo[3]+ ")")
	conn.commit()
	conn.close()

def ModificarPatenteLista(Lista):
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("update estacionamiento set patente = '" + Lista[1] + "' , FEntrada = '"+Lista[2]+"' , FSalida = '"+ Lista[3]+ "'  , precio  = "+ str(Lista[4]) + ", pago = " + str(Lista[5]) + " where idpatente = '"+ str(Lista[0]) +"'")
	x = conn.commit()
	conn.close()

def CobrarPatenteLista(Lista):
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("update estacionamiento set patente = '" + Lista[1] + "' , FEntrada = '"+Lista[2]+"' , FSalida = '"+ Lista[3]+ "'  , precio  = "+ str(Lista[4]) + ", pago = " + str(Lista[5]) + ",minuto =" +str(Lista[6]) + ",hora ="+ str(Lista[7])+",dia =" +str(Lista[7])+ ",mes = " +str(Lista[8])+ " where idpatente = '"+ str(Lista[0]) +"'")
	x = conn.commit()
	conn.close()
	
def EstablecerPreciosxTiempo(PxT):
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("update horarios set minutos = " + PxT[0]+", horas = "+PxT[1]+" , dias = "+PxT[2]+"  , mes  = "+ PxT[3] + " ")
	x = conn.commit()
	conn.close()

def ObtenerPreciosXTiempo():
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("select minutos,horas,dias,mes from horarios")
	x = c.fetchall()
	conn.close()
	return x

def OrdenarLista(consulta):
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute(consulta)
	x = c.fetchall()
	conn.close()
	return x

def EliminarPatenteLista(idpat):
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("Delete from estacionamiento where idPatente ='" +idpat+"'")
	conn.commit()
	conn.close()
	
def obtenerLista():
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("select idpatente,patente,fentrada,fsalida,precio,pago from estacionamiento")
	x = c.fetchall()
	conn.close()
	return x

def ObtenerSiguienteIdPatente():
	conn = sqlite3.connect('est.db')
	c = conn.cursor()
	c.execute("SELECT IdPatente FROM estacionamiento ORDER BY IdPatente DESC LIMIT 1")
	x = c.fetchall()
	conn.close()
	return x
