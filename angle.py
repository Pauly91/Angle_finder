#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Babu
#
# Created:     02/09/2012
# Copyright:   (c) Babu 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cv2
import cv
import numpy as np
import time
import math

class core_con2():
	def __init__(self):
		cv2.namedWindow("image1",1)
		cv2.namedWindow("image2",1)
		self.vid= cv2.VideoCapture(0)
		val, self.im = self.vid.read()
		self.im1= cv.fromarray(self.im)
		self.im2= cv.fromarray(self.im)
		self.s=self.im.shape
		self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
		print "h=",self.s[0],"w=",self.s[1]

	def line_pro(self):
		val,im = self.vid.read()
		if val==True:
			gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			edges = cv2.Canny(gray,80,120)
			cv2.imshow("image2",edges)
			cv2.waitKey(5)
			storage = cv.CreateMemStorage(0)
			lines = cv.HoughLines2(cv.fromarray(edges), storage, cv.CV_HOUGH_STANDARD, 1, math.pi / 180, 120, 0,10)
			for (rho, theta) in lines:
				self.pro(rho,theta,lines,im)
				a = math.cos(theta)
				b = math.sin(theta)
				x0 = a * rho
				y0 = b * rho
				pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
				pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
				cv.Line(cv.fromarray(im), pt1, pt2, cv.RGB(255, 0, 0), 3, 8)
			cv2.imshow("image1",im)
			cv2.waitKey(5)
			#lines = cv.HoughLines2(cv.fromarray(edges), storage, cv.CV_HOUGH_PROBABILISTIC, 1,math.pi / 180,val, 50, 10)
			#for lin in lines:
			#	print "lin=",lin
			#	theta=math.atan2((lin[1][1]-lin[0][1]),(lin[1][0]-lin[0][0]))
			#	if math.sin(theta)!=0:
			#		m=-(math.cos(theta)/math.sin(theta))
			#	c=lin[0][1]-(m*lin[0][0])
			#	self.pro(lines,m,c,lin,im)
			#	d=self.dist(lin)
			#	print "d=",d
			#	cv.Line(cv.fromarray(im), lin[0], lin[1], cv.CV_RGB(255, 0, 0), 3, 8)
			#	#print "lin[0]=",lin[0],"lin[1]=",lin[1]
			cv2.imshow("image1",im)
			cv2.waitKey(5)

	def pro(self,rho,theta,lines,im):
		for (r,t) in lines:
			if math.sin(theta)!=0:
				m1=-(math.cos(theta)/math.sin(theta))
				c1=rho/math.sin(theta)
			else:
				m1=0;
				c1=0;
			if math.sin(t)!=0:
				m2=-(math.cos(t)/math.sin(t))
				c2=r/math.sin(t)
			else:
				m2=0;
				c2=0;
			#a1x+b1y=c1
			#a2x+b2y=c2
			#-m1x+y=c1
			#-m2x+y=c2
			if m1>=m2:
				angle=int((math.atan2((m1-m2),(1+m1*m2))*180)/math.pi)
			else:
				angle=int((math.atan2((m2-m1),(1+m1*m2))*180)/math.pi)
			if (m2-m1)!=0:
				x = (c1-c2)/(m2-m1)
				y = (-m1*c2+m2*c1)/(m2-m1)
			else:
				x=0
				y=0
			if -10000 < int(x) < 10000:
				if-10000 < int(y) < 10000:
					if angle>5:
						cv2.circle(im,(int((x)),int((y))),40,(255,0,0),2,1)
						cv.PutText(cv.fromarray(im),str(angle),(int(x),int(y)),self.font, (0,255,0))




def main():
	a=core_con2()
	while True:
		a.line_pro()
	return 0

if __name__ == '__main__':
	main()

