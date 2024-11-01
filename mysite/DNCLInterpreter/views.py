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
        if code_text:
            result = ""
            Code.objects.create(code=code_text)
            
            code = code_text
            lexer = Lexer(code)
            try:
                tokens = lexer.tokenize()
                # result += str(tokens)
            except LexerError as e:
                result += e

            parser = Parser(tokens)
            try:
                _, statement = parser.program(0)
                result += statement.print()
            except ParserError as e:
                result += e

            return render(request, self.template_name, {'result': result, 'code': code_text})
        return render(request, self.template_name, {'code': code_text})