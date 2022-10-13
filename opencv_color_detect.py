#import numpy.core.multiarray
import numpy as np
#import cv2

import math
#import time
from PIL import Image
import decision_tree as DEC
import robot_movement as RM
import colorsys


import pandas as pd
import statistics

def process_image(raw_image):

		
		global jart
		global rec
		
		mat=np.float32(raw_image)
		
		for i in mat:
			for j in range(len(i)):
				hsv = colorsys.rgb_to_hsv(i[j][2]/255.,i[j][1]/255.,i[j][0]/255.)
				i[j] = hsv[0]*360
		#mat=np.float32(raw_image)
		THRESH_TXT = ["Green"]
		THRESH_LOW = [55, 0, 0]
		THRESH_HI = [175, 100, 100]




		#print(len(mat))
		print(mat[0])
		df=pd.DataFrame(mat[0])

		for i in range(1,len(mat)):
			ind=i*640
			df_new=pd.DataFrame(mat[i],index=[np.arange(ind,ind+640)])
			df=pd.concat([df,df_new])
		df_small=pd.DataFrame()

		def sel(i):

			ind=np.arange(i,i+64)
		# ind = np.arange(i + 100, i + 110)
			for j in range(0,30080,640):
				temporary=np.arange(j+640+i,j+704+i)
				ind=np.append(ind,temporary,axis=0)
			return ind
		r=0
		g=0
		b=0

		ran=[]
		i=0
		#307,200=480*640
		while i<277120:
			if (i % 640 == 0 and i != 0):
				i += 30080
			ten = df.iloc[sel(i)]

			r = ten[0].mean()

			df_new = pd.DataFrame({'H': [r]})
			df_small = pd.concat([df_small, df_new])
			i += 64

		df_small= df_small.set_index([np.arange(1,101)])


		print(df_small)
		border_distance=0
		border=[]
		utolsof=False
		area=0
		for i in range(len(df_small)):

			zold=0
			hsv=df_small.iloc[i].values

			if(hsv[0]>THRESH_LOW[0] and hsv[0]<THRESH_HI[0]):
				zold+=1
				if(utolsof==True):
					border.append(border_distance)
					utolsof=False
				border_distance=0
				area+=1
				zold=0
			else:
				utolsof=True
				border_distance+=1
				zold=0

			
		if(border!=[]):
			distance=statistics.mean(border)
		else:
			distance=0
		print(border)
		print(distance,'distance')
		print(area,'area')


		map=np.loadtxt('map.txt',dtype='int')
		cor=np.loadtxt('coordinates.txt',dtype='int')

		jart='uj'
		x=cor[0,0]
		y=cor[0,1]
	
		x += int(math.cos(math.radians(cor[1][0]))*1)
		y -= int(math.sin(math.radians(cor[1][0]))*1)
		

		if(abs(y)>=len(map)):
			print(map)
			map = np.vstack((map, np.zeros((1, len(map[0])))))
			print('###y')
			print(map)

		if(x>=len(map[0])):
			print(map)
			map = np.hstack( ( map, np.zeros((len(map),1)) ) )
			print('###x')
			print(map)

		print(x,y)
		print(map)
		if(area<15):
			DEC.decide('zold','szabad','forduljobb',jart)
			cor[1][0] += 90
			np.savetxt('coordinates.txt',cor,fmt='%d')


		elif(map[-y,x] == 0):
			DEC.decide('zold','szabad','kozep',jart)
			cor[1][1] =0
			cor[0][0] = x
			cor[0][1] = y
			map[y,x] = 1
			np.savetxt('coordinates.txt',cor,fmt='%d')
			np.savetxt('map.txt',map,fmt='%d')
		else:
			DEC.decide('zold','szabad','kozep','volt')
			cor[1][0] += 90
			cor[1][1] +=1
			np.savetxt('coordinates.txt',cor,fmt='%d')

		return()



