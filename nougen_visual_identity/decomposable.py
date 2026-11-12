"""
NouGen Multimodal Visual Identity Capsule Specification (v2.1)
Universal, multi-tenant, decomposable identity and inheritance models.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import hashlib
import json

@dataclass(frozen=True)
class MutationPolicy:
    """Explicit permission space for property changes. 0.0 = immutable, 1.0 = full freedom."""
    face_geometry: float = 0.00
    skin_identity: float = 0.00
    persistent_marks: float = 0.00
    body_proportions: float = 0.05
    hair_arrangement: float = 0.20
    expression: float = 0.40
    wardrobe: float = 0.70
    pose: float = 1.00
    environment: float = 1.00

@dataclass
class IdentityRoot:
    """The immutable root: 'Who is this entity?'"""
    character_id: str
    canonical_name: str
    tenant_id: str = "global"
    face_embedding: Optional[List[float]] = None
    face_geometry: Dict[str, Any] = field(default_factory=dict)
    persistent_marks: List[Dict[str, Any]] = field(default_factory=list)
    base_hair: Dict[str, Any] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)
    mutation_policy: MutationPolicy = field(default_factory=MutationPolicy)

@dataclass
class IdentityVariant:
    """Causal, temporal, or route branch inheriting from IdentityRoot."""
    variant_id: str
    parent_id: str
    timeline_state: Optional[str] = None  # e.g., "vol_1", "2155"
    route_state: Optional[str] = None     # e.g., "prime", "sdx", "x2"
    scene_state: Optional[str] = None     # e.g., "level_9_combat"
    age_delta: Dict[str, Any] = field(default_factory=dict)
    hair_delta: Dict[str, Any] = field(default_factory=dict)
    mark_delta: Dict[str, Any] = field(default_factory=dict)
    body_delta: Dict[str, Any] = field(default_factory=dict)
    wardrobe_delta: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class FrozenCharacterContract:
    """Immutable contract frozen for a single render transaction."""
    transaction_id: str
    character_id: str
    variant_id: str
    canon_revision: int
    contract_hash: str
    resolved_phenotype: Dict[str, Any]
    resolved_presentation: Dict[str, Any]
    mutation_policy: Dict[str, float]
    canonical_references: List[Dict[str, Any]]
    negative_constraints: List[str]
    fidelity_level: int = 5  # F0 to F5

    def to_dict(self) -> Dict[str, Any]:
        return json.loads(json.dumps(self, default=lambda o: getattr(o, "__dict__", str(o))))
