# API para Estudo de Arquitetura em Camadas

## Objetivo

Este projeto tem como objetivo **compreender arquitetura em camadas na prática**, utilizando o desenvolvimento de uma API como meio para entender:

- Separação de responsabilidades  
- Organização de código  
- Redução de acoplamento  
- Melhoria de manutenção, legibilidade e testabilidade  

A API não tem como foco principal funcionalidades complexas, mas sim **clareza arquitetural**.

## Motivação

Arquitetura em camadas é amplamente utilizada no mercado por facilitar a evolução do sistema ao longo do tempo. Ao estruturar o código em camadas bem definidas, torna-se mais simples:

- Identificar onde cada regra deve existir  
- Alterar partes do sistema sem afetar outras  
- Escalar o projeto de forma controlada  

Este projeto serve como laboratório para esse aprendizado.

## Arquitetura Utilizada

A aplicação segue uma arquitetura em camadas, onde cada camada possui uma responsabilidade única.

### Camadas

#### 1. Server (Main)
- Inicializa a aplicação FastAPI
- Registra middlewares e rotas
- Não contém regras de negócio

#### 2. Routers (Controllers)
- Define os endpoints HTTP
- Recebe e responde requisições
- Chama a camada de serviços
- Não acessa diretamente o banco de dados

#### 3. Schemas (DTOs)
- Define os formatos de entrada e saída
- Realiza validações com Pydantic
- Desacopla a API dos modelos do banco

#### 4. Services
- Contém as regras de negócio
- Centraliza decisões do domínio
- Não depende de HTTP ou banco de dados

#### 5. Repositories
- Responsável pelo acesso ao banco
- Executa queries e operações CRUD
- Não contém lógica de negócio

#### 6. Models
- Mapeamento das tabelas do banco de dados
- Representação persistente das entidades

#### 7. Database
- Configuração da conexão
- Criação de engine e sessões
- Infraestrutura de persistência

## Benefícios da Arquitetura em Camadas

- Código mais organizado e previsível  
- Facilidade de manutenção  
- Melhor isolamento de responsabilidades  
- Testes unitários mais simples  
- Facilidade para trocar banco ou framework  

## Conclusão

O desenvolvimento desta API é uma ferramenta prática para compreender como a arquitetura em camadas impacta diretamente a qualidade do código. O foco está menos na funcionalidade final e mais na **forma como o sistema é estruturado**.
