from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import base64
from django.core.files.base import ContentFile
from rest_framework.response import Response
import random

from django.db.models import Q

def base64_file(data, name):
    # print(data)
    format, img_str = data.split(';base64,')
    ext = 'png'
    return ContentFile(base64.b64decode(img_str), name='{}.{}'.format(name, ext))



class ClientesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ) 
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        # query            
        cpf = self.request.query_params.get('cpf')
        if cpf is not None:
            usuario =  get_object_or_404(Cliente, user__id_fiscal=cpf)
            if usuario is not None:
                print("caiu aqui")
                queryset = queryset.filter(id=usuario.id)
            return queryset
        else:
            queryset = Cliente.objects.all()
            return queryset

    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
        print(token)
        dados_TOKEN = AccessToken(token)
        usuario = dados_TOKEN['user_id']
        print(usuario)
        clienteObject = CustomUser.objects.get(id=usuario)
        print(clienteObject)
        dados = request.data
        print(dados)    
        criar =Cliente.objects.create(
            rg = dados['rg'],
            nome = dados['nome'],
            user = clienteObject,
            foto =  base64_file(dados['foto'],f"foto {dados['nome']}"),
            dt_nascimento = dados['dt_nascimento']
        )
        return super().list(request, *args, **kwargs)

class EnderecoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    
    
    # def retrieve(self, request, *args, **kwargs):
    #     token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
    #     print(token)
    #     dados_TOKEN = AccessToken(token)
    #     usuario = dados_TOKEN['user_id']
    #     print(usuario)
    #     item = get_object_or_404(self.queryset, cliente=usuario)
    #     serializer = EnderecoSerializer(item)
    #     # EnderecoObject = Endereco.objects.get(Cliente=usuario)
    #     return Response(serializer.data)
    

       
    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
        print(token)
        dados_TOKEN = AccessToken(token)
        usuario = dados_TOKEN['user_id']
        print(usuario)
        clienteObject = Cliente.objects.get(user=usuario)
        print(clienteObject)
        dados = request.data
        print(dados)    
        criar = Endereco.objects.create(
            logradouro = dados['logradouro'],
            bairro = dados['bairro'],
            cep = dados['cep'],
            cidade = dados['cidade'],
            n_casa = dados['n_casa'],
            uf = dados['uf'],
            cliente = clienteObject,
        )
        return super().list(request, *args, **kwargs)

class ContatoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
    
    
    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
        print(token)
        dados_TOKEN = AccessToken(token)
        usuario = dados_TOKEN['user_id']
        print(usuario)
        clienteObject = Cliente.objects.get(user=usuario)
        print(clienteObject)
        dados = request.data
        print(dados)    
        criar = Contato.objects.create(
            telefone = dados['telefone'],
            ramal = dados['ramal'],
            email = dados['email'],
            cliente = clienteObject,
            )
        return super().list(request, *args, **kwargs)
    
    

class ContaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    def get_queryset(self):
        queryset = Conta.objects.all()
        id_Cliente = self.request.query_params.get('cliente')
        if id_Cliente is not None:
            queryset = queryset.filter(cliente=id_Cliente)
            return queryset
        else:
            queryset = Conta.objects.all()
            return queryset
        
    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
        dados_TOKEN = AccessToken(token)
        usuario = dados_TOKEN['user_id']
        clienteObject = Cliente.objects.get(user=usuario)
        dados = request.data
        criar =Conta.objects.create(
            ativo = dados['ativo'],
            agencia = dados['agencia'],
            cliente = clienteObject,
            tipo =  dados['tipo'],
            saldo = dados['saldo'],
            numero = dados['numero'],
        )
        return super().list(request, *args, **kwargs)
    
    # def list(self, request, *args, **kwargs):
    #     token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
    #     print(token)
    #     dados = AccessToken(token)
    #     usuario = dados['user_id']
    #     print(usuario)
    #     listaConta = Conta.objects.filter(pk=usuario)
    #     return super().list(request, *args, **kwargs)

class EmprestimoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

class MovimentacaoViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )  
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    def get_queryset(self):
        queryset = Movimentacao.objects.all()
        id_Conta = self.request.query_params.get('conta')
        if id_Conta is not None:
            queryset = queryset.filter(Q(conta_remetente=id_Conta) | Q(conta_destinatario=id_Conta))
            # queryset +=queryset.filter(conta_destinatario=id_Conta)
            return queryset
        else:
            queryset = Movimentacao.objects.all()
            return queryset     

class InvestimentoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Investimento.objects.all()
    serializer_class = InvestimentoSerializer

class CartaoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )  
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer
    
    def get_queryset(self):
        queryset = Cartao.objects.all()
        id_Conta = self.request.query_params.get('conta')
        if id_Conta is not None:
            cartao = get_object_or_404(Cartao,conta = id_Conta)
            # queryset +=queryset.filter(conta_destinatario=id_Conta)
            return queryset
        else:
            queryset = Cartao.objects.all()
            return queryset     
    
    def create(self, request, *args, **kwargs):
        # aleatorio = random.randint(1,9)
        token = request.META.get('HTTP_AUTHORIZATION', '').split(" ")[1]
        dados_TOKEN = AccessToken(token)
        usuario = dados_TOKEN['user_id']
        ContaObject = Conta.objects.get(id=usuario)
        dados = request.data
        limite_acoount = round(ContaObject.saldo/3)
        cvv=""
        num=""
        for i in range(0,3):
            cvv += str(random.randint(1,9))
            
        for i in range(0,12):
            num += str(random.randint(1,9))
            
            
        print(cvv)
        print(num)
        print(limite_acoount)
      
        criar =Cartao.objects.create(
            numero = num,
            limite = limite_acoount,
            cvv = cvv,
            validade = dados['validade'],
            bandeira = "MasterCard",
            situacao ="B",
            conta =ContaObject
        )
        serializer = CartaoSerializer(criar)
        return Response(serializer.data)

