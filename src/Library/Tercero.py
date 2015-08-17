
import maya.cmds as cmds
import random
from functools import partial
import math


#Creamos la interfaz grafica
def UI():

	#Comprobamos que no se este ejecutando el algoritmo
	if(cmds.window("Tercer_Algoritmo", exists = True)):
		cmds.deleteUI("Tercer_Algoritmo")

	#Creamos la ventana
	window = cmds.window("Tercer_Algoritmo", title = "Tercer Algoritmo", widthHeight=(265, 430), s = False, menuBar = True)
		
	cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )

	#Aniadimos los campos a la ventana
	cmds.text(label="Ancho", al = "left")
	Anchura = cmds.textField( tx = "750")

	cmds.text(label="Largo", al = "left")
	Largo = cmds.textField( tx = "750")

	cmds.text(label="Altura maxima", al = "left")
	Amaxima = cmds.textField( tx = "100")
	
	cmds.text(label = "Decoracion en los edificios", al = "left")
	Deificios = cmds.textField( tx = "2")
	
	cmds.text(label = "Ancho de la calle", al = "left")
	Acalle = cmds.textField( tx = "16")
	
	cmds.text(label = "Tamanio del bloque", al = "left")
	Tamanio_Bloque = cmds.textField( tx = "125")

	#Barra de pogreso
	Barra_progreso = cmds.progressBar(maxValue=100, width=100, vis = False)

	#Boton para generar	
	cmds.button(label = "Generar", c = partial(Tercer_Algoritmo, Anchura, Largo, Amaxima, Deificios, Acalle, Tamanio_Bloque, Barra_progreso ))
	
	#Mostramos la ventana
	cmds.showWindow(window)


