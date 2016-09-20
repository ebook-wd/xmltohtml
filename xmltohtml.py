#!/usr/bin/env python

"""
Usage: Type at the command prompt

python xmltohtml.py -i <inputfile> -o <outputfile> 

inputfile     =  name of the input file. Must be a text file containing register number and date of birth seperated by comma .
outputfile    =  name of the output file. Must be a text file.
eg:
python xmltohtml.py -i foo.xml -o foo.html
"""

__author__      = "William Doyle A F"
__copyright__   = "Copyright 2016"
__license__ 	= "GNU GPLv3 (http://www.gnu.de/documents/gpl-3.0.en.html)"
__version__ 	= "1.5"

import re
import sys
import getopt
from bs4 import BeautifulSoup

soup = ''
tag = ''
indent = ''
fo = ''
next_indent = ''
next_font = ''
next_header = ''

#==============================================================================
PARA_INDENT = [252,253,254,255]
BLOCK_QUOTE = ['254','255'] 
unwanted_font = ['1','2','15']
HEADER = ['0','87','198','199','200','217']
LINE_SPACING = ''
CENTER = 5
CONTENT_PAGE_START = 8
CONTENT_PAGE_END = 8
INDEX = list(range(284,302))
H1 = '0'
H2 = '9'
H3 = '14' 
H4 = ''
SUPER_FONT = ['']
FOOTNOTES_FONT = ['']
#==============================================================================
BLOCK_LOWER = int(BLOCK_QUOTE[0])    
l = len(BLOCK_QUOTE)-1 
BLOCK_UPPER = int(BLOCK_QUOTE[l])          
                                                       
def header_match(header):
    for n in HEADER:
        if header == n:
            #print(header,n)
            return 0
def  font_match(font):
    for n in unwanted_font:
        if font == n:
            #print(font,n)
            return 0
def heading(line,font):
    text_line=''
    if font == H1:
        text_line = "<h1>"+line+"</h1>"+"\n"
        return text_line 
    elif font == H2 :
        text_line = "<h2>"+line+"</h2>"+"\n"
        return text_line             
    elif font == H3 :
        text_line = "<h3>"+line+"</h3>"+"\n"
        return text_line
    elif font == H4 :
        text_line = "<h4>"+line+"</h4>"+"\n"
        return text_line    
    else:
        return 'NULL'
def index_check(page_no):
    for i in INDEX:
        if i == page_no:
            return 0
def superscript(line,font, line_top, nextline_top ):
    # checks for super script and subscript
    text_line=''
    for n in SUPER_FONT:
        if n == font and nextline_top > line_top :
            text_line = "<sup><small>" + line + "</small></sup>"
            return text_line
        elif n == font and nextline_top < line_top :
            text_line = "<sub><small>" + line + "</small></sub>"
            return text_line
        else:
            return 'NULL'
def footnote(line,font):
    # checks for footnotes
    text_line = line
    for n in FOOTNOTES_FONT:
        if n == font:
            text_line = "\n"+"<small>" + line + "</small>" 
           
    return   text_line           
def paragraph_check(indent_next):
    para = 0
    for n in PARA_INDENT :
        if  n == indent_next :
            para = 1    
    return para                
def check_line_spacing(line_top, nextline_top)   :
    return nextline_top - line_top            
