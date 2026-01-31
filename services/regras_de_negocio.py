# services/cliente_service.py
"""
Service para gerenciar a lógica de negócio relacionada a Clientes.
Contém todas as regras de negócio e validações.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from models.modelo import Cliente
from  middleware.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteService:
    """
    Service Layer para operações de Cliente.
    
    Responsabilidades:
    - Validações de negócio
    - Regras de negócio
    - Acesso ao banco de dados
    - Transações
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o service com a sessão do banco de dados.
        
        Args:
            db (Session): Sessão do SQLAlchemy
        """
        self.db = db
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def criar_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente no sistema.
        
        Args:
            cliente_data (ClienteCreate): Dados do cliente a ser criado
            
        Returns:
            Cliente: Cliente criado
            
        Raises:
            HTTPException: Se CPF ou email já estiverem cadastrados
        """
        # Validações de negócio
        self._validar_cpf_unico(cliente_data.cpf)
        self._validar_email_unico(cliente_data.email)
        
        # Criar e salvar cliente
        novo_cliente = Cliente(**cliente_data.model_dump())
        self.db.add(novo_cliente)
        self.db.commit()
        self.db.refresh(novo_cliente)
        
        return novo_cliente
    
    def listar_clientes(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Lista todos os clientes com paginação.
        
        Args:
            skip (int): Número de registros para pular
            limit (int): Número máximo de registros
            
        Returns:
            List[Cliente]: Lista de clientes
        """
        return self.db.query(Cliente).offset(skip).limit(limit).all()
    
    def obter_cliente_por_id(self, cliente_id: int) -> Cliente:
        """
        Obtém um cliente pelo ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            Cliente: Cliente encontrado
            
        Raises:
            HTTPException: Se cliente não for encontrado
        """
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
        
        return cliente
    
    def obter_cliente_por_cpf(self, cpf: str) -> Cliente:
        """
        Obtém um cliente pelo CPF.
        
        Args:
            cpf (str): CPF do cliente
            
        Returns:
            Cliente: Cliente encontrado
            
        Raises:
            HTTPException: Se cliente não for encontrado
        """
        cliente = self.db.query(Cliente).filter(Cliente.cpf == cpf).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com CPF {cpf} não encontrado"
            )
        
        return cliente
    
    def atualizar_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente:
        """
        Atualiza os dados de um cliente.
        
        Args:
            cliente_id (int): ID do cliente
            cliente_data (ClienteUpdate): Novos dados do cliente
            
        Returns:
            Cliente: Cliente atualizado
            
        Raises:
            HTTPException: Se cliente não for encontrado ou email já estiver em uso
        """
        cliente = self.obter_cliente_por_id(cliente_id)
        
        # Validar email se estiver sendo atualizado
        if cliente_data.email and cliente_data.email != cliente.email:
            self._validar_email_unico(cliente_data.email)
        
        # Atualizar apenas campos fornecidos
        update_data = cliente_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cliente, key, value)
        
        self.db.commit()
        self.db.refresh(cliente)
        
        return cliente
    
    def atualizar_email(self, cliente_id: int, novo_email: str) -> Cliente:
        """
        Atualiza apenas o email de um cliente.
        
        Args:
            cliente_id (int): ID do cliente
            novo_email (str): Novo email
            
        Returns:
            Cliente: Cliente com email atualizado
            
        Raises:
            HTTPException: Se cliente não for encontrado ou email já estiver em uso
        """
        cliente = self.obter_cliente_por_id(cliente_id)
        
        # Validar se email já está em uso
        if novo_email != cliente.email:
            self._validar_email_unico(novo_email)
        
        cliente.email = novo_email
        self.db.commit()
        self.db.refresh(cliente)
        
        return cliente
    
    def deletar_cliente(self, cliente_id: int) -> None:
        """
        Deleta um cliente do sistema.
        
        Args:
            cliente_id (int): ID do cliente
            
        Raises:
            HTTPException: Se cliente não for encontrado ou tiver pedidos associados
        """
        cliente = self.obter_cliente_por_id(cliente_id)
        
        #error 400 significa pedido invalido
        if len(cliente.pedidos) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível deletar cliente com pedidos associados. "
                       f"Cliente possui {len(cliente.pedidos)} pedido(s)."
            )
        
        self.db.delete(cliente)
        self.db.commit()
    
    def listar_pedidos_do_cliente(self, cliente_id: int):
        """
        Lista todos os pedidos de um cliente.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            List[Pedido]: Lista de pedidos do cliente
            
        Raises:
            HTTPException: Se cliente não for encontrado
        """
        cliente = self.obter_cliente_por_id(cliente_id)
        return cliente.pedidos
    
    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        """
        Busca clientes por nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome
            
        Returns:
            List[Cliente]: Lista de clientes encontrados
        """
        return self.db.query(Cliente).filter(
            Cliente.nome.ilike(f"%{nome}%")
        ).all()
    
    def contar_clientes(self) -> int:
        """
        Conta o total de clientes cadastrados.
        
        Returns:
            int: Total de clientes
        """
        return self.db.query(Cliente).count()
    
    # ==================== MÉTODOS PRIVADOS (VALIDAÇÕES) ====================
    
    def _validar_cpf_unico(self, cpf: str) -> None:
        """
        Valida se o CPF já está cadastrado.
        
        Args:
            cpf (str): CPF a validar
            
        Raises:
            HTTPException: Se CPF já estiver cadastrado
        """
        cliente_existente = self.db.query(Cliente).filter(Cliente.cpf == cpf).first()
        
        if cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CPF {cpf} já cadastrado no sistema"
            )
    
    def _validar_email_unico(self, email: str) -> None:
        """
        Valida se o email já está cadastrado.
        
        Args:
            email (str): Email a validar
            
        Raises:
            HTTPException: Se email já estiver cadastrado
        """
        cliente_existente = self.db.query(Cliente).filter(Cliente.email == email).first()
        
        if cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {email} já cadastrado no sistema"
            )
    
    def _validar_cpf_formato(self, cpf: str) -> bool:
        """
        Valida o formato do CPF (11 dígitos numéricos).
        
        Args:
            cpf (str): CPF a validar
            
        Returns:
            bool: True se válido
        """
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        return len(cpf_limpo) == 11