def Tercer_Algoritmo(Anchura, Largo, Amaxima, Deificios, Acalle, Tamanio_Bloque, Barra_progreso,  *args): 

	#Edificios definidos por el usuario
	Array_edificios_creados = get_Array_edificios_creados()
	
	#Leemos los campos de la interfaz
	Anchura = int(cmds.textField(Anchura, q=True, text=True))
	Largo = int(cmds.textField(Largo, q=True, text=True))
	Amaxima = int(cmds.textField(Amaxima, q=True, text=True))
	Deificios = int(cmds.textField(Deificios, q = True, text = True))
	Acalle = int(cmds.textField(Acalle, q = True, text = True))
	Tamanio_Bloque = int(cmds.textField(Tamanio_Bloque, q = True, text = True))

	#Tamanios por defecto para el maximo de los edificios
	Tamanio_base_eje_x = 20
	Tamanio_base_eje_z = 20
	Anchra_min_edificio = 5
	Largo_min_edificio = 3
	
	#Espacio por defecto entre edificios
	Espacio_eje_x = 0
	Maximo_eje_x = 0
	aux = 0
	aux_x = 0
		
	#Grupo de edificios a usar
	cmds.group( em = True, n = "generar_edificios")
	cmds.group( em = True, n = "calle")
	cmds.group( em = True, n = "calle")
	cmds.group( em = True, n = "calle")

	#Creamos el plano del suelo
	cmds.polyPlane(w = Anchura, h = Largo, n = "malla_suelo")
	cmds.move(Anchura / 2, 0, Largo / 2)
	
	#Array donde se van a insertar los edificios creados
	Edificios = []
	

	#generamos las columnas
	while(Espacio_eje_x < Largo ):
		
		#Reiniciamos el contador para cada columna
		contador = 0
		
		#Generamos fila
		while(contador < Anchura):
			
			#Creamos un edificio
			if(len(Array_edificios_creados) > 0):
				
				#Seleccionamos uno de los edificos aleatoriamente
				edififio_seleccionado = random.randrange(1, len(Array_edificios_creados))
				edificio = cmds.duplicate(Array_edificios_creados[edififio_seleccionado])
				
				#Escalamos los edificios para que se vean uniformes
				escala_edificios = randrange_float(.5, 2, .1)
				cmds.scale(escala_edificios, escala_edificios, escala_edificios, edificio )
				
				#Reseteamos las transformaciones (http://download.autodesk.com/us/maya/2011help/CommandsPython/makeIdentity.html)
				cmds.makeIdentity(edificio, apply=True, t=1, r=1, s=1, n=0)
				
				#Aplicamos transformaciones a los edificios
				Transformacion_x = cmds.xform(edificio, q = True, bb = True)[3] - cmds.xform(edificio, q = True, bb = True)[0]
				Transformacion_y = cmds.xform(edificio, q = True, bb = True)[4] - cmds.xform(edificio, q = True, bb = True)[1]
				Transformacion_z = cmds.xform(edificio, q = True, bb = True)[5] - cmds.xform(edificio, q = True, bb = True)[2]

				
				#comprobamos si el edificio puede ir en esa posicion
				if(Transformacion_x > Maximo_eje_x):
					Maximo_eje_x = Transformacion_x
				
				#Comprobamos si molesta a su edificio contiguo
				for z in range(contador - 1, contador + Transformacion_z + Deificios + 1):
					if( z % Tamanio_Bloque == 0 ):
						#Creamos calles
						segmento_calle = cmds.polyPlane( h = Acalle, w = Maximo_eje_x, sx = 1, sy = 1)
						cmds.move( Espacio_eje_x + (Maximo_eje_x/2), 0.01, z + (Acalle/2))
						cmds.parent(segmento_calle[0], "calle")
						contador = z + Acalle + Deificios
						break
				
				
				cmds.parent(edificio, "generar_edificios")
				cmds.move( (Espacio_eje_x + (Transformacion_x/2)), 0, (contador + (Transformacion_z/2) ) )

			else:
			
				#Si no, volvemos a calcular el random
				Anchura_random = random.randrange(Largo_min_edificio, Amaxima)
				if(random.randrange(0, 100) > 90):
					Anchura_random = Anchura_random + (Anchura_random * 0.7)
				Transformacion_z = random.randrange(Anchra_min_edificio, Tamanio_base_eje_z)
				Transformacion_x = random.randrange(Anchra_min_edificio, Tamanio_base_eje_x)
				
				#Comprobamos si el edificio no se sale de la fila
				if(Transformacion_x > Maximo_eje_x):
					Maximo_eje_x = Transformacion_x
				
				#Comprobamos si molesta a su edificio contiguo
				for z in range(contador - 1, contador + Transformacion_z + Deificios + 1):
					if( z % Tamanio_Bloque == 0 ):
						#Creamos calles
						segmento_calle = cmds.polyPlane( h = Acalle, w = Maximo_eje_x + Deificios, sx = 1, sy = 1)
						cmds.move( Espacio_eje_x + (Maximo_eje_x/2), 0.01, z + (Acalle/2))
						cmds.parent(segmento_calle[0], "calle")
						contador = z + Acalle + Deificios
						break
				
				edififio_seleccionado = random.randrange(0,3)
				edificio = Edificio(Transformacion_x, Transformacion_z, Anchura_random, edififio_seleccionado)
				
				Edificios.append(edificio)
				Edificios[aux].crear()
				cmds.parent( Edificios[aux].EdificioName, "generar_edificios")

				#Colocamos el edificio en su lugar
				Edificios[aux].mover_edificio( (Espacio_eje_x + (Transformacion_x/2)), (Anchura_random / 2), (contador + (Transformacion_z/2) ) )
			
			#Actualizamos la barra de progreso
			progressInc = cmds.progressBar(Barra_progreso, edit=True, maxValue = (Largo), pr = Espacio_eje_x, vis = True)
			
			#Cargamos el espacio para el proximo edificio
			contador = contador + Transformacion_z + Deificios
			
			aux += 1
			print "aux_x = " + str(aux_x)
			
		
		if aux_x == 1:
			print "Creando calle"
			segmento_calle = cmds.polyPlane( h = Anchura, w = Acalle + Deificios, sx = 1, sy = 1)
			cmds.move( Espacio_eje_x + (Acalle/2) + Maximo_eje_x + Deificios, 0.01, Anchura/2)
 			cmds.parent(segmento_calle[0], "calle")

			Espacio_eje_x = Espacio_eje_x + Acalle + Maximo_eje_x + (Deificios*2)
			aux_x = 0
		else:
			aux_x += 1
			Espacio_eje_x = Espacio_eje_x + (Maximo_eje_x) + Deificios
		

	
	#Actualizamos la barra de progreso
	progressInc = cmds.progressBar(Barra_progreso, edit=True, maxValue = 100, pr = 0, vis = False)
	
	#Unimos las calles
	calles = cmds.listRelatives("calle", c = True)
	cmds.select(calles)
	cmds.polyUnite(n = "combinacion_calles")
	cmds.delete(ch = True)
	