def main():
    Input_File_Name  = ''
	# Assigns the out put file name
    Output_File_Name = ''
    try:
      		opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["infile=","outfile="])
    except getopt.GetoptError:
      		print ('copytxt.py -i <inputfile> -o <outputfile> ')
      		sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            #print 'copytxt.py -i <inputfile> -o <outputfile> -b <begintext> -e <endtext>'
            usage()
            sys.exit()
        elif opt in ("-i", "--infile"):
            Input_File_Name  = arg
        elif opt in ("-o", "--outfile"):
            Output_File_Name = arg     

    try:
        fin = open(Input_File_Name, 'r')
    except IOError:
        print ("There was an error in opening", Input_File_Name )
        sys.exit()
   #if os.path.exists(Output_File_Name):
	  #print "The output file "+Output_File_Name+ " alredy exist. Try another name for outputfile"
	  #sys.exit()    

    fo = open(Output_File_Name,'w') 
    
    fo.write("<!DOCTYPE html>"+"\n")
    fo.write('''<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">'''+"\n")
    fo.write("<head>"+"\n")
    fo.write("<title>Thomas Young</title>"+ "\n")
    fo.write('''<style type="text/css">'''+ "\n")
    fo.write('''h1 {
                    text-align: center;
                    }

                h2 {
                    text-align: center;
                    }''')
    fo.write(''' p {
                    padding: 0cm 0cm 0cm 0cm;
                    text-indent: 45px;
                    text-align:justify;
                    }
                    ''')
    fo.write('''blockquote { 
                            display: block;
                            margin-top: 1em;
                            margin-bottom: 1em;
                            margin-left: 40px;
                            margin-right: 40px;
                            text-align:justify;
                    }''')
    fo.write("</style>"+"\n")
    fo.write("</head>"+"\n")
    fo.write('''<body bgcolor="#FFFFFF" vlink="blue" link="blue">'''+"\n")
     
    soup = BeautifulSoup(fin,'xml')    
    
    outline = soup.outline.find_all('item')
    fo.write('''<a name="outline"></a><h1>Document Outline</h1><ul>''')
    #print(outline)
    for t in outline:
        s =BeautifulSoup(str(t),"lxml")
        ol = s.item.get('page')
        #print(ol) 
        item = s.item.contents
        #print(item[0])
        fo.write(''' <li><a href=" ''' +Output_File_Name+"#"+ol+"\">"+item[0]+'''</a></li>''')
    fo.write("</ul>")
        
    page = soup.find_all('page')
    page_no = 0
    for p in page:
        page_no = page_no +1
        quote = 0
        center = 0
        
        if index_check(page_no) == 0:
            #..........Skips the index pages...............
            continue
        
        fo.write("<p>") 
        
        soup =BeautifulSoup(str(p),'xml')
        pgref = soup.find('page')
        pg_tag = pgref.get('number')
        fo.write("<a name="+pg_tag+"></a>"+"\n")
        
        image = soup.find_all('image')
        #print(image)
        for i in image:
            s = BeautifulSoup(str(i),"lxml") 
            img = s.find('image')
            img_tag = img.get('src')
            #print(img_tag)
            fo.write('''<img src="'''+str(img_tag)+'''"/><br/>''')
            
        tex=soup.find_all('text')
        
        if page_no == CENTER :  
            #....Centralises copy right page
            fo.write("<center>"+"\n")
            for x in tex:
                 soup = BeautifulSoup(str(x),"lxml") 
                 tag = soup.find('text')
                 font = tag.get('font') 
                 header =tag.get('top')
                 if header_match(header) == 0 or font_match(font) == 0:
                     continue                 
                 con = soup.find('text')
                 c =con.contents
                 for i in c:
                     line = str(i)
                     text_line =  line +"<br/>" + "\n"
                     fo.write(text_line )
            fo.write("</center>"+"\n")
            fo.write("</p>" +"\n")
            continue
        
        if page_no >= CONTENT_PAGE_START and page_no <= CONTENT_PAGE_END:   
            #......Fix content pages..............                     
            for x in tex:
                 soup = BeautifulSoup(str(x),"lxml") 
                 tag = soup.find('text')
                 font = tag.get('font') 
                 header =tag.get('top')
                 if header_match(header) == 0 or font_match(font) == 0:
                     continue                 
                 con = soup.find('text')
                 c =con.contents
                 for i in c:
                     line = str(i)
                     text_line =  line +"<br/>" + "\n"
                     fo.write(text_line )           
            fo.write("</p>" +"\n")
            continue
        
        texy = tex +['<text top="0" left="0" width="0" height="0" font="0">SAMPLE TEXT</text>']
        for x, y in zip(tex, texy[1:]):
            #print("x= ",x,"\n","y = ",y)  
            soup = BeautifulSoup(str(y),"lxml") 
            tag = soup.find('text')
            indent_next = int(tag.get('left'))
            nextline_header = tag.get('top')
            nextline_top = int(tag.get('top'))
            nextline_font = tag.get('font')
            
            
            soup =BeautifulSoup(str(x),"lxml")
            tag = soup.find('text')
            #indent = int(tag.get('left'))
            indent = int(tag.get('left'))
            font = tag.get('font') 
            header =tag.get('top')
            line_top = int(tag.get('top'))
            
            if header_match(header) == 0 or font_match(font) == 0:
                continue         
                         
            con = soup.find('text')
            c =con.contents
            #print(c)
            for i in c:
                line = str(i)
                text_line = heading(line,font)
                if text_line == 'NULL':
                     pass
                else:
                    fo.write("</p>"+"\n")
                    fo.write(text_line)
                    fo.write("<p>"+"\n")
                    continue  
                
                if indent >= BLOCK_LOWER and indent <= BLOCK_UPPER:                                                      
                    if quote == 0 and indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER: 
                        # ..Biginning of blockquote.....
                        #fo.write("..quote...A...")
                        text_line="<blockquote>"+line+ "\n"
                        fo.write(text_line)
                        quote = 1 
                    elif quote == 0 and indent_next < BLOCK_LOWER : 
                        #.......Bigining of paragraph..............
                        #fo.write("..quote..B...")
                        text_line=line+ "\n"
                        fo.write(text_line) 
                    elif quote ==1 and  indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER: 
                        #......Lines within blockquote
                        #fo.write("..quote..C...")
                        text_line = line+ "\n"
                        fo.write(text_line)  
                    elif quote ==1 and  indent_next>= BLOCK_LOWER : 
                        #......Lines within blockquote
                        #fo.write("..quote..D...")
                        text_line = line+ "\n"
                        fo.write(text_line)    
                    elif (quote ==1 and  header_match(nextline_header) == 0 ) or ( quote ==1 and font_match( nextline_font) == 0): 
                        # ...If last line of page is blockquote
                        #fo.write("..quote.E..")
                        text_line = line +"\n" 
                        fo.write(text_line) 
                    elif quote ==1 and indent_next < BLOCK_LOWER and PARA_INDENT  == BLOCK_QUOTE : 
                        #....Check begining of Paragraph after a block quote when both blockquote and paragraph have same indent
                        #fo.write("..quote.F..")
                        text_line=  "</blockquote>"+ "</p>" + "\n" + "<p>" +"\n" + line +"\n"
                        fo.write(text_line)
                        quote = 0
                    elif quote ==1 and indent_next < BLOCK_LOWER and PARA_INDENT  != BLOCK_QUOTE:  
                        #....Check begining of Paragraph after a block quote when both blockquote and paragraph have different indent
                        #fo.write("..quote.G..")
                        text_line= line +"\n" + "</blockquote>"+ "</p>" + "\n" + "<p>" +"\n"
                        fo.write(text_line)
                        quote = 0
                    else:
                        pass 
                elif quote == 1 and indent > BLOCK_UPPER:
                    # Citation after the blockquote
                    if indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER: 
                        #fo.write("..quote..H.")
                        text_line = "<br/>"+line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        fo.write(text_line) 
                        quote = 0
                    elif indent_next <= BLOCK_LOWER   :
                        #fo.write("..quote..I.")
                        text_line = "<br/>"+line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        fo.write(text_line) 
                        quote = 0
                    else:
                        #fo.write("..quote..J.")
                        text_line ="<br/>"+ line.rstrip('\n') +"\n" 
                        fo.write(text_line)                                    
                else: 
                   
                   if quote == 1 and indent_next < BLOCK_LOWER : 
                       #fo.write("..quote..K.")
                       text_line= "</blockquote>"+"</p> " + "\n" +"<p>"+ line + "\n" 
                       fo.write(text_line)
                       quote = 0 
                   text_line = superscript(line,font, line_top, nextline_top )  #checks for super script and subscript
                   if text_line == 'NULL':                        
                        pass
                   else:
                        fo.write(text_line + "\n")
                        continue
                   line = footnote(line,font) #checks for footnotes     
                   line_gap = check_line_spacing(line_top, nextline_top)   
                   if line_gap >= 2*LINE_SPACING - 2  and    line_gap <= 2*LINE_SPACING + 2 :
                        text_line = line +"<br/>" +"<br/>" +"\n" 
                   p = paragraph_check(indent_next)
                   if p == 1:
                       text_line = line+"</p>"+"\n"+"<p>"                                                                          
                   else:
                       text_line = line+"\n"                        
                   fo.write(text_line)
        if center == 1:
            fo.write("</center>"+"\n")
            center = 0                                                                                    
        if quote == 1:
            fo.write("</blockquote>")              
        fo.write("</p>"+"\n")            
    fo.write("</html>") 
    fo.close()
    fin.close() 

def usage():
 print ("""	
	Usage: Type at the command prompt
	python xmltohtml.py -i <inputfile> -o <outputfile> 
	inputfile     =  name of the input file. Must be a xml file.
	outputfile    =  name of the output file. Must be a html file.
	eg:
	 xmltohtml.py -i fin.xml -o fout.html 
	"""	)

if __name__ == '__main__':
    main()

