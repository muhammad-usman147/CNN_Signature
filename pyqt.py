import cv2
import os
import math as m
from pdf2image import convert_from_path
class ImageGenerator():
    def __init__(self,pdf):
        self.count=0
        self.p_c =0  #p_c  = pdf counter
        #to save pdf names by their pdf number i-e 1st_PDF_page1.jpg.2nd_PDF_page1.jpg so on
        self.pdf = pdf
        #pdf names pdf = ['1st','2nd','3rd','4th','5th','6th']


    def GetPdF(self,pdf_name):
        self.GeneratePictures(pdf_name) 
        #sending the names of the pdf
        self.p_c+=1
        #p_c = p_c + 1 is the number of pdf in the self.pdf list


    def GeneratePictures(self,pdf_name):
        ''' 
        Converting the pages of the pdfs into imagees
        '''
        pages = convert_from_path(pdf_name)
        print(pages)
        num=0
        x=self.pdf[self.p_c] #getting pdf name from self.pdf list 
        for i in pages:
            num+=1
            i.save('../DLP/signature/generated_pics/{}_PDF_page{}.jpg'.format(x,num),'JPEG')
            
    def GenerateSignatures(self):
        ''' 
        Croping the generated images of the pdf pages into 4 sections...
        top left, top right, bottom left, bottom right
        '''
        sig_dir='../DLP/signature/generated_pics/' #directory of the image
        for i in os.listdir(sig_dir):
            try:
                image = cv2.imread('../DLP/signature/generated_pics/'+i)
                x = image[:-150,:]     
                #removing the useless part of the images
                ''' 
                image[:-150,:] means that I am removing 150 pixs from below, to get the 
                images of signature in focus
                '''
                #croping the image from the bottom
                #To get the image in focus
                div=round(4//2)
                #4 represents the total no of croped images
                #to retreive the single images
                div_height =m.floor(x.shape[0]/div) 
                div_width = m.floor(x.shape[1]/div)
                #divding total by 2 because two images 
                #will be generated from top and two from bottom
                h=0 #iniital croping
                w=0 #initial croping
                width=div_width
                height=div_height
                for i in range(div):
                     #for row
                    for i in range(div):
                        croped = x[h:div_height,w:div_width]
                        '''
                        Croping the image from 
                        [ top left, top right
                          bottom left, bottom right
                        ] 
                        becasue 4 is given as 4 croped images are req from a picture
                        '''
                        print("{}:{},{}:{}".format(h,div_height,w,div_width))
                        w=div_width 
                        div_width+=width
                        # moving the next width value
                        #i-e moving from left to right 
                        if cv2.imwrite('../DLP/signature//SIG_DATA/signature{}.png'.format(self.count),croped):
                            # if Ture(saving the image)
                            print("image generated from page {} ".format(self.count))
                            self.count+=1
                    h = div_height
                    div_height+=height
                    div_width=width
                    # moving the next row value
                    # i-e moving from top to bottom
                    w=0
                    # shifting width value to it's initial position
                    print(str(i)+' converted')
            except Exception as e:
                print(e)
                #if ANY error occurs display here.... 
pdf = ['1st','2nd','3rd','4th','5th','6th']
obj = ImageGenerator(pdf)

for i in range(0,len(pdf)):
    pdf_name='../DLP/signature/'+pdf[i]+'PDF.pdf'
    obj.GetPdF(pdf_name)
obj.GenerateSignatures()
