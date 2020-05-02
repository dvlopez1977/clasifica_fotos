#!/usr/bin/python3
import os;
import sys;
import hashlib;
import io;
import yaml;
from shutil import copy
from datetime import datetime;
#from PIL import Image;
#from PIL import UnidentifiedImageError;
import PIL

# algunas constantes
nArg=4 # n'umero de argumentos de entrada
stage=1 # ejecutamos todas las etapas por defecto
datos_fotos='datos_fotos.yml'

def bitacora(rutaBitacora, mensaje):
    print("{}: {}".format(rutaBitacora, mensaje))
    file=open(rutaBitacora, "a+")
    file.write(mensaje + "\n")
    file.close()

def muestraError(mensajeError="Error generico: el programador ha sido demasiado vago para especificar que ha pasado"):
    print (mensajeError)

def comoUsar(mensajeError="Error generico: el programador ha sido demasiado vago para especificar que ha pasado"):
    muestraError(mensajeError)
    print ("Este programa recorre un directorio lleno de fotos")
    print ("y las clasifica en un directorio destino por anho y mes")
    #print ("Trabaja en tres etapas:")
    print ("   1 - calculate the data for the files")
    print ("   2 - calculate the list of non duplicated files")
    print ("   3 - copy files to the destination folder")
    print ("Recibe como parametros: ")
    print (" Si la etapa es 1, entonces los siguientes parametros son la ruta donde se almacenan las fotos y la ruta donde queremos guardar las fotos clasificadascontiene las fotos")
    print (" 2-. La ruta al directorio donde queremos clasificar las fotos")

def esDirectorio(ruta):
	if os.path.isdir(ruta):
		# error, la ruta introducida no es un directorio
		return True
	else:
		return False

def calcularMD5sum(rutaAbsoluta, tamanoFragmento=io.DEFAULT_BUFFER_SIZE):
	md5 = hashlib.md5()
	with io.open(rutaAbsoluta, mode="rb") as fd:
		for pedazo in iter(lambda: fd.read(tamanoFragmento), b''):
			md5.update(pedazo)
	return md5

def obtenerFechaFoto(rutaAbsoluta):
	foto= Image.open(rutaAbsoluta)
	fechaFoto= foto._getexif()[36867]
	foto.close()
	return fechaFoto

def crearDirectorio(ruta):
# dada una ruta intenta crearla, si no puede devuelve error
	print ("Intento crear el directorio " + ruta)
	try:
		os.makedirs(ruta)
		return True
	except OSError:
		return False

def hayDuplicado(ruta, md5sum, DirectorioDestino):
#Dentro de DirectorioDestino tiene que haber un fichero csv con los campos:
# 1-. md5sum del fichero
# 2-. nombre del fichero
	# empezamos, si no existe el fichero csv, lo creamos
	if not os.path.isfile(DirectorioDestino + "fotos.csv"):
		return False
	return True

def copiarFoto(foto):
# Copia una foto al directorio destino.
# foto es una lista que:
# foto[0] ruta origen
# foto[1] directorio destino
	# if not esDirectorio(foto[1]):
	# 	crearDirectorio(foto[1])
	rutaDestino=os.path.join(foto[1], foto[2])
	copy(foto[0],foto[1])

def seleccionaNombre(nombre, DirectorioFoto):
# si el fichero DirectorioFoto/nombre ya existe le anhadimos un contador a nombre
	i=0
	nombreTemp=nombre
	absolutePath=os.path.join(DirectorioFoto, nombreTemp)
	while os.path.exists(absolutePath):
		i+=1
		nombreTemp= nombre + str(i)
		absolutePath=os.path.join(DirectorioFoto, nombreTemp)
	return nombreTemp

def calcularFileType(ruta_absoluta):
    #super easy, we return the extension of the file
    type = ruta_absoluta.split('.')[-1]
    return type


def stage1(ruta_fotos):
    datos_fotos="datos_fotos.yml"
# En la etapa calculamos los datos de cada fichero
#
    #src path for the file --> this is the key for the dictionary
    #md5 sum
    #file type
    #error type
    #dst path for the file, it will include the month and year in which the photo was shoot if the file is a photo and if that data is available
    df=dict()
