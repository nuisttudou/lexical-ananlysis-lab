from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_main import Ui_MainWindow

content=None
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.set_trigger()
        self.show()
    def set_trigger(self):
        # self.actionloadFile.triggered.connect()
        self.action_lex.triggered.connect(self.set_lex_button)
    # def load_file(self):    
    def set_lex_button(self):
        global content
        content=self.textEdit_in.toPlainText()
        ans=lexer()
        self.textEdit_out.setText(ans)





# token比较大的分类
TOKEN_STYLE = [
    'KEY_WORD', 'ID,name= ', 'NUM,value= ',
    'OPERATOR', 'SEPARATOR', 'STRING_CONSTANT',
    'ERROR'
]

# 将关键字、运算符、分隔符进行具体化
DETAIL_TOKEN_STYLE = {
    'include': 'reserved word:',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'for': 'reserved word:',
    'else': 'reserved word:',
    'while': 'reserved word:',
    'do': 'reserved word:',
    'return': 'reserved word:',
    '=': '',
    '&': '',
    '<': '',
    '>': '',
    '++': '',
    '--': '',
    '+': '',
    '-': '',
    '*': '',
    '/': '',
    '>=': '',
    '<=': '',
    '(': '',
    ')': '',
    '{': '',
    '}': '',
    '[': '',
    ']': '',
    ',': '',
    '"': '',
    ';': '',
    '#': '',
    'if': 'reserved word:',
    'read':  'reserved word:',
    'write': 'reserved word:',
    'then': 'reserved word:',
    'repeat':'reserved word:',
    'until':'reserved word:',
    ':=':'',
    ':':'',
}

# 关键字
keywords = [
    ['int', 'float', 'double', 'char', 'void'],
    ['if', 'for', 'while', 'do', 'else'], ['include', 'return'],
    ['read','write','then','repeat','until']
]

# 运算符
operators = [
    '=', '&', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<=', '!=',':=',':'
]

# 分隔符
delimiters = ['(', ')', '{', '}', '[', ']', ',', '\"', ';']




class Token(object):
    '''记录分析出来的单词'''
    
    def __init__(self, type_index, value,row_number):
        self.type = DETAIL_TOKEN_STYLE[value] if (
            type_index == 0 or type_index == 3 or type_index == 4
        ) else TOKEN_STYLE[type_index]
        self.value = value
        self.row_number = row_number


class Lexer(object):
    '''词法分析器'''

    def __init__(self):
        # 用来保存词法分析出来的结果
        self.tokens = []
        self.row_now=1
        self.is_comment=False

    # 判断是否是空白字符
    def is_blank(self, index):
        if content[index] == '\n' or content[index] == '\r':
            self.row_now+=1
            return True
        return (
            content[index] == ' ' or
            content[index] == '\t' 
        )

    # 跳过空白字符
    def skip_blank(self, index):
        while index < len(content) and self.is_blank(index):
            index += 1
        return index

# 打印
    def print_log(self, style, value):
        print('(%s, %s)' % (style, value))

    # 判断是否是关键字
    def is_keyword(self, value):
        for item in keywords:
            if value in item:
                return True
        return False

    # 词法分析主程序
    def main(self):
        i = 0
        while i < len(content):
            i = self.skip_blank(i)
            #注释中
            if self.is_comment:
                if content[i]=='}':
                    self.is_comment=False
                i+=1
                continue
            # 如果是字母或者是以下划线开头
            elif content[i].isalpha() or content[i] == '_':
                # 找到该字符串
                temp = ''
                while i < len(content) and (
                        content[i].isalpha() or
                        content[i] == '_' or
                        content[i].isdigit()):
                    temp += content[i]
                    i += 1
                # 判断该字符串
                if self.is_keyword(temp):
                    # self.print_log( '关键字', temp )
                    self.tokens.append(Token(0, temp,self.row_now))
                else:
                    # self.print_log( '标识符', temp )
                    self.tokens.append(Token(1, temp,self.row_now))
                i = self.skip_blank(i)
                continue
            # 如果是数字开头
            elif content[i].isdigit():
                temp = ''
                while i < len(content):
                    if content[i].isdigit() or (
                            content[i] == '.' and content[i + 1].isdigit()):
                        temp += content[i]
                        i += 1
                    elif not content[i].isdigit():
                        if content[i] == '.':
                            print('float number error!')
                            exit()
                        else:
                            break
                # self.print_log( '常量' , temp )
                self.tokens.append(Token(2, temp,self.row_now))
                i = self.skip_blank(i)
                continue
            # 如果是分隔符
            elif content[i] in delimiters:
                # self.print_log( '分隔符', content[ i ] )
                if content[i] == '{':
                    self.is_comment=True
                    i+=1
                    continue
                else:
                    self.tokens.append(Token(4, content[i],self.row_now))
                    # 如果是字符串常量
                    if content[i] == '\"':
                        i += 1
                        temp = ''
                        while i < len(content):
                            if content[i] != '\"':
                                temp += content[i]
                                i += 1
                            else:
                                break
                        else:
                            print('error:lack of \"')
                            exit()
                        # self.print_log( '常量' , temp )
                        self.tokens.append(Token(5, temp,self.row_now))
                        # self.print_log( '分隔符' , '\"' )
                        self.tokens.append(Token(4, '\"',self.row_now))
                    i = self.skip_blank(i + 1)
                continue
            # 如果是运算符
            elif content[i] in operators:
                # 如果是++或者--
                if (content[i] == '+' or content[i] == '-') and (
                        content[i + 1] == content[i]):
                    # self.print_log( '运算符', content[ i ] * 2 )
                    self.tokens.append(Token(3, content[i] * 2,self.row_now))
                    i = self.skip_blank(i + 2)
                # 如果是>=或者<=
                elif (content[i] == '>' or content[i] == '<') and content[i + 1] == '=':
                    # self.print_log( '运算符', content[ i ] + '=' )
                    self.tokens.append(Token(3, content[i] + '=',self.row_now))
                    i = self.skip_blank(i + 2)
                # 如果是:=
                elif content[i] == ':' and content[i + 1] == '=':
                    # self.print_log( '运算符', content[ i ] + '=' )
                    self.tokens.append(Token(3, content[i] + '=',self.row_now))
                    i = self.skip_blank(i + 2)
                else:
                    # self.print_log( '运算符', content[ i ] )
                    self.tokens.append(Token(3, content[i],self.row_now))
                    i = self.skip_blank(i + 1)
                continue
            #Error
            else:
                # print('error:',self.row_now)
                temp = ''
                while i < len(content) and not (
                        # content[i].isalpha() or
                        # content[i] == '_' or
                        # content[i].isdigit()):
                        content[i] == '\n' or content[i] == '\r' or content[i] == ' ' or content[i] == '\t' ):
                    temp += content[i]
                    i += 1
                self.tokens.append(Token(6, temp,self.row_now))
                i = self.skip_blank(i + 1)


def lexer():
    lexer = Lexer()
    lexer.main()
    out=""
    for token in lexer.tokens:#输出
        # print(token.row_number,':',token.type,'', token.value) #print('(%s, %s)' % (token.type, token.value))
        out+=str(token.row_number)+': '+token.type+' '+token.value+"\n" #print('(%s, %s)' % (token.type, token.value))
    print(out)
    return out






if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()