from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Code

class IndexView(TemplateView):
    template_name = 'DNCLInterpreter/index.html'

    def post(self, request, *args, **kwargs):
        code_text = request.POST.get('code', '')
        if code_text:
            Code.objects.create(code=code_text)
            # ここでコードを実行するロジックを追加
            result = "コードが正常に保存されました。"
            return render(request, self.template_name, {'result': result})
        return render(request, self.template_name)