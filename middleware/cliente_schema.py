# middleware/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


#schemas para validação e serialização dos dados ,tamanhos dos dados e etc

# ========== CLIENTE SCHEMAS ==========
class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    idade: Optional[int] = Field(None, ge=0, le=150)
    cpf: str = Field(..., min_length=11, max_length=11)
    cnpj: Optional[str] = Field(None, min_length=14, max_length=14)
    cep: Optional[str] = Field(None, min_length=8, max_length=8)
    endereco: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=15)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    idade: Optional[int] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True


# ========== CATEGORIA SCHEMAS ==========
class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    descricao: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== FORNECEDOR SCHEMAS ==========
class FornecedorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    contato: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=15)
    email: EmailStr
    endereco: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorResponse(FornecedorBase):
    id: int
    
    class Config:
        from_attributes = True


# ========== PRODUTO SCHEMAS ==========
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = None
    preco: float = Field(..., gt=0)
    estoque_quantidade: int = Field(default=0, ge=0)
    categoria_id: int
    fornecedor_id: Optional[int] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = Field(None, gt=0)
    estoque_quantidade: Optional[int] = Field(None, ge=0)
    categoria_id: Optional[int] = None
    fornecedor_id: Optional[int] = None

class ProdutoResponse(ProdutoBase):
    id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True


# ========== PEDIDO SCHEMAS ==========
class PedidoItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)

class PedidoItemResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float
    
    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    cliente_id: int
    itens: List[PedidoItemCreate]

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    data_pedido: datetime
    status: str
    valor_total: float
    itens: List[PedidoItemResponse]
    
    class Config:
        from_attributes = True


# ========== FUNCIONARIO SCHEMAS ==========
class FuncionarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cargo: Optional[str] = None
    salario: Optional[float] = Field(None, gt=0)
    telefone: Optional[str] = Field(None, max_length=15)
    email: EmailStr

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioResponse(FuncionarioBase):
    id: int
    data_contratacao: datetime
    ativo: int
    
    class Config:
        from_attributes = True