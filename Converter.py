#!/usr/bin/env python
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os 
import zipfile
from shutil import make_archive
from pathlib import Path
import xml.etree.ElementTree as ET
	
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
		
	blueprintFiles = []
		
	if os.path.exists("Mod Source/data/blueprints.xml.append") is True:
		blueprintFiles.append("Mod Source/data/blueprints.xml.append")
		
	if os.path.exists("Mod Source/data/dlcBlueprints.xml.append") is True:
		blueprintFiles.append("Mod Source/data/dlcBlueprints.xml.append")
		
	if os.path.exists("Mod Source/data/dlcBlueprintsOverwrite.xml.append") is True:
		blueprintFiles.append("Mod Source/data/dlcBlueprintsOverwrite.xml.append")
	
	
	playerShipOrder = ['PLAYER_SHIP_HARD', 'PLAYER_SHIP_CIRCLE', 'PLAYER_SHIP_FED', 'PLAYER_SHIP_ENERGY', 'PLAYER_SHIP_MANTIS', 'PLAYER_SHIP_JELLY', 'PLAYER_SHIP_ROCK', 'PLAYER_SHIP_STEALTH', 'PLAYER_SHIP_CRYSTAL', 'PLAYER_SHIP_ANAEROBIC', 'PLAYER_SHIP_HARD_2', 'PLAYER_SHIP_CIRCLE_2', 'PLAYER_SHIP_FED_2', 'PLAYER_SHIP_ENERGY_2', 'PLAYER_SHIP_MANTIS_2', 'PLAYER_SHIP_JELLY_2', 'PLAYER_SHIP_ROCK_2', 'PLAYER_SHIP_STEALTH_2', 'PLAYER_SHIP_CRYSTAL_2', 'PLAYER_SHIP_ANAEROBIC_2', 'PLAYER_SHIP_HARD_3', 'PLAYER_SHIP_CIRCLE_3', 'PLAYER_SHIP_FED_3', 'PLAYER_SHIP_ENERGY_3', 'PLAYER_SHIP_MANTIS_3', 'PLAYER_SHIP_JELLY_3', 'PLAYER_SHIP_ROCK_3', 'PLAYER_SHIP_STEALTH_3']
	
	#analysis
	
	modPlayerShips = []
	modPlayerShipNames = []
	modBasePlayerShipNames = []
	#nameCheck = False
	
	for file in blueprintFiles:
	
		xml = open(file, "r")
		code = xml.readlines()
		xml.close()
		
		if '<FTL>' not in code and '</FTL>' not in code:
		
			declaration = ''
		
			for x in range(0, len(code)):
				if '<?xml' in code[x]:
					declaration = code[x]
					del code[x]
					break
		
			code.insert(0, '<FTL>')
			code.insert(0, declaration)
			code.append('</FTL>')
			
			xml = open(file, "w")
			code = xml.writelines(code)
			xml.close()
		
		tree = ET.parse(file)
		root = tree.getroot()
		
		for child in root:
			if child.tag == 'shipBlueprint':
				for child2 in child:
					if child2.tag == 'name':
						modBasePlayerShipNames.append(child.attrib['name'] + '_' + child2.text)
						child.set('name', modBasePlayerShipNames[-1])
						break
						
		tree.write(file)
	
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
	xml.close()
	
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