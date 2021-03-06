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
# It is the difference of "top" values of two neighbouring lines .Only one numeric value can be assigned
# eg LINE_SPACING = 18 . If no value LINE_SPACING = ''
LINE_SPACING = 18
# Paragraph intend must be the value of "left" in xml file . Each value must be without quote and seperated by coma. 
#eg: PARA_INDENT = [252,253,254,255]. if no values PARA_INDENT = []
PARA_INDENT = [241, 247]
# Block qoute must be the value of "left" in xml file . Each value must be with quote and seperated by coma. 
#eg: BLOCK_QUOTE = ['254','255'] 
BLOCK_QUOTE = ['0'] 

unwanted_font = ['']
# Header must be the value of "top" in xml file. Each value must be with quote and seperated by coma. 
#header reperesent the line no of headers and footers to be avoided printing.
#eg: HEADER = ['14','15']. if no values PARA_INDENT = [''] 
HEADER = ['54','69','72','163','166','167','1032','1031','1053','1054']
#LINE_SPACING = ''
CENTER = ''
CONTENT_PAGE_START = 8
CONTENT_PAGE_END = 9
INDEX = list(range(422,438))
# H1,H2,H3,H4 must be the value of "font" in xml file. Value must be in quote. Only one value can be assighed to each.
# This represent the headings to be displayed as chapter name.
# eg H1 = '11' .If no vale H1 = '' and so on
H1 = '17'
H2 = '18'
H3 = '13' 
H4 = '18'
# Super font must be the value of "font" in xml file. Each value must be with quote and seperated by coma. 
#eg: SUPER_FONT  = ['14','15']. if no values PARA_INDENT = [''] 
SUPER_FONT = ['5']
# Footnotes font must be the value of "font" in xml file. Each value must be with quote and seperated by coma. 
#eg: FOOTNOTES_FONT  = ['14','15']. if no values PARA_INDENT = [''] 
FOOTNOTES_FONT = ['15']
#==============================================================================
BLOCK_LOWER = int(BLOCK_QUOTE[0])    
l = len(BLOCK_QUOTE)-1 
BLOCK_UPPER = int(BLOCK_QUOTE[l])   
       
def match(BLOCK_QUOTE,PARA_INDENT):
    for i in BLOCK_QUOTE:
        if int(i) in PARA_INDENT:
            return True
        return False                                                       
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
def check_line_spacing(line_top, nextline_top)   :
    return nextline_top - line_top
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
        else:
            return 'NULL'       
def paragraph_check(indent_next):
    para = 0
    for n in PARA_INDENT :
        if  n == indent_next :
            para = 1    
    return para                
            
