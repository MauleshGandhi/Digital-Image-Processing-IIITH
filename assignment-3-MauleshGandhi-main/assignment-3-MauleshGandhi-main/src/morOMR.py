import cv2 as cv
import numpy as np
# do not import any other library
# Note: this is just a boiler plate
# feel free to make changes in the structure
# however, input/output should essentially be the same.
# IMPORTANT: When you use this, save it in the path src/morOMR.py - if you don't
# your test will fail automatically.

def erode(omr_sheet,filter):
  # Padding image
    maxVal = np.max(filter.shape)
    omr_sheet3 = np.zeros((omr_sheet.shape[0] + 2 * maxVal, omr_sheet.shape[1] + 2 * maxVal))
    omr_sheet3[maxVal:omr_sheet3.shape[0] - maxVal, maxVal:omr_sheet3.shape[1] - maxVal] = omr_sheet
    omr_sheet3 = omr_sheet3.astype('float')
    filter = filter.astype('float')
    omr_sheet2 = omr_sheet3.copy()
    # Convolution
    for r in range(filter.shape[0], omr_sheet2.shape[0] - filter.shape[0] + 1):
        for c in range(filter.shape[1], omr_sheet2.shape[1] - filter.shape[1] + 1):
            omr_sheet2[r][c] = np.min(omr_sheet3[r - int(filter.shape[0] / 2):r - int(filter.shape[0] / 2) + filter.shape[0], c - int(filter.shape[1] / 2):c - int(filter.shape[1] / 2) + filter.shape[1]]*filter)
    # Remove padded region and return image
    return omr_sheet2[maxVal:omr_sheet2.shape[0] - maxVal, maxVal:omr_sheet2.shape[1] - maxVal]

def dilate(omr_sheet, filter):
  # Padding image
    maxVal = np.max(filter.shape)
    omr_sheet3 = np.zeros((omr_sheet.shape[0] + 2 * maxVal, omr_sheet.shape[1] + 2 * maxVal))
    omr_sheet3[maxVal:omr_sheet3.shape[0] - maxVal, maxVal:omr_sheet3.shape[1] - maxVal] = omr_sheet
    omr_sheet3 = omr_sheet3.astype('float')
    filter = filter.astype('float')
    omr_sheet2 = omr_sheet3.copy()
    # Convolution
    for r in range(filter.shape[0], omr_sheet2.shape[0] - filter.shape[0] + 1):
        for c in range(filter.shape[1], omr_sheet2.shape[1] - filter.shape[1] + 1):
            omr_sheet2[r][c] = np.max(omr_sheet3[r - int(filter.shape[0] / 2):r - int(filter.shape[0] / 2) + filter.shape[0], c - int(filter.shape[1] / 2):c - int(filter.shape[1] / 2) + filter.shape[1]]*filter)
    # Remove padded region and return image
    return omr_sheet2[maxVal:omr_sheet2.shape[0] - maxVal, maxVal:omr_sheet2.shape[1] - maxVal]

def getAnswers(omr_sheet)->list:
    c = ([236,814], [573,814], [910,814])
    w_diff = 42
    h_diff = 42.5
    r = 12
    area = np.pi*r*r
    approx_area = int(area*0.7)
    rows = 15
    columns = 4
    parts = 3
    answers = np.zeros([rows*parts,columns])
    omr_sheet_copy = np.copy(omr_sheet)

    # applying thresholding
    omr_sheet_copy[omr_sheet <= 200] = 0
    omr_sheet_copy[omr_sheet > 200] = 1

    # taking inverse of omr_sheet so that white will be filled in darkened circles
    omr_sheet_copy = np.logical_not(omr_sheet_copy).astype(int)

    # applying closing to fill gaps in manually filled answer sheets
    dilated = dilate(omr_sheet_copy, np.ones([5,5]))
    eroded = erode(dilated, np.ones([5,5]))

    const = 0
    for i in range(parts):
            centre_x,centre_y = c[i]
            for j in range(rows):
                centre_x = c[i][0]
                for k in range(columns):
                    # check sum of area within circle of radius r
                    temp = omr_sheet_copy[centre_y-r-1:centre_y+r,centre_x-r:centre_x+r+1]
                    if np.sum(temp) >= approx_area:
                        answers[(const+j),k] = 1
                    centre_x += w_diff
                centre_y = c[i][1] + int(np.rint(h_diff*(j+1)))
            const += 15
    for i in range(45):
        k = np.where(answers[i]==1)
        if k[0].size == 0:
            print("-1")
        elif k[0]==0:
            print("A")
        elif (k[0]==1):
            print("B")
        elif k[0]==2:
            print("C")
        elif k[0]==3:
            print("D")
    return answers

  # do all your processing here.
  # return answers of particular omr sheet here
  
  
pass

if __name__ == "__main__":
  
  # Read the number of test cases
  # input() returns str by default, i.e. 1000 is read as '1000'.
  # .strip() used here to strip of the trailing `\n` character
      
  T = int(input().strip())
                           
  
  for i in range(T):
    
    fileName = input().strip() # read path to image
    omr_sheet = cv.imread(fileName)
    H,W = omr_sheet.shape[:2]
    omr_sheet2 = np.zeros((H,W), np.uint8)
    for i in range(H):
        for j in range(W):
            omr_sheet2[i,j] = np.clip(0.07 * omr_sheet[i,j,0]  + 0.72 * omr_sheet[i,j,1] + 0.21 * omr_sheet[i,j,2], 0, 255)

    
    answers = getAnswers(omr_sheet2) # fetch your answer
    # for answer in answers: # assuming answers is a list
    #   print(answer)  # print() function automatically appends the `\n`