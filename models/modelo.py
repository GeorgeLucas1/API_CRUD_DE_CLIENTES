# models/modelo.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
from database.banco import Base


# aqui e a criação dos modelos do banco de dados

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    idade = Column(Integer)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    cnpj = Column(String(14), unique=True, index=True)
    cep = Column(String(8), index=True)
    endereco = Column(String)
    telefone = Column(String(15), index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="cliente")


class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="categoria")


class Fornecedor(Base):
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    contato = Column(String)
    telefone = Column(String(15), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    endereco = Column(String)
    
    # Relacionamentos
    produtos = relationship("Produto", back_populates="fornecedor")


class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    estoque_quantidade = Column(Integer, default=0)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    
    # Relacionamentos
    categoria = relationship("Categoria", back_populates="produtos")
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    pedidos = relationship("PedidoItem", back_populates="produto")


class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    data_pedido = Column(DateTime, default=datetime.utcnow)
    status = Column(String, index=True, default="pendente")
    valor_total = Column(Float, default=0.0)
    
    # Foreign Keys
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="pedidos")
    funcionario = relationship("Funcionario", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")


class PedidoItem(Base):
    __tablename__ = "pedidos_itens"
    
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Foreign Keys
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="pedidos")


class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    cargo = Column(String, index=True)
    salario = Column(Float)
    data_contratacao = Column(DateTime, default=datetime.utcnow)
    telefone = Column(String(15), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    ativo = Column(Integer, default=1)  # 1=ativo, 0=inativo
    
    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="funcionario")