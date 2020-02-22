import glob
import pandas as pd
import urllib.request
from fpdf import FPDF # This library is needed to convert the result images to a pdf
from resizeimage import resizeimage
from PIL import Image
import re

df = pd.read_csv('df')

def extra_analysis():
    print('Would you like to do an extra analysis of the billionaires list and check who occupies a specific position?')
    global extra_analysis_answer
    extra_analysis_answer = input('Write "Y" for Yes and "N" for No: ').upper().strip()
    global num_position
    if extra_analysis_answer == 'Y':
        num_position = int(input("From 0 to 2207, choose a number to see who's billionaire occupies that position: "))
        urllib.request.urlretrieve(df['image'][num_position], f"../data/results/z{df['name'][num_position]}.jpg")
    elif extra_analysis_answer != 'N':
        while not extra_analysis_answer in ['Y', 'N']:
            print('Not a valid answer, try again!')
            extra_analysis_answer = input('Write "Y" for Yes and "N" for No: ').upper().strip()
        num_position = int(input("From 0 to 2207, choose a number to see who's billionaire occupies that position: "))
        urllib.request.urlretrieve(df['image'][num_position], f"../data/results/z{df['name'][num_position]}.jpg")

def header(self):
    # Code to set a logo
    self.image('../package1/ironhack.jpg', 10, 8, 33)
    self.set_font('Arial', 'B', 15)

    # Code to add some introductional titles and subtitles
    self.ln(10)
    self.cell(100)
    self.cell(0, 5, 'Ironhack Madrid', ln=1)
    self.cell(100)
    self.cell(0, 5, 'Data Analytics Part-time 2019', ln=1)
    self.cell(100)
    self.cell(0, 5, 'Pipeline Project: Billionaires 2018', ln=1)

    # Some lines of text
    self.ln(15)
    self.set_font('Arial', 'B', 12)
    self.cell(0, 5, 'This document contains your desired results obtained from the most billionaires of 2018!', ln=1)
    self.ln(20)

def footer(self):
    self.set_y(265)

    self.set_font('Arial', 'I', 8)

    # Add a page number
    page = 'Page ' + str(self.page_no())
    self.cell(0, 10, page, 0, 0, 'C')

def add_pdf(type_of_analysis):
    legend = ['Total number of billionaires per country. (Top 30)',
              'Top 15 fields of work most responsible for the wealth of their billionaires.',
              'Top 15 of countries which hold more billions of dollars by its billionaires.',
              'Percentage of billions of dollars distributed by gender.',
              'Ratio of billionaires with and without studies.']

    resume_analysis = ['the US dominated the list with nearly 600 billionaires followed by China with over 350. Last positions were occupied by Denmark and Ireland',
                       'the two most profitable work fields are technology and fashion & retail industry. Last positions were occupied by Telecom and Construction.',
                       'the US is the country that holds more billions with a record of over 3000 billions followed by china responsible for over 1000 billion.',
                       'about 90% of billionaire fortunes belong to men.',
                       "about 70% of the billionaires don't have university studies."]
    pdf = FPDF()
    count = 1
    for image in glob.glob('../data/results/results*.jpg'):
        pdf.add_page()
        header(pdf)
        pdf.image(image, x=10, y=60, w=180)
        pdf.set_font('Arial', size=8)
        pdf.ln(170)  # move 170 down
        if type_of_analysis < 6 and re.match('../data/results/results[0-9].jpg', image):
            pdf.cell(200, 10, txt='', ln=1)
            pdf.cell(ln=0, h=5.0, align='L', w=0, txt=f"Figure {count}: {legend[type_of_analysis-1]}", border=0)
            pdf.ln(5)
            pdf.cell(ln=0, h=5.0, align='L', w=0, txt=f"In this graphic, {resume_analysis[type_of_analysis - 1]}", border=0)
        elif type_of_analysis == 6 and re.match("../data/results/results[0-9].jpg", image):
            pdf.cell(200, 10, txt='', ln=1)
            pdf.cell(ln=0, h=5.0, align='L', w=0, txt=f"Figure {count}: {legend[count-1]}", border=0)
            pdf.ln(5)
            pdf.cell(ln=0, h=5.0, align='L', w=0, txt=f"In this graphic, {resume_analysis[count-1]}", border=0)
        else:
            continue
        footer(pdf)
        count += 1
    for i in glob.glob('../data/results/z*.jpg'):
        pdf.add_page()
        header(pdf)
        pdf.image(i, x=10, y=60, w=180)
        pdf.set_font('Arial', size=8)
        pdf.ln(170)  # move 170 down
        with open(i, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [200, 100])
                cover.save('1image.jpg', image.format)
        pdf.cell(200, 10,
                     txt=f"Figure {count}: In {num_position}.º place is {re.sub('_', ' ', df['name'][num_position])} who had a fortune of {df['worth(BUSD)'][num_position]} billions of dollars in 2018.",
                     ln=1)
            #pdf.write(500,f"Figure {count}: In {num_position}.º place is {re.sub('_', ' ', df['name'][num_position])} who had a fortune of {df['worth(BUSD)'][num_position]} billions of dollars in 2018.")
        footer(pdf)
    pdf.output('../data/results/results.pdf')