class Edificio:

	contador_edificios = 0
	
	#constructor	
	def __init__(self, anchura_edificio, Largo_edificio, Anchura_random_edificio, tipo_edificio):
		self.anchura = anchura_edificio
		self.Anchura_random = Anchura_random_edificio
		self.Largo = Largo_edificio
		self.edififio_seleccionado = tipo_edificio
		Edificio.contador_edificios += 1
		self.EdificioName = "Edificio_" + str(self.contador_edificios)
		self.xDiv = 10
		self.yDiv = 10
		self.zDiv = 10
	
	
	#funcion para generar edificio
	def crear(self):
			
		#Tipo 1
		if(self.edififio_seleccionado == 0):
			cmds.polyCube(w = self.anchura, d = self.Largo, h = self.Anchura_random, n =  str(self.EdificioName))
			
		#Tipo 2
		elif(self.edififio_seleccionado == 1):
		
			cmds.polyCube(w = self.anchura, d = self.Largo, h = self.Anchura_random, n =  str(self.EdificioName))
			
			#Modificamos las caras aleatoriamente
			for i in range(0, random.randrange(0,3)):
				cmds.polyExtrudeFacet(str(self.EdificioName) + ".f[1]", kft = False, ls = (0.8, 0.8, 0))
				cmds.polyExtrudeFacet(str(self.EdificioName) + ".f[1]", kft = False, ltz = 30)	
			
		#Tipo 3	
		else:
			cmds.polyCube(w = self.anchura, d = self.Largo, h = self.Anchura_random, sx = self.xDiv, sy = self.yDiv, sz = self.zDiv, n = str(self.EdificioName))			
			
			sides = []
			
			#Seleccionamos el edificio
			for i in range(0, 8):
				if(i != 1 and i != 3):
					sides.append(str(self.EdificioName) + ".f[" + str(self.xDiv * self.yDiv * i) + ":" + str((self.xDiv * self.yDiv * (i+1)) - 1) + "]")
			
			#Modificamos las caras para generar ventanas
			cmds.polyExtrudeFacet(sides[0], sides[1], sides[2], sides[3], sides[4], sides[5], kft = False, ls = (0.8, 0.8, 0))
			windows = cmds.ls(sl = True)
			cmds.polyExtrudeFacet(windows[1], windows[2], windows[3], kft = False, ltz = -0.2)
			cmds.select( self.EdificioName)
				
	#Mueve un edificio
	def mover_edificio(self, x, y, z):
		cmds.select(self.EdificioName)
		cmds.move(x, y, z)
		cmds.select( cl = True)


#devolvemos array de edificios generados por el usuario
def get_Array_edificios_creados(*args):
	
	Array_edificios_creados = []
	
	group = cmds.ls(sl=True)
	
	if(len(group) > 0):
		Array_edificios_creados = cmds.listRelatives(group, c = True)

			
	return Array_edificios_creados



#randrange_float funcion obtenida de stackoverflow.com/questions/11949179/how-to-get-a-random-float-with-step-in-python
def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start