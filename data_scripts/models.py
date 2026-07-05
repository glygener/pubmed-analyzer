from pydantic import BaseModel
from typing import Optional


class Author(BaseModel):
    name: str
    affiliation_text: Optional[str] = None
    department: Optional[str] = None
    institution: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class MeshTerm(BaseModel):
    term: str
    ui: str
    major_topic: bool


class Article(BaseModel):
    pmid: str
    title: str
    pub_year: int
    pub_month: Optional[str] = None
    journal: str
    authors: list[Author]
    mesh_terms: Optional[list[MeshTerm]] = []
