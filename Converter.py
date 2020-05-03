from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os 
import zipfile
from shutil import make_archive
from pathlib import Path

dataSave = open("Program Source/Data.txt", "r")
saveRead = dataSave.readlines()
dataSave.close()

if 'True' in saveRead[0]:
	AskAgain = True
else:
	AskAgain = False
	

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
modFiles = list(askopenfilenames()) # show an "Open" dialog box and return the path to the selected file
print(str(modFiles))

for mods in range(0, len(modFiles)):

	if modFiles[mods][-4:] != '.ftl':
		if modFiles[mods][-4:] == '.zip':
			print('Not an FTL mod. Zip files are not accepted')
		else:
			print('Not an FTL mod.')
		continue

	for file in os.walk("Mod Source"):
		for x in range(0, len(file[2])):
			os.remove(file[0]+'/'+file[2][x])
	
	with zipfile.ZipFile(modFiles[mods], 'r') as zip_ref:
	    zip_ref.extractall('Mod Source')
		
	for x in range(1, modFiles[mods].count('/')):
		modFiles[mods] = modFiles[mods][:modFiles[mods].index('/')] + modFiles[mods][modFiles[mods].index('/')+1:]
	
	modname = modFiles[mods][modFiles[mods].index('/')+1:-4]
	for y in range(0, modname.count(' ')):
		modname = modname[:modname.index(' ')] + '_' + modname[modname.index(' ')+1:]
		
	print('converting ' + str(modname))
		
	blueprintsData = []
		
	if os.path.exists("Mod Source/data/blueprints.xml.append") is True:
		xml = open("Mod Source/data/blueprints.xml.append", "r")
		blueprintsData += xml.readlines()
		xml.close()
		
	if os.path.exists("Mod Source/data/dlcBlueprints.xml.append") is True:
		xml = open("Mod Source/data/dlcBlueprints.xml.append", "r")
		blueprintsData += xml.readlines()
		xml.close()
		
	if os.path.exists("Mod Source/data/dlcBlueprintsOverwrite.xml.append") is True:
		xml = open("Mod Source/data/dlcBlueprintsOverwrite.xml.append", "r")
		blueprintsData += xml.readlines()
		xml.close()
	
	
	playerShipOrder = ['PLAYER_SHIP_HARD', 'PLAYER_SHIP_CIRCLE', 'PLAYER_SHIP_FED', 'PLAYER_SHIP_ENERGY', 'PLAYER_SHIP_MANTIS', 'PLAYER_SHIP_JELLY', 'PLAYER_SHIP_ROCK', 'PLAYER_SHIP_STEALTH', 'PLAYER_SHIP_CRYSTAL', 'PLAYER_SHIP_ANAEROBIC', 'PLAYER_SHIP_HARD_2', 'PLAYER_SHIP_CIRCLE_2', 'PLAYER_SHIP_FED_2', 'PLAYER_SHIP_ENERGY_2', 'PLAYER_SHIP_MANTIS_2', 'PLAYER_SHIP_JELLY_2', 'PLAYER_SHIP_ROCK_2', 'PLAYER_SHIP_STEALTH_2', 'PLAYER_SHIP_CRYSTAL_2', 'PLAYER_SHIP_ANAEROBIC_2', 'PLAYER_SHIP_HARD_3', 'PLAYER_SHIP_CIRCLE_3', 'PLAYER_SHIP_FED_3', 'PLAYER_SHIP_ENERGY_3', 'PLAYER_SHIP_MANTIS_3', 'PLAYER_SHIP_JELLY_3', 'PLAYER_SHIP_ROCK_3', 'PLAYER_SHIP_STEALTH_3']
	
	#analysis
	
	modPlayerShips = []
	modPlayerShipNames = []
	modBasePlayerShipNames = []
	#nameCheck = False
	
	for lines in range(0, len(blueprintsData)):
		if '<shipBlueprint name="' in blueprintsData[lines]:
			for x in range(0, len(playerShipOrder)):
				if '"' + playerShipOrder[x] + '"' in blueprintsData[lines]:
					modPlayerShips.append(lines)
					modPlayerShipNames.append(playerShipOrder[x])
		
	for x in range(0, len(modPlayerShipNames)):
		modPlayerShipNames[x] = (modname.upper() + '_MOD_HYPER_' + modPlayerShipNames[x].upper()).upper()
		if x // 10 == 0:
			modBasePlayerShipNames.append(modPlayerShipNames[x])
	
	
	#Implementation
	
	for ships in range(0, len(modPlayerShips)):
		if '<shipBlueprint name="' in blueprintsData[modPlayerShips[ships]]:
			for x in range(0, len(playerShipOrder)):
				if '"' + playerShipOrder[x] + '"' in blueprintsData[modPlayerShips[ships]]:
					blueprintsData[modPlayerShips[ships]] = blueprintsData[modPlayerShips[ships]][:blueprintsData[modPlayerShips[ships]].index(playerShipOrder[x])] + modPlayerShipNames[ships] + blueprintsData[modPlayerShips[ships]][blueprintsData[modPlayerShips[ships]].index(playerShipOrder[x])+len(playerShipOrder[x]):]
		
	xml = open("Mod Source/data/blueprints.xml.append", "w")
	for lines in blueprintsData:
		xml.writelines(lines)
	xml.close()	
	
	if AskAgain is True:
	
		HackingNerf = input('Include Hacking Drone Nerf (explodes on disabling) (type y/n)\n').lower()
		if HackingNerf == ('y' or 'yes'):
			HackingNerf = True
		elif HackingNerf == ('n' or 'no'):
			HackingNerf = False
		else:
			HackingNerf = False
			print('Input accepted as a no')
		
		AskAgain = input('Ask again? (type y/n)\n').lower()
		print(AskAgain)
		if AskAgain == ('y' or 'yes'):
			print('check1')
			AskAgain = True
		elif AskAgain == ('n' or 'no'):
			print('check2')
			AskAgain = False
		else:
			print('check3')
			AskAgain = False
			print('Input accepted as a no')
		print(AskAgain)
	else:
		HackingNerf = 'True' in saveRead[1]
	
	xml = open("Mod Source/data/hyperspace.xml.append", "w")
	xml.writelines('<ships>\n')
	for x in range(0, len(modBasePlayerShipNames)):
		if modBasePlayerShipNames[x] + '_2' in modPlayerShipNames:
			typeB = True
		else:
			typeB = False
		
		if modBasePlayerShipNames[x] + '_3' in modPlayerShipNames:
			typeC = True
		else:
			typeC = False
		
	xml.writelines('\t<ship name="' + modBasePlayerShipNames[x] + '" b="' + str(typeB).lower() + '" c="' + str(typeC).lower() + '"/>\n')
	xml.writelines('</ships>\n\n')
	xml.writelines('<titleScreen enabled="false"/>\n')
	xml.writelines('<console enabled="false"/>\n')
	xml.writelines('<hackingDroneFix enabled="'+str(HackingNerf).lower()+'"/>\n')
	xml.close()
	
	dataSave = open("Program Source/Data.txt", "w")
	dataSave.writelines(str(AskAgain) + '\n')
	dataSave.writelines(str(HackingNerf) + '\n')
	dataSave.close()
	
	make_archive('Hyperspace ' + modname, 'zip', "Mod Source")
			
	print("Archived")
			
	if os.path.exists('Hyperspace ' + modname+'.ftl') is True:
		os.remove('Hyperspace ' + modname+'.ftl')
		print("Existing Archive Removed")
			
	p = Path('Hyperspace ' + modname+'.zip')
	p.rename(p.with_suffix('.ftl'))
	print("Renamed")
			
print("Done!")

input('Press Enter to Exit')