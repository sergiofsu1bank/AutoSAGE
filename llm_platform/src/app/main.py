"""
MAIN OFFLINE (SEM API)

Fluxo:

1) Persistência:
   - Cria agente (se não existir)
   - Cria pipeline (se não existir)
   - Cria versão ativa (se não existir)
   - Cria node n1 (se não existir)
   - Ingere base de conhecimento

2) Execução:
   - Carrega agentes do banco
   - Executa pipeline simples
   - Se use_rag=True → Engine usa RAG automaticamente
"""

from dotenv import load_dotenv
load_dotenv()

# ==================================================
# Infraestrutura
# ==================================================

from src.db.base import Base
from src.db.session import engine, SessionLocal
from src.db.agent_repository import AgentRepository
from src.db.pipeline_repository import PipelineRepository

# ==================================================
# Aplicação
# ==================================================

from src.app.agents.registry import AgentRegistry
from src.app.llm.openai_adapter import OpenAIAdapter
from src.app.rag.service import RAGService

from src.app.orchestration.engine import ExecutionEngine
from src.app.orchestration.contracts import (
    PipelineDefinition,
    PipelineNode,
)
from src.app.orchestration.pipeline_loader import PipelineLoader


# Garante que tabelas existem
Base.metadata.create_all(bind=engine)


# ==================================================
# 1️⃣ FASE DE PERSISTÊNCIA
# ==================================================

def persist_phase(pipeline_name: str) -> None:

    db = SessionLocal()

    agent_repo = AgentRepository(db)
    pipeline_repo = PipelineRepository(db)

    # ============================================
    # AGENT
    # ============================================

    existing_agent = agent_repo.get_by_name("analista")

    if existing_agent:
        agent = existing_agent
        print(f"Agente já existente. ID: {agent.id}")
    else:
        agent = agent_repo.create(
            name="analista",
            role="Analisa textos criticamente",
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=500,
            use_rag=True,
        )
        print(f"Novo agente criado. ID: {agent.id}")

    # IMPORTANTE: capture antes de fechar sessão
    agent_id = agent.id

    # ============================================
    # PIPELINE
    # ============================================

    pipeline = pipeline_repo.get_pipeline_by_name(pipeline_name)

    if not pipeline:
        pipeline = pipeline_repo.create_pipeline(pipeline_name)
        print(f"Pipeline criado: {pipeline.name}")
    else:
        print(f"Pipeline já existente: {pipeline.name}")

    # ============================================
    # VERSION
    # ============================================
    version = pipeline_repo.get_active_version(pipeline.id)

    if not version:
        version = pipeline_repo.create_new_version(
            pipeline_id=pipeline.id,
            activate=True,
        )
        print(f"Pipeline version {version.version_number} criada.")
    else:
        print("Pipeline version já existente.")

    # ============================================
    # NODE
    # ============================================
    existing_nodes = {node.node_id for node in pipeline_repo.list_nodes(version.id)}

    if "n1" not in existing_nodes:
        pipeline_repo.add_node(
            pipeline_version_id=version.id,
            node_id="n1",
            agent_id=agent.id,
        )

    if "n2" not in existing_nodes:
        pipeline_repo.add_node(
            pipeline_version_id=version.id,
            node_id="n2",
            agent_id=agent.id,
        )

    existing_edges = pipeline_repo.list_edges(version.id)

    if not existing_edges:
        pipeline_repo.add_edge(
            pipeline_version_id=version.id,
            source_node_id="n1",
            target_node_id="n2",
            condition_json={
                "type": "expression",
                "expression": "len(output) > 300"
            },
        )

    print("Nodes e edge verificados.")

    db.close()

    # ============================================
    # RAG INGESTION
    # ============================================

    rag_service = RAGService()

    rag_service.ingest(
        agent_id=agent_id,
        content="A empresa Orion utiliza IA generativa exclusivamente para automação de contratos jurídicos internos.",
        source="bootstrap_manual",
    )

    print("Persistência concluída.")


# ==================================================
# 2️⃣ FASE DE EXECUÇÃO
# ==================================================

def execute_phase() -> None:
    print("=== EXECUTION START ===")

    registry = AgentRegistry()
    registry.load_from_database()

    loader = PipelineLoader()
    pipeline = loader.load("pipeline_analise_orion")

    if not pipeline:
        raise ValueError("Pipeline não encontrado.")

    engine = ExecutionEngine(
        registry=registry,
        llm_adapter=OpenAIAdapter(),
        rag_service=RAGService(),
    )

    context = engine.run(
        pipeline=pipeline,
        initial_input="Para que a empresa Orion utiliza IA generativa?",
    )

    print("\n=== RESULT ===")

    for node_id, output in context.outputs_by_node.items():
        print(f"\nNODE: {node_id}")
        print(output)

# ==================================================
# MAIN
# ==================================================

def main() -> None:
    print("\n=== BOOTSTRAP ===")
    pipeline_name = "pipeline_analise_orion"
    persist_phase(pipeline_name=pipeline_name)
    execute_phase()

if __name__ == "__main__":
    main()
