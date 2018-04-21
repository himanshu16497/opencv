#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results_2817.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()

def main(path):
    #read images
    ref_img=cv2.imread('square.png')
    img=cv2.imread(path)


    #convert to gray scale
    ref_gray=cv2.cvtColor(ref_img,cv2.COLOR_BGR2GRAY)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #convert to binary
    ret,ref_thresh=cv2.threshold(ref_gray,230,255,0)
    ret,thresh=cv2.threshold(gray,230,255,0)

    #find contours
    _,ref_contours,hirarchy=cv2.findContours(ref_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _,contours,hirarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    #other_reference_image
    if(len(ref_contours)>1):
        ref_contours=ref_contours[2]

    #centroids
    length = len(contours)
    centroids = []
    color_detection = []
    centroids1 = []
    centroids2 = []
    for cnt in range(1, length):
        M = cv2.moments(contours[cnt], True)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cent = (cx, cy)
        cent1 = (cx - 90, cy + 40)
        cent2 = (cx - 90, cy + 80)
        color_array = (cy, cx)
        color_detection.append(color_array)
        centroids.append(cent)
        centroids1.append(cent1)
        centroids2.append(cent2)

    #color and centroids printing
    colors=[]
    eff_length = (len(color_detection))
    for x in range(0, eff_length):
        array = img[color_detection[x]]
        print(array)
        if (array[0] == 0 and array[1] == 0):
            print('red color')
            cv2.putText(img, 'RED', centroids[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.putText(img, str(centroids[x]), centroids1[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            colors.append('red')
        if (array[2] == 0 and array[1] == 0):
            print('blue color')
            cv2.putText(img, 'BLUE', centroids[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.putText(img, str(centroids[x]), centroids1[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            colors.append('blue')
        if (array[0] == 0 and array[2] == 0):
            print('green color')
            cv2.putText(img, 'GREEN', centroids[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.putText(img, str(centroids[x]), centroids1[x], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            colors.append('green')

    #shape detection and printing
    # 1Finding vertices in input image
    vert_in_img=[]
    vert_in_ref=[]
    for i in contours:
        approx = cv2.approxPolyDP(i, 0.01 * cv2.arcLength(i, True), True)
        print len(approx)
        x = len(approx)
        vert_in_img.append(x)
    print ('a=', vert_in_img)

    # 2Finding vertices in sample image
    for i in ref_contours:
        approx = cv2.approxPolyDP(i, 0.01 * cv2.arcLength(i, True), True)
        print len(approx)
        x = len(approx)
        vert_in_ref.append(x)
    print ('b=', vert_in_ref)
     #detection
    #####################Detection of shape####################################
    shapes=[]
    m_count=0

    font = cv2.FONT_HERSHEY_SIMPLEX
    for m in vert_in_img:
        m_count += 1
        n_count = 0
        for n in vert_in_ref:
            n_count += 1
            if m == 4 & n == 4:
                #ret = cv2.matchShapes(contours[m_count], ref_contours[n_count], 1, 0.0)
                # Ret values have been hard coded

                if ret > 0.3:
                    print "Trapezium"
                    shapes.append("Trapezium")
                    #cv2.putText(img, "Trapezium", centroids2[count], font, 0.5, (0, 0, 255), 2)


                else:
                    print "Rhombus"
                    shapes.append("Rhombus")
                    #cv2.putText(img, "Rhombus",centroids2[count] , font, 0.5, (0, 0, 255), 2)


            elif m == 3:  # Triangle has three edges/points
                print "Input image is a triangle"
                shapes.append("triangle")
                #cv2.putText(img, "Triangle", centroids2[count], font, 0.5, (0, 0, 255), 2)


            elif m == 5:  # Pentagon has five edges/points
                print "pentagon"
                shapes.append("pentagon")
                #cv2.putText(img, "Pentagon", centroids2[count], font, 0.5, (0, 0, 255), 2)

            elif m == 6:  # Hexagon has six points/edges
                print "hexagon"
                shapes.append("hexagon")
                #cv2.putText(img, "Hexagon", centroids2[count], font, 0.5, (0, 0, 255), 2)


            elif m == 7:
                print "Arrow"
                shapes.append("Arrow")
                #cv2.putText(img, "Arrow", centroids2[count], font, 0.5, (0, 0, 255), 2)

            elif m > 7:
                print "Circle"
                shapes.append("Circle")


                #cv2.putText(img, "Circle", centroids2[count], font, 0.5, (0, 255, 0), 2)
    print(shapes)
    for count in range(1,len(shapes)):
        cv2.putText(img,shapes[count],centroids2[count-1],font,1,(0, 0, 0),4)
        writecsv(colors[count-1], shapes[count],centroids[count-1])

    #printing images
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #saving output image
    cv2.imwrite(path[:-4]+'output'+'.png',img)

#####################################################################################################
    #Write your code here!!!
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":

    mypath = 'C:\\Users\\Himanshu\\Desktop\\Set 4\\Task 1\\Task1A\\2. Task_Description\\Test Images'
    #getting all files in the directory
    onlyfiles = [mypath+os.sep+f for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles :
        #Open the csv to write in append mod
        print(fp)
        filep = open('results_2817.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results_2817.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