def main():
    Input_File_Name  = ''
	# Assigns the out put file name
    Output_File_Name = ''
    try:
      		opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["infile=","outfile="])
    except getopt.GetoptError:
      		print ('xmltohtml.py -i <inputfile> -o <outputfile> ')
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
    if  Output_File_Name ==''   :
        text = Input_File_Name
        split = re.split(r'\.(?!\d)', text)
        #print(split[0])
        Output_File_Name  = split[0]+"."+"html"
        #print(Output_File_Name  )
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
    fo.write("<title>" + Output_File_Name + "</title>"+ "\n")
    fo.write('''<style type="text/css">'''+ "\n")
    fo.write(
             '''h1 {
                            text-align: center;
                    }

                h2 {
                            text-align: center;
                    }
                    ''')
    fo.write('''
                p {
                            padding: 0cm 0cm 0cm 0cm;               
                            text-align:justify;
                    }
                    ''')
    fo.write('''
                blockquote { 
                            display: block;
                            margin-top: 1em;
                            margin-bottom: 1em;
                            margin-left: 40px;
                            margin-right: 40px;
                            text-align:justify;
                    }
                    ''')
    fo.write('''
                .indent{
                            margin: .1em 0em 0em 0em;
                            font-size: 100%;
                            text-align: justify;
                            text-indent: 1em;
                    }
                    ''')
    fo.write('''
                small{
                            font-size: 90%;
                    }
                    ''')
    fo.write('''
                .note{
                            margin: .1em 0em 0em 1.8em;
                            font-size: 90%;
                            text-indent:-0.8em;
                    }
                    ''')    
    fo.write("</style>"+"\n")
    fo.write("</head>"+"\n")
    fo.write('''<body bgcolor="#FFFFFF" vlink="blue" link="blue">'''+"\n")
     
    soup = BeautifulSoup(fin,'xml')    
    #print(soup)
    
    if soup.outline != None:  
        outline = soup.outline.find_all('item')
    #if outline:
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
        previous_line_top = 0
        if index_check(page_no) == 0:
            #..........Skips the index pages...............
            continue
        
        fo.write("<p>") 
        
        soup =BeautifulSoup(str(p),'xml')
        pgref = soup.find('page')
        pg_tag = pgref.get('number')
        fo.write("<a name="+pg_tag+"></a>"+"\n")
        
        image = soup.find_all('image')
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
        
        if CONTENT_PAGE_START != '':
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
                    
            #print(line_top)

            if header_match(header) == 0 or font_match(font) == 0:
                continue         
                         
            con = soup.find('text')
            c =con.contents
            #print(c)
            Line = ''
            line = ['']            
            for i in c:
                #line = str(i)
                Line = Line + str(i)
            line[0] = Line
            for i in line:
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
                        line_gap = check_line_spacing(line_top, nextline_top)  
                        if line_gap >= 2*LINE_SPACING - 2  and line_gap <= 2*LINE_SPACING + 2 :
                            text_line = text_line +"<br/>" +"<br/>" +"\n"     
                        fo.write(text_line)
                        quote = 1 
                    elif quote == 0 and indent_next < BLOCK_LOWER : 
                        #.......Bigining of paragraph..............
                        #fo.write("..quote..B...")                        
                        if match(BLOCK_QUOTE,PARA_INDENT) == True:
                            fo.write("..quote..B1...")
                            text_line = line + "\n" 
                        else:
                            fo.write("..quote..B2...")
                            text_line=line+"</p>" + "\n" + "<p>" +"\n" 
                        fo.write(text_line) 
                    elif quote ==1 and  indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER: 
                        #......Lines within blockquote
                        #fo.write("..quote..C...")             
                        line_gap = check_line_spacing(line_top, nextline_top)                           
                        if line_gap >= 2*LINE_SPACING - 2  and line_gap <= 2*LINE_SPACING + 2 :
                            text_line = line +"<br/>" +"<br/>" +"\n"  
                        else:
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
                    elif quote ==1 and indent_next < BLOCK_LOWER :                         
                        #fo.write("..quote.F..")
                        if match(BLOCK_QUOTE,PARA_INDENT) == True:
                            #....Check begining of Paragraph after a block quote when both blockquote and paragraph have same indent
                            fo.write("..quote..F1...")
                            text_line=  "</blockquote>"+ "</p>" + "\n" + "<p>" +"\n" + line +"\n"
                        else:
                            fo.write("..quote..F2...")
                            #....Check begining of Paragraph after a block quote when both blockquote and paragraph have different indent
                            text_line= line +"\n" + "</blockquote>"+ "</p>" + "\n" + "<p>" +"\n"
                        fo.write(text_line)                         
                        quote = 0                    
                    else:
                        #pass 
                        #fo.write("..quote.H..")
                        text_line="<blockquote>"+line+ "\n"
                        fo.write(text_line)    
                        quote = 1
                elif quote == 1 and indent > BLOCK_UPPER:
                    # Citation after the blockquote
                    if indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER and line_top ==  previous_line_top: 
                        #fo.write("..quote..I.")
                        text_line = line  +"\n" 
                        line_gap = check_line_spacing(line_top, nextline_top)  
                        if line_gap >= 2*LINE_SPACING - 2  and line_gap <= 2*LINE_SPACING + 2 :
                            text_line = text_line +"<br/>" +"<br/>" +"\n"
                        fo.write(text_line) 
                    elif indent_next>= BLOCK_LOWER  and line_top ==  previous_line_top: 
                        #fo.write("..quote..J1.")
                        text_line = line  +"\n" 
                        fo.write(text_line) 
                        #quote = 0
                    elif indent_next>= BLOCK_LOWER and indent_next <= BLOCK_UPPER and line_top !=  previous_line_top: 
                        #fo.write("..quote..J.")
                        text_line = "<br/>"+line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        fo.write(text_line) 
                        quote = 0
                    elif indent_next <= BLOCK_LOWER and (line_top - previous_line_top == 1 or line_top - previous_line_top == -1):
                        #fo.write("..quote..K.")
                        text_line = line +"\n" 
                        fo.write(text_line) 
                    elif indent_next <= BLOCK_LOWER :
                        #fo.write("..quote..L.")
                        if line_top ==  previous_line_top:                            
                            text_line = line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        else:
                            text_line = "<br/>"+line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        fo.write(text_line) 
                        quote = 0
                    elif indent_next <= BLOCK_LOWER and line_top ==  previous_line_top: #
                        #fo.write("..quote..M.")
                        text_line = line +"</blockquote>"+"</p>" + "\n" +"<p>" +"\n" 
                        fo.write(text_line) 
                        quote = 0
                    elif nextline_top < line_top or nextline_top > line_top:
                        text_line = superscript(line,font, line_top, nextline_top )  #checks for super script and subscript
                        if text_line == 'NULL':                        
                            pass
                        else:
                            fo.write(text_line + "\n")
                    else:
                        #fo.write("..quote..N.")
                        #text_line ="<br/>"+ line.rstrip('\n') +"\n" 
                        text_line ="<br/>"+ line +"\n" 
                        fo.write(text_line)                                    
                else: 
                   
                   if quote == 1 and indent_next < BLOCK_LOWER : 
                       #fo.write("..quote..O.")
                       text_line= "</blockquote>"+"</p> " + "\n" +"<p>"+ line + "\n" 
                       fo.write(text_line)
                       quote = 0 
                   text_line = superscript(line,font, line_top, nextline_top )  #checks for super script and subscript
                   if text_line == 'NULL':                        
                        text_line = line
                   else:
                        fo.write(text_line + "\n")
                        continue
                   line_gap = check_line_spacing(line_top, nextline_top)   
                   #if line_gap >= 1.5*LINE_SPACING - 2  and    line_gap <= 1.5*LINE_SPACING + 2 :
                   if line_gap >= LINE_SPACING + 5  and    line_gap <= 2*LINE_SPACING :
                        text_line = line +"<br/>" +"<br/>" +"\n"   
                        fo.write(text_line + "\n")
                        continue                                      
                   text_line = footnote(line,font) #checks for footnotes  
                   if  text_line ==  'NULL':
                        text_line = line
                        fn = 0
                   else:
                   		#fo.write("<br/>")
                   		if fn == 0:
                   			fo.write("<br/><br/>")
                   			fo.write(text_line + "\n")
                   			fn = 1
                   		else:  
                   		    if line.isdigit() and line.isdigit()<100:  
                   			    print(line)
                   			    fo.write("<br/>")         			
                   			    fo.write("<small>"+line +"</small>"+ "  "+"\n")
                   			    fn=1
                   		    else:
                   			    fo.write(text_line + "\n")
                   			    fn=1                   				
                   		continue

                   p = paragraph_check(indent_next)
                   if p == 1:
                       #text_line = text_line +"</p>"+"\n"+"<p >"   
                       text_line = text_line +"</p>"+"\n"+ '''<p class="indent">'''                                                                          
                   else:                        
                       text_line = text_line +"\n"                                        
                   fo.write(text_line)
                if SUPER_FONT[0] != '':
                    if int(font) != int(SUPER_FONT[0]): 
                        #print ("line_top =",line_top," previous_line_top =", previous_line_top)
                        previous_line_top = line_top   
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
