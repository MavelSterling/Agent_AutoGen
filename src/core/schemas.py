from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Requirements(BaseModel):
    project_name: str = Field(default="Arquitecto de Solucion")
    domain: str = Field(default="Cloud/AI")
    cloud_provider: Optional[str] = None
    functional_requirements: List[str] = Field(default_factory=list)
    non_functional_requirements: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    data_sources: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    traffic_profile: Optional[str] = None
    regions: List[str] = Field(default_factory=list)
    compliance: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class Component(BaseModel):
    name: str
    purpose: str
    inputs: List[str]
    outputs: List[str]
    dependencies: List[str]
    security_considerations: List[str]


class Flow(BaseModel):
    name: str
    steps: List[str]
    error_handling: List[str]
    timeouts: List[str]
    idempotency: List[str]
    fallback: List[str]
    happy_path: List[str]


class ADR(BaseModel):
    id: str
    title: str
    context: str
    options: List[str]
    decision: str
    consequences: List[str]


class BacklogItem(BaseModel):
    id: str
    epic: str
    story: str
    priority: str
    acceptance_criteria: List[str]
    definition_of_done: List[str]


class Risk(BaseModel):
    id: str
    description: str
    impact: str
    mitigation: str
    assumptions: List[str]


class CostEstimate(BaseModel):
    range_low: str
    range_mid: str
    range_high: str
    drivers: List[str]
    volume_assumptions: List[str]


class SolutionProposal(BaseModel):
    diagram_mermaid: str
    components: List[Component]
    flows: List[Flow]
    adrs: List[ADR]
    backlog: List[BacklogItem]
    risks: List[Risk]
    cost_estimate: CostEstimate
