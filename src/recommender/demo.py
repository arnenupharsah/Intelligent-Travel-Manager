import web
from web import form
import sys
import os
import numpy as np
import pandas as pd
import pickle as pkl
import model
from fastkml import kml, styles
from shapely.geometry import Point

### Url mappings
urls = (
	'/', 'Index'
)

### Templates
render = web.template.render('templates', base='base')
class Index:

	inputform = form.Form(
	form.Textbox('startPOI'),
	form.Textbox('length'),
	form.Button('recommendBtn')
	)

	

	def GET(self):
		inputform = self.inputform()
		return render.demo(inputform)

	def POST(self):
		i = web.input()
		startPOI = int(i.startPOI)
		length=int(i.length)
		inputform = self.inputform()
		fmodel = 'model-Melb.pkl'  # path of the trained model file
		model = pkl.load(open(fmodel, 'rb'))['MODEL']
		recommendations = model.predict(startPOI,length) # recommendations is list of 10 trajectories
		#result = "\n"
		#for i in range(len(recommendations)):
			#result += "Top "+str(i+1)+" recommendation: "+str(list(recommendations[0]))+"\n"

		data=pd.read_csv("./static/dataset/poi-Melb-all.csv")
		list1=(recommendations[0])
		list2=(recommendations[1])
		list3=(recommendations[2])
		poiNm1=[]
		poiTheme1=[]
		for i in range(len(list1)):
    			poiNm1.append(data.poiName[list1[i]])
    			poiTheme1.append(data.poiTheme[list1[i]])
		poiNm2=[]
		poiTheme2=[]
		for i in range(len(list2)):
			poiNm2.append(data.poiName[list2[i]])
			poiTheme2.append(data.poiTheme[list2[i]])
		poiNm3=[]
		poiTheme3=[]
		for i in range(len(list3)):
			poiNm3.append(data.poiName[list3[i]])
			poiTheme3.append(data.poiTheme[list3[i]])
		list1_df=data[data['poiID'].isin(list1)]
		list2_df=data[data['poiID'].isin(list2)]
		list3_df=data[data['poiID'].isin(list3)]
		generate_kml('./static/kml/poi1.kml',list1_df)
		generate_kml('./static/kml/poi2.kml',list2_df)
		generate_kml('./static/kml/poi3.kml',list3_df)

		return render.demo2(startPOI, length, inputform, list(recommendations[0]), list(recommendations[1]), list(recommendations[1]), poiNm1,poiNm2,poiNm3,poiTheme1,poiTheme2,poiTheme3)

def generate_kml(fname, poi_df):
	k = kml.KML()
	ns = '{http://www.opengis.net/kml/2.2}'
	styid = 'style1'
	# colors in KML: aabbggrr, aa=00 is fully transparent
	sty = styles.Style(id=styid, styles=[styles.LineStyle(color='9f0000ff', width=2)]) # transparent red
	doc = kml.Document(ns, '1', 'POIs', 'POIs visualization', styles=[sty])
	k.append(doc)

	# Placemark for POIs
	for ix in poi_df.index:
		name = poi_df.loc[ix, 'poiName']
		cat  = poi_df.loc[ix, 'poiTheme']
		lat  = poi_df.loc[ix, 'poiLat']
		lon  = poi_df.loc[ix, 'poiLon']
		url  = poi_df.loc[ix, 'poiURL']
		ext_data = kml.ExtendedData(ns,elements=[kml.Data(name='video', value="![CDATA[<iframe name='Framename' width='480' height='360' src='%s' frameborder='0'></iframe><br><br>]]" %(url))])

		desc = ''.join(['POI Name: ', name, '<br/>Category: ', cat, '<br/>Coordinates: (%f, %f)' % (lat, lon), '<br/>URL: ', url])
		pm = kml.Placemark(ns, str(ix), name, desc, styleUrl='#' + styid, extended_data=ext_data)
		pm.geometry = Point(lon, lat)
		doc.append(pm)



	# save to file
	kmlstr = k.to_string(prettyprint=True)
	with open(fname, 'w') as f:
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write(kmlstr)
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
