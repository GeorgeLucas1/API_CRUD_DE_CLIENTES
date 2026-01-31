# routers/clientes.py
"""
Router para endpoints de Clientes.
Responsável apenas por receber requisições HTTP e chamar os services.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.sessao import get_db
from services.regras_de_negocio import ClienteService
from middleware.cliente_schema import ClienteCreate, ClienteResponse, ClienteUpdate


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)



@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cria um novo cliente no sistema. CPF e email devem ser únicos."
)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo cliente.
    
    - **nome**: Nome completo do cliente
    - **email**: Email único do cliente
    - **cpf**: CPF único (11 dígitos)
    - **telefone**: Telefone de contato (opcional)
    - **endereco**: Endereço completo (opcional)
    """
    service = ClienteService(db)
    return service.criar_cliente(cliente)


@router.get(
    "/",
    response_model=List[ClienteResponse],
    summary="Listar todos os clientes",
    description="Lista todos os clientes com paginação."
)
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista clientes com paginação.
    
    - **skip**: Número de registros para pular (padrão: 0)
    - **limit**: Número máximo de registros (padrão: 100)
    """
    service = ClienteService(db)
    return service.listar_clientes(skip=skip, limit=limit)


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Obter cliente por ID",
    description="Retorna um cliente específico pelo ID."
)
def obter_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um cliente pelo ID.
    
    - **cliente_id**: ID do cliente
    """
    service = ClienteService(db)
    return service.obter_cliente_por_id(cliente_id)


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente."
)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados de um cliente.
    
    - **cliente_id**: ID do cliente
    - Apenas os campos fornecidos serão atualizados
    """
    service = ClienteService(db)
    return service.atualizar_cliente(cliente_id, cliente_update)


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente",
    description="Remove um cliente do sistema."
)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um cliente.
    
    - **cliente_id**: ID do cliente
    - Não é possível deletar clientes com pedidos associados
    """
    service = ClienteService(db)
    service.deletar_cliente(cliente_id)
    return None


# ==================== ENDPOINTS ESPECÍFICOS ====================

@router.get(
    "/cpf/{cpf}",
    response_model=ClienteResponse,
    summary="Buscar cliente por CPF",
    description="Retorna um cliente pelo CPF."
)
def obter_por_cpf(
    cpf: str,
    db: Session = Depends(get_db)
):
    """
    Busca cliente por CPF.
    
    - **cpf**: CPF do cliente (11 dígitos)
    """
    service = ClienteService(db)
    return service.obter_cliente_por_cpf(cpf)


@router.patch(
    "/{cliente_id}/email",
    response_model=ClienteResponse,
    summary="Atualizar email do cliente",
    description="Atualiza apenas o email de um cliente."
)
def atualizar_email(
    cliente_id: int,
    email: str,
    db: Session = Depends(get_db)
):
    """
    Atualiza apenas o email do cliente.
    
    - **cliente_id**: ID do cliente
    - **email**: Novo email (deve ser único)
    """
    service = ClienteService(db)
    return service.atualizar_email(cliente_id, email)


@router.get(
    "/{cliente_id}/pedidos",
    summary="Listar pedidos do cliente",
    description="Lista todos os pedidos de um cliente específico."
)
def listar_pedidos_do_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Lista pedidos de um cliente.
    
    - **cliente_id**: ID do cliente
    """
    service = ClienteService(db)
    return service.listar_pedidos_do_cliente(cliente_id)


# ==================== ENDPOINTS DE BUSCA ====================

@router.get(
    "/buscar/nome",
    response_model=List[ClienteResponse],
    summary="Buscar clientes por nome",
    description="Busca clientes cujo nome contenha o texto fornecido."
)
def buscar_por_nome(
    nome: str,
    db: Session = Depends(get_db)
):
    """
    Busca clientes por nome (busca parcial).
    
    - **nome**: Texto para buscar no nome
    """
    service = ClienteService(db)
    return service.buscar_por_nome(nome)


@router.get(
    "/estatisticas/total",
    summary="Total de clientes",
    description="Retorna o número total de clientes cadastrados."
)
def contar_clientes(db: Session = Depends(get_db)):
    """
    Conta total de clientes.
    """
    service = ClienteService(db)
    total = service.contar_clientes()
    return {"total_clientes": total}