from .models import * 
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields =['id','nome','foto','dt_nascimento','dt_abertura','rg','user']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields=['id','logradouro','cidade','bairro','uf','cep','cliente','n_casa']

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields=['id','telefone','ramal','observacao','email','cliente']

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields=['id','dt_solicitacao','valor_solicitado','juros','numero_parcela','valor_parcela','aprovado','dt_aprovado','conta']

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id','ativo','agencia','tipo','numero','saldo','cliente']

class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = ['id','numero','validade','cvv','situacao','bandeira','limite','conta']

class InvestimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investimento
        fields = ['id','tipo','aporte','taxaAdministracao','prazo','grauRisco','rentabilidade','finalizado','conta']

class MovimentacaoSerializer(serializers.ModelSerializer):
    nome_cliente_remetente = serializers.ReadOnlyField(source="conta_remetente.cliente.nome")
    nome_cliente_destinatario = serializers.ReadOnlyField(source="conta_destinatario.cliente.nome")
    dataHora = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    # def gerar_nome_remetente(self,a):
    #     return a.conta_remetente.cliente.nome 

    # def gerar_nome_destinatario(self,a):
    #     return a.conta_destinatario.cliente.nome
    
    class Meta:
        model = Movimentacao
        fields = ['id','dataHora','operacao','valor','conta_remetente','conta_destinatario','nome_cliente_remetente','nome_cliente_destinatario']
   
    