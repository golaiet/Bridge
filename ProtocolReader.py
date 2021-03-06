from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage # supported by python version <= 3.6.3
from io import StringIO
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')


class ProtocolReader():
    """ Protocol reader is the python instantiation of protocol.
    It handles a pdf clinical protocol and outputs a list of sentences """
    def __init__(self, path):
        self.path = path
        self.text = self.convert_pdf_to_txt(path)
        self.text_list = self.text.split('.')
        self.clean_text = self.text_cleanup(self.text)
        self.clean_text_list = self.clean_text.split('.')

    def text_cleanup(self, text):
        print("##### Start text cleanup")
        ps = PorterStemmer()

        ct = str(text).lower() # ct = clean text
        for i in range(1000):
            ct = ct.replace('  ', ' ')
        ct = ct.replace('\n', ' ')
        ct = " ".join([ps.stem(word) for word in ct.split() if not word in set(stopwords.words('english'))])
        print("##### Done text cleanup")
        return ct

    def convert_pdf_to_txt(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        print("##### Text consumed from PDF")
        return text



# def convert_pdf_to_txt(path):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     codec = 'utf-8'
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#     fp = open(path, 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     password = ""
#     maxpages = 0
#     caching = True
#     pagenos=set()
#
#     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
#         interpreter.process_page(page)
#
#     text = retstr.getvalue()
#
#     fp.close()
#     device.close()
#     retstr.close()
#     return text
#
# def cnn(text):
#     text_manipulate = text.lower()
#
#     for i in range(1000):
#         text_manipulate = text_manipulate.replace("  ", " ")
#         text_manipulate = text_manipulate.replace("\n\n", "\n")
#         text_manipulate = text_manipulate.replace("\n \n", "\n")
#     # text_manipulate = text_manipulate.replace("\n", " ")
#     return text_manipulate

# class Engine():
#
#     def __init__(self, path):
#         self.protocol = path
#         self.text = convert_pdf_to_txt(path).lower()
#         self.DM = ""
#         self.ARM = ""
#
# def find_in_text(text, word):
#     start_pointer = 0
#     list = []
#     while text.find(word, start_pointer+len(word)+2)>-1:
#         start_pointer = text.find(word, start_pointer+len(word)+2)
#         # print(start_pointer)
#         list.append(start_pointer)
#     return list
#
#
# def get_line_with_word(text, word):
#     indexs = find_in_text(text.lower(), word.lower())
#     for index in indexs:
#         start_index = text.rfind('.',0,index)
#         end_index = text.find('.',index)
#         print(index)
#         print(text[start_index:end_index+1])
#
# def text_to_list(text):
#     index = 0
#     list = []
#     while text.find('.', index) > -1:
#         new_index = text.find('.', index+1)
#         list.append(text[index: new_index+1])
#         index = new_index
#     return list
#
#
# text = convert_pdf_to_txt('0011.pdf')
# list = text_to_list(text)
# get_line_with_word(text,'Patient')
#
# for line in list:
#     if line.lower().find('patient'):
#         print("XXX:" + line)

# en = Engine('0011.pdf')