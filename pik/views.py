from django.http import JsonResponse
from django.views import View
import json

class CalcApiView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        return JsonResponse({
            'calculation': [
                {
                    'algo': {
                        'code': 'simple',
                        'name': 'Поиск кратчайшего пути'
                    },
                    'score': 0.95,
                    'result': {}
                },
                {
                    'algo': {
                        'code': 'genetic',
                        'name': 'Генетический алгоритм'
                    },
                    'score': 0.88,
                    'result': {}
                }
            ],
            'request': data
        })