# si tenemos datos de una ejecucion anterior, los cargamos
    if os.path.exists(os.path.join(ruta_fotos, datos_fotos)):
    # cargamos los md5sums de las fotos que se crearon
        parcial=open(os.path.join(ruta_fotos, datos_fotos),'r')
        df=yaml.load(parcial)
        close(parcial)
        # en este punto hemos cargado los datos de una ejecucion parcial anterior
    # Recorremos todos los ficheros que encontremos en 'ruta_fotos'
    for ruta,dirs,archs in os.walk(ruta_fotos.encode('utf-8', 'surrogateescape').decode('utf-8')):
        for archivo in archs:
            ruta_absoluta=os.path.join(ruta, archivo)
            if not ruta_absoluta in df:
                # es la primera vez que procesamos el archivo
                datos_archivo = dict()
                datos_archivo['md5']=calcularMD5sum(ruta_absoluta)
                datos_archivo['file_type']=calcularFileType(ruta_absoluta)
                datos_archivo['error_type']='NONE'
                try:
                    datos_archivo['date']=obtenerFechaFoto(ruta_absoluta)
                except TypeError:
                    datos_archivo['error_type']='TypeError'
                except KeyError:
                    datos_archivo['error_type']='KeyError'
                except AttributeError:
                    datos_archivo['error_type']='AttributeError'
                except UnidentifiedImageError:
                    datos_archivo['error_type']='UnidentifiedImageError'
                except UnicodeEncodeError:
                    datos_archivo['error_type']='UnicodeEncodeError'
                except :
                    datos_archivo['error_type']='UnknownError'
                datos_archivo['dst_path']='' #no es relevante todavia
                datos_archivo['src_path']=ruta_absoluta
                df[ruta_absoluta]=datos_archivo
    # en este punto tenemos todos los datos en memoria, hay que volcarlos a disco
    parcial= open(os.path.join(ruta_fotos, datos_fotos),'w')
    yaml.dump(df, stream=parcial)
    parcial.close()

    return true

#
# Programa principal
#

# comprobaci'on de pre condiciones
# ?hemos recibido el numero correcto de parametros?
if len(sys.argv) != nArg:
	# error, mostramos la informaci'on de uso y salimos
	comoUsar()
	sys.exit(1)
else:
	print ("Numero de par'ametros correcto " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3])

# ?los parametros que hemos recibido son directorios?

if not esDirectorio(sys.argv[2]):
	comoUsar(mensajeError="El segundo parametro {} no es un directorio".format(sys.argv[2]))
	sys.exit(1)

if not esDirectorio(sys.argv[3]):
	if os.path.exists(sys.argv[3]):
		# la ruta existe pero es un fichero regular, devolvemos error
		comoUsar(mensajeError="El tercer parametro " + sys.argv[3] + " es un fichero regular")
		sys.exit(1)
	else:
		# la ruta destino no existe, la intentamos crear
		if crearDirectorio(sys.argv[3]):
			print ("Directorio de destino: " + sys.argv[3] + " creado correctamente")
		else:
			muestraError("No pude crear el directorio de destino: " + sys.argv[3])
			sys.exit(1)

# Obtengo los parametros de entrada
NombrePrograma=sys.argv[0].split(sep="/")[-1]
print(NombrePrograma)
DirectorioOrigen=sys.argv[2]
DirectorioDestino=sys.argv[3]
ahora=datetime.now().strftime("%Y%m%d-%H%M%S")
rutaBitacora=os.path.join(DirectorioDestino, NombrePrograma + "-" + ahora + ".txt")
bitacora(rutaBitacora,"ORIGEN,DESTINO,FECHA,ERROR")
print(DirectorioDestino)
Fotos=dict()
# Obtengo la lista de archivos en un directorio


for ruta,dirs,archs in os.walk(DirectorioOrigen.encode('utf-8', 'surrogateescape').decode('utf-8')):
    print ("la ruta es : {}".format(ruta))
    #	for dir in dirs:
