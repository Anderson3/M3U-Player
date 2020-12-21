

import sys, os
import PyQt5
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox, QWidget, QInputDialog, QLineEdit, QFileDialog, QAction, qApp
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer

import datetime

#os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    print('AA_EnableHighDpiScaling')

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    print('AA_EnableHighDpiScaling')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




import threading
import time
import vlc
import os
import sys

from pprint import pprint

global aux
aux = True

global comando
comando = 'parar'

global canal
canal = 1

global fist_exec
#auto_exec = True --- ativar posterior mente
auto_exec = False #--- desativar posterior mente

global duracao
duracao = 0

global volume
volume = 70

global midia_atual
midia_atual = None

global pl
global pl_simp

global duracao_total
duracao_total = 1

global novo_tempo

global tipo_midia
tipo_midia = 'stream'

global tempo_atual
global tempo_agora

global pesquisa
pesquisa = False

global pl_simp_pesq
pl_simp_pesq = []

global pl_pesq
pl_pesq = []


pl = []
pl_simp = []
def extrair_links(arquivo):
	global pl
	global pl_simp

	try:

		f = open(arquivo, encoding="utf8")
		line = f.readline()

		pl = []
		pl_simp = []

		cont = 1
		while line:
			if "#EXTINF:" in line:
				ch = line.split(',')[1].strip()
				url = f.readline().strip()
				pl.append([cont,ch,url])
				cont+=1
			line = f.readline()
		f.close()

		for i in pl:
			#print(i[0],' - ',i[1])
			aux = str(str(i[0])+' - '+str(i[1]))
			pl_simp.append(aux)

		print('- lista carregada: links extraidos')
		#print(pl_simp)

	except Exception as e:
		raise e
	


arquivo = 'arquivos m3u/tv_channels_Adr2020_plus.m3u'
extrair_links(arquivo)



def fun1():
	global canal
	global comando
	global auto_exec
	global volume
	global duracao_total
	global novo_tempo
	global duracao
	global tipo_midia
	global tempo_atual
	global tempo_agora
	global pesquisa
	global pl_pesq

	#volume = 70

	if pesquisa == False:
		canal_link = pl[int(canal)][2]
		print("canal_link",canal_link)
	else:
		canal_link = pl_pesq[int(canal)][2]
		print("canal_link",canal_link)
		pprint(pl_pesq)
		#pesquisa = False

	Instance = vlc.Instance('--no-embedded-video --video-x=100 --video-y=100')
	player = Instance.media_player_new()
	Media = Instance.media_new(canal_link)
	Media.get_mrl()
	player.set_media(Media)
	player.audio_set_volume(volume)

	#duration = player.get_length() / 1000
	#mm, ss = divmod(duration, 60)

	#print('Duração da Midia: ',duration,'-Minutos: ',mm,'-Segundos: ',ss)

	
	global aux
	duration = mm = ss = 0


	if auto_exec == True:
		#print('Primeira excução')
		#time.sleep(10)
		comando = 'iniciar'
		auto_exec = False


	while aux == True:

		if comando == 'iniciar':
			player.play()

			duracao = player.get_length()

			if duracao > 1:
				millis = int(duracao)
				seconds=(millis/1000)%60
				seconds = int(seconds)
				minutes=(millis/(1000*60))%60
				minutes = int(minutes)
				hours=(millis/(1000*60*60))%24

				if round(hours) == 0:
					duracao_total = str(minutes)+':'+str(seconds)
				else:
					duracao_total = str(round(hours))+':'+str(minutes)+':'+str(seconds)

				tipo_midia = 'video'
			else:
				tipo_midia = 'stream'
			

		elif comando == 'pausar':
			player.pause()

		elif comando == 'parar':
			player.stop()

		elif comando == 'volume':
			player.audio_set_volume(volume)

		elif comando == 'definir_tempo':
			fator = (novo_tempo/duracao)
			#print('fator: ',fator)
			player.set_position(fator)
			comando = 'iniciar'

			#print('Duração Total: ', duracao)
			#print('Tempo especificado: ', novo_tempo)

		elif comando == 'fechar':
			print('- opção canal utilizada')
			player.stop()
			comando = 'abrir'
			fun1()
			break

		try:
			tempo_agora = player.get_time()
			tempo_atual = player.get_time()

			millis = int(tempo_atual)
			seconds=(millis/1000)%60
			seconds = int(seconds)
			minutes=(millis/(1000*60))%60
			minutes = int(minutes)
			hours=(millis/(1000*60*60))%24

			if round(hours) == 0:
				tempo_atual = str(minutes)+':'+str(seconds)
			else:
				tempo_atual = str(round(hours))+':'+str(minutes)+':'+str(seconds)

			#print(tempo_atual)

		except Exception as e:
			print('- tempo atual não definido')

		#print('Duração: ', duration)
		#print('-Minutos: ', mm,' - Segundos: ', ss)
		time.sleep(1)

	


a = threading.Thread(target=fun1)
a.start()




