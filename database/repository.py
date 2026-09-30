from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Project, KnowledgeSource


def create_project(
    name: str,
    description: str | None = None,
) -> Project:

    with SessionLocal() as session:

        project = Project(
            name=name,
            description=description,
        )

        session.add(project)
        session.commit()
        session.refresh(project)

        return project


def get_project(project_id: str) -> Project | None:

    with SessionLocal() as session:

        statement = select(Project).where(
            Project.id == project_id
        )

        return session.scalar(statement)


def get_projects() -> list[Project]:

    with SessionLocal() as session:

        statement = select(Project).order_by(
            Project.created_at.desc()
        )

        return list(session.scalars(statement).all())


def create_knowledge_source(
    project_id: str,
    name: str,
    source_type: str,
    storage_path: str,
    mime_type: str,
    file_size: int,
    source_id: str,
) -> KnowledgeSource:

    with SessionLocal() as session:

        project = session.get(Project, project_id)

        if project is None:
            raise ValueError(
                f"Project '{project_id}' does not exist."
            )

        source = KnowledgeSource(
            id=source_id,
    project_id=project_id,
            name=name,
            source_type=source_type,
            storage_path=storage_path,
            mime_type=mime_type,
            file_size=file_size,
        )

        session.add(source)
        session.commit()
        session.refresh(source)

        return source

def get_project_knowledge_sources(
    project_id: str,
) -> list[KnowledgeSource]:

    with SessionLocal() as session:

        statement = (
            select(KnowledgeSource)
            .where(KnowledgeSource.project_id == project_id)
            .order_by(KnowledgeSource.created_at.desc())
        )

        return list(session.scalars(statement).all())    