from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('clientes',views.ClientesViewSet, basename='clientes')
router.register('endereco',views.EnderecoViewSet)
router.register('contato',views.ContatoViewSet)
router.register('emprestimo',views.EmprestimoViewSet)
router.register('conta',views.ContaViewSet)
router.register('cartao',views.CartaoViewSet)
router.register('investimento',views.InvestimentoViewSet)
router.register('movimentacao',views.MovimentacaoViewSet)

urlpatterns =[] +router.urls