# ------ Função responsável por execultar outro comando depois que a interface gráfica do Pyqt5 for fechada.
# --- essa função altera o valor de aux e sai da thread destinada a instancia do vlc
def appExec():
	global aux

	app = QApplication(sys.argv)
	a_window = Aplicacao()
	dev_window = Info_dev()
	app.exec_()

	print("janela do PyQt5 finalizada")
	aux = False


class Aplicacao(QMainWindow):

	def __init__(self):
		super().__init__()
		self.ui = None
		self.load_ui()
		self.load_signals()
		self.setWindowTitle('m3uPlayer - Teste')

		#-- horizontal sliders ----------------------------------------------------------
		self.horizontalSlider.setMinimum(0)
		self.horizontalSlider.setMaximum(100)
		self.horizontalSlider.setValue(0)
		self.horizontalSlider.setSingleStep(2)

		self.horizontalSlider_2.setMinimum(1)
		self.horizontalSlider_2.setMaximum(125)
		self.horizontalSlider_2.setValue(70)

		#-- timers ----------------------------------------------------------
		self.timer=QTimer()
		self.timer.timeout.connect(self.att_duracao)
		self.timer.start(1000)

		self.timer_2=QTimer()
		self.timer_2.timeout.connect(self.att_slide_tempo)
		self.timer_2.start(10000)

		#-- actions ----------------------------------------------------------
		self.actionAbrir_arquivo_m3u.setShortcut('Ctrl+A')
		self.actionAbrir_arquivo_m3u.setStatusTip("Abrir arquivos .m3u do seu local ...")
		self.actionAbrir_arquivo_m3u.triggered.connect(lambda: self.funcoes_menu('abrir'))

		self.actionFechar_arquivo_m3u.setShortcut('Ctrl+F')
		self.actionFechar_arquivo_m3u.setStatusTip("Fechar arquivos .m3u do seu local ...")
		self.actionFechar_arquivo_m3u.triggered.connect(lambda: self.funcoes_menu('fechar'))

		#self.actionSair = QAction(QIcon('exit.png'), '&Exit', self)
		self.actionSair.setShortcut('Ctrl+Q')
		self.actionSair.setStatusTip('Sair da aplicação.')
		self.actionSair.triggered.connect(lambda: self.funcoes_menu('sair'))
		

	def load_ui(self):
		self.ui = loadUi(resource_path('nm3uplayer.ui'),self)
		self.ui = loadUi(resource_path('m3u.ui'),self)
		self.show()

	def load_signals(self):
		self.carregar_lista()

		self.listWidget.doubleClicked.connect(self.clicado_lista)

		self.pushButton.clicked.connect(self.iniciar)
		self.pushButton_2.clicked.connect(self.parar)
		#self.listWidget.clicked.connect(self.clicado_lista)
		
		self.pushButton_3.clicked.connect(self.avancar)
		self.pushButton_4.clicked.connect(self.voltar)

		self.toolButton_3.clicked.connect(self.abrir_arquivos)
		self.toolButton_2.clicked.connect(self.limpar_lista)

		self.horizontalSlider.sliderReleased.connect(self.alterar_tempo_midia)
		self.horizontalSlider_2.valueChanged.connect(self.alterar_volume)

		self.toolButton_4.clicked.connect(self.pesquisa)
		self.toolButton.clicked.connect(self.limpar_pesq)


	def pesquisa(self):
		global pl
		global pl_simp
		global pesquisa
		global pl_simp_pesq
		global pl_pesq

		try:
			palavra = str(self.lineEdit.text())
			#print(palavra)

			pl_simp_pesq = []
			pl_pesq = []

			cont_1 = 0
			for i in pl:
				#print(i)
				aux_concat = str(i[1])+' '+str(i[2])
				#print(aux_concat)
				if palavra.lower() in aux_concat.lower():
					#pl_simp_pesq.append(aux_concat)
					#pl_pesq.append(i)
					pl_simp_pesq.insert(0, aux_concat)
					pl_pesq.insert(0, i)

			self.limpar_lista()

			cont_2 = 0
			for i in pl_simp_pesq:
				i = str(i).split('http')[0]
				self.listWidget.insertItem(cont_2, i)
				cont_2+=1

			pesquisa = True
			#pprint(pl_simp_pesq)

		except Exception as e:
			print('[!] Erro - ocorreu um erro durante a pesquisa de termos na lista - ', e)
		

	def limpar_pesq(self):
		global pesquisa
		pesquisa = False
		self.limpar_lista()
		self.lineEdit.setText('')
		self.carregar_lista()



	def info_dev(self):
		dev_window.show()

	def funcoes_menu(self, option):
		global aux

		print("click", option)

		if option == 'abrir':
			self.abrir_arquivos()
		elif option == 'fechar':
			self.limpar_lista()
		if option == 'sair':
			QApplication.closeAllWindows()
			#qApp.quit


	def att_slide_tempo(self):
		global tempo_agora
		global duracao
		global tipo_midia


		if tipo_midia != 'stream':
			
			try:
				tempo_agora_m = str(tempo_agora)[0:(len(str(tempo_agora))-1)]
				duracao_m = str(duracao)[0:(len(str(duracao))-1)]
				#print('tempo_agora: ',tempo_agora)
				#print('duracao: ',duracao)
				#posicao_atual_m = round(int(tempo_agora_m)/int(duracao_m), 5)
				posicao_atual_m = int(tempo_agora_m)/int(duracao_m) * 100
				print('posicao_atual: ',posicao_atual_m)
				#self.horizontalSlider.setValue(posicao_atual_m * 100)
				self.horizontalSlider.setValue(posicao_atual_m )

			except Exception as e:
				print('[!] Erro - erro no load do horizontalSlider')
		


	def limpar_lista(self):
		pl = []
		pl_simp = []
		self.listWidget.clear()


	def carregar_lista(self):
		#print(pl_simp)
		cont = 0
		for i in pl_simp:
			self.listWidget.insertItem(cont, str(pl_simp[cont]))
			cont += 1


	def clicado_lista(self):
		global canal
		global comando
		global auto_exec
		global midia_atual
		global pesquisa

		item  = self.listWidget.currentRow()
		canal = item
		print('- canal escolhido: ', item+1)

		comando = 'fechar'
		auto_exec = True

		self.horizontalSlider.setValue(0)

		midia_atual = self.listWidget.currentItem().text()
		self.att_reproducao()



	def iniciar(self):
		print('iniciar')
		global comando
		comando = 'pausar'

		self.horizontalSlider.setValue(0)

		self.att_reproducao()
		self.att_duracao()

	def parar(self):
		print('parar')
		global comando
		global duracao_total
		global tipo_midia
		comando = 'parar'
		duracao_total = 1
		tipo_midia = 'stream'

		self.horizontalSlider.setValue(0)
		self.att_duracao()

	def pausar(self):
		print('pausar')
		global comando
		comando = 'iniciar'

	def avancar(self):
		print('avançar')
		global canal
		global comando
		global auto_exec
		global midia_atual

		item  = self.listWidget.currentRow()
		canal = item+1
		print('- canal escolhido: ', item+2)

		comando = 'fechar'
		auto_exec = True

		self.horizontalSlider.setValue(0)

		midia_atual = self.listWidget.currentItem().text()
		self.att_reproducao()


	def voltar(self):
		print('voltar')
		global canal
		global comando
		global auto_exec
		global midia_atual

		item  = self.listWidget.currentRow()
		canal = item-1
		print('- canal escolhido: ', item-2)

		comando = 'fechar'
		auto_exec = True

		self.horizontalSlider.setValue(0)

		midia_atual = self.listWidget.currentItem().text()
		self.att_reproducao()


	def alterar_volume(self):
		global comando
		global volume
		volume = int(self.horizontalSlider_2.value())
		print('volume: ',volume)
		comando = 'volume'
		self.label_4.setText(str(volume))


	def att_reproducao(self):
		global midia_atual
		self.lineEdit_2.setText(str(midia_atual))

	def att_duracao(self):
		global duracao_total
		global tipo_midia
		global tempo_atual

		global tempo_agora
		global duracao
		global tipo_midia

		self.label_8.setText(str(tempo_atual))
		self.label_9.setText(str(duracao_total))

		if tipo_midia == 'stream':
			self.horizontalSlider.hide()
			self.label_8.hide()
			self.label_9.hide()
		else:
			self.horizontalSlider.show()
			self.label_8.show()
			self.label_9.show()

		#self.att_slide_tempo()
		
		

	def alterar_tempo_midia(self):
		global comando
		global duracao
		global novo_tempo

		posicao = int(self.horizontalSlider.value())
		#print(posicao)

		novo_tempo = round((posicao * duracao /100), 3)
		print('novo tempo: ',novo_tempo)
		if novo_tempo > 0:
			comando = 'definir_tempo'




	def abrir_arquivos(self):
		#global pl
		global arquivo
		global pesquisa

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file, _ = QFileDialog.getOpenFileName(self,"Abrir arquivo m3u ...", "","M3u Files (*.m3u *.m3u8)", options=options)
		if file:
			print('arquivo: ',file)

			try:
				extrair_links(file)
				self.limpar_lista()
				self.carregar_lista()
				#comando == 'fechar'

				self.lineEdit_3.setText(str(file))

				pesquisa = False

			except Exception as e:
				print('[!] Erro - Houve um erro ao tentar abrir o arquivo.')


class Info_dev(QMainWindow):

	def __init__(self):
		super().__init__()
		self.ui = None
		self.load_ui()
		self.load_signals()
		
		self.setWindowTitle('m3uPlayer_dev - Teste')
		

	def load_ui(self):
		self.ui = loadUi(resource_path('m3u_dev.ui'),self)
	def load_signals(self):
		pass



#app = QApplication(sys.argv)
#a_window = Aplicacao()
sys.exit(appExec())


'''
b = threading.Thread(target=Aplicacao)
b.start()
'''


'''
media.add_option('start-time=600.00') - usar para modificar tamanho da janela
'''