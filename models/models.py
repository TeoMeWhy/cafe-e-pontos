from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    cpf = Column(String, unique=True, nullable=False, index=True)  # Índice adicionado
    nome_completo = Column(String, nullable=False)
    email = Column(String, nullable=True)
    aniversario = Column(Date, nullable=True)
    telefone = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    pontos = Column(Integer, default=0)
    transacoes = relationship('Transacao', back_populates='cliente')


class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String, nullable=False)
    preco_venda = Column(Float, nullable=False)
    preco_custo = Column(Float, nullable=False)
    pontos_compra = Column(Integer, nullable=False)
    pontos_resgate = Column(Integer, nullable=True)
    produto_transacoes = relationship('ProdutoTransacao', back_populates='produto')


class Transacao(Base):
    __tablename__ = 'transacao'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    data = Column(DateTime, nullable=False)
    valor_moeda_cento = Column(Integer, nullable=False)
    valor_moeda_cento_final = Column(Integer, nullable=False)
    valor_pontos = Column(Integer, nullable=False)
    cliente = relationship('Cliente', back_populates='transacoes')
    produtos = relationship('ProdutoTransacao', back_populates='transacao')


class ProdutoTransacao(Base):
    __tablename__ = 'produto_transacao'

    id = Column(Integer, primary_key=True)
    transacao_id = Column(Integer, ForeignKey('transacao.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    transacao = relationship('Transacao', back_populates='produtos')
    produto = relationship('Produto', back_populates='produto_transacoes')