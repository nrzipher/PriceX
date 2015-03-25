from flask import Flask
from flask import request
from PIL import Image
import StringIO
import base64
app = Flask(__name__)

def match(img,img2,w,h):
    k=0
    for x in range(w):
        for y in range(h):
            
            if abs(img.getpixel((x,y))-img2.getpixel((x,y)))>20:
                k=k+1
    if k>w*h*.05:
        return 0
    else:
        return 1
            
def OCR(img,img2,w,h,imgdata):
    #img.save("./static/target.png")
    result=-1
    for x in range(10):
        print x
        col=int(imgdata[x*2])-1
        row=int(imgdata[x*2+1])-1
        #img2.crop((row*w,col*h,row*w+w,col*h+h)).save("./static/"+str(x)+'.png')
        if match(img2.crop((row*w,col*h,row*w+w,col*h+h)),img,w,h):
            result = x
    return result

@app.route("/")
def index():
	return """API page <br>
    post url=http://10.8.92.9:5000/meituanOCR?vender=meituan&type=a&width=15&height=30&posx=15&posy=0 <br>
    parameters:vender type('a' for now) width height posx posy <br>
    
    Request Body:Image file as a byte array in base64
    """

    

@app.route("/meituanOCR",methods = ['POST'])
def meituanOCR():

	imgvender = str(request.args.get('vender'))
	imgtype = str(request.args.get('type'))
	imgw = int(request.args.get('width'))
	imgh = int(request.args.get('height'))
	posx = int(request.args.get('posx'))
	posy = int(request.args.get('posy'))
	#print dir(request)
	#print dir(request.data)
	
	f = request.data
	img = Image.open(StringIO.StringIO(base64.decodestring(f)))
	
	img2 = Image.open("./static/"+imgvender+imgtype+str(imgw)+str(imgh)+".png")
	imgdata = open('./static/'+imgvender+imgtype+str(imgw)+str(imgh)+".txt")
	
	imgdata = imgdata.readline().split(',')
	
	#img.crop((posx,posy,posx+imgw,posy+imgh)).save('out.png')
        
	s=str(OCR(img.crop((posx,posy,posx+imgw,posy+imgh)),img2,imgw,imgh,imgdata))
	
	return s 



if __name__=='__main__':
	app.run()#host='0.0.0.0')