#            print("directorio: {}".format(dir))
#        for a in archs:
#            print("archivo: {}".format(a))
print("saliendo que es gerundio")
sys.exit(0)
# ?hay una ejecuci'on anterior que no se completo?
if os.path.exists(os.path.join(sys.argv[2], "EjecucionParcial.yml")):
# cargamos los md5sums de las fotos que se crearon
	parcial=open(os.path.join(sys.argv[2], "EjecucionParcial.yml"),'r')
	Fotos=yaml.load(parcial)
	parcial.close()
try:
	for ruta,dirs,archs in os.walk(DirectorioOrigen.encode('utf-8', 'surrogateescape').decode('utf-8')):
		for archivo in archs:
#			archivo=archivo.encode('utf-8', 'surrogateescape').decode('utf-8')
			print("working with archive {}".format(archivo))
			# calculamos el nombre, el md5, y la fecha
			error="NO"
			nombre= os.path.join(ruta, archivo)
			nombre=nombre.encode('utf-8', 'surrogateescape').decode('ISO-8859-1')
			md5sum= calcularMD5sum(nombre)
			try:
				fecha= obtenerFechaFoto(nombre)
				anho= fecha[:4]
				mes= fecha[5:7]
				DirectorioFoto=os.path.join(DirectorioDestino, anho, mes + '/')
# TypeError: 'NoneType' object is not subscriptable
			except TypeError:
				error="SI"
				fecha="Error/TypeError"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')
			except KeyError:
				error="SI"
				fecha="Error/KeyError"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')
			except AttributeError:
				error="SI"
				fecha="Error/AttributeError"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')
			except UnidentifiedImageError:
				error="SI"
				fecha="Error/NoFoto"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')
# UnicodeEncodeError: 'utf-8' codec can't encode character '\udcaa' in position 120: surrogates not allowed
			except UnicodeEncodeError:
				error="SI"
				fecha="Error/UnicodeEncodeError"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')
			except KeyboardInterrupt:
				raise
			except :
				error="SI"
				fecha="Error/Unknown"
				DirectorioFoto=os.path.join(DirectorioDestino, fecha + '/')

			if md5sum.hexdigest() not in Fotos:
				try:
# En este punto sabemos que la imagen es unica (no hay otra con el mismo md5sum),
# sin embargo puede haber un fichero con el mismo nombre y una imagen diferente procedente de otra camara
# si DirectorioFoto/nombre ya existe entonces tenemos que cambiar el nombre al fichero para no sobrescribir
# la foto con otra cuyo nombre de fichero es el mismo
# en nombre tenemos la ruta absoluta al fichero origen, necesitamos solo el nombre del fichero
					nombreFichero=nombre.split('/')[-1]
					nombreDestino=seleccionaNombre(nombreFichero, DirectorioFoto)

					foto=[nombre, DirectorioFoto, nombreDestino, fecha, error]
					Fotos[md5sum.hexdigest()]=foto
#				copiarFoto(foto)
					bitacora(rutaBitacora, nombre + "," + DirectorioFoto + "/" + nombreDestino + "," + fecha + "," + error)
				except UnicodeEncodeError:
					nombre=nombre.encode('utf-8', 'surrogateescape').decode('ISO-8859-1')
					print("problema al trabajar con {}".format(nombre))
			else:
				try:
					fecha="DUPLICADO"
					bitacora(rutaBitacora, nombre + "," + Fotos[md5sum.hexdigest()][0] + "," + fecha + "," + error)
				except UnicodeEncodeError:
					print("un problema al dectectar un duplicado {}".format(nombre))
	try:
		print("Comienzo a copiar fotos")
		for foto in Fotos:
			print(Fotos[foto])
			copiarFoto(Fotos[foto])
	except UnicodeEncodeError:
		print("Problema intentando copiar fichero {}".format(foto))
except :
# volcamos el trabajo parcial en "EjecucionParcial.yml" y terminamos
#	print(Fotos)
	print("Ha habido una excepcion trabajando con el fichero {}".format(nombre))
	parcial= open(os.path.join(sys.argv[2], "EjecucionParcial.yml"),'w')
	yaml.dump(Fotos, stream=parcial)
	parcial.close()
	raise

