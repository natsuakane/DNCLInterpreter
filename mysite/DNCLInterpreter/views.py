from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Code
from .Interpreter.Lexer import *
from .Interpreter.MyParser import *
from .Interpreter.Expression import *

class IndexView(TemplateView):
    template_name = 'DNCLInterpreter/index.html'

    def post(self, request, *args, **kwargs):
        code_text = request.POST.get('code', '')
        input_data = request.POST.get('input', '')
        if code_text and input_data:
            Code.objects.create(code=code_text, input_d=input_data)
            
            result = ""
            code = code_text
            lexer = Lexer(code)
            try:
                tokens = lexer.tokenize()
            except LexerError as e:
                result += str(e)

            parser = Parser(tokens)
            try:
                IOProcess.init()
                IOProcess.input(input_data)
                _, program = parser.program(0)
                program.evaluate()
                result += "正常に実行されました\r\n"
                for o in IOProcess.get_output():
                    result += "{0}\r\n".format(o)
            except ParserError as e:
                result += str(e)

            return render(request, self.template_name, {'result': result, 'code': code_text, 'input': input_data})
        return render(request, self.template_name, {'code': code_text})