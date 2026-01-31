# server/server.py
# Importações necessárias
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.banco import engine, Base
from routers.rota import router as cliente_router

# Criar tabelas de banco de dados
Base.metadata.create_all(bind=engine) # serve para criar todas as tabelas no banco de dados com base nos modelos 

#aqui é o aplicativo FAST API E CRIADO(nome,versão da api e a descrição para documentação))
app = FastAPI(
    title="Sistema de Gestão",
    version="1.0.0",
    description="API para gestão de clientes, produtos e pedidos"
)

# CORS são políticas de segurança que permitem ou restringem recursos solicitados em uma página web de outro domínio fora do domínio ao qual o recurso pertence.
# Configurar middleware CORS
# permite que qualquer origem acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Registrar routers
# incluir o roteador de clientes na aplicação principal
app.include_router(cliente_router)




@app.get("/")
def root():
    return {
        "message": "API de Gestão desenvolvido por GEORGE COM FOCO EM ESTUDOS DE BACK-END",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
