"""
NouGen Character State Compiler (Compiler Engine)
Resolves canonical inheritance:
Root Identity -> Canon Amendments -> Temporal State -> Route/Branch State -> Scene Overrides -> Frozen Contract
"""
import hashlib
import json
import uuid
import time
from typing import Dict, Any, List, Optional
from .decomposable import IdentityRoot, IdentityVariant, FrozenCharacterContract, MutationPolicy

class CharacterStateCompiler:
    """Compiles decomposable character identities into frozen, hash-addressed contracts."""

    def resolve(
        self,
        root: IdentityRoot,
        variant: Optional[IdentityVariant] = None,
        amendments: Optional[List[Dict[str, Any]]] = None,
        scene_overrides: Optional[Dict[str, Any]] = None,
        canon_revision: int = 1
    ) -> FrozenCharacterContract:
        """
        Deterministic precedence pipeline:
        SceneOverride > BranchState > TemporalState > CanonAmendment > RootIdentity
        """
        # 1. Base phenotype (immutable root)
        resolved_phenotype = {
            "face_embedding": list(root.face_embedding) if root.face_embedding else [],
            "face_geometry": dict(root.face_geometry),
            "persistent_marks": list(root.persistent_marks),
            "body": dict(root.body),
        }

        # 2. Base presentation (mutable root)
        resolved_presentation = {
            "hair": dict(root.base_hair),
            "wardrobe": {},
            "expression": "neutral",
            "pose": "neutral_standing",
            "environment": "studio_neutral"
        }

        # 3. Apply valid amendments (if any)
        if amendments:
            for am in amendments:
                if am.get("target") == "phenotype":
                    resolved_phenotype.update(am.get("delta", {}))
                elif am.get("target") == "presentation":
                    resolved_presentation.update(am.get("delta", {}))

        # 4. Apply variant deltas (temporal, route, causal branch)
        variant_id = "prime"
        if variant:
            variant_id = variant.variant_id
            if variant.age_delta:
                resolved_phenotype["age_modifiers"] = variant.age_delta
            if variant.mark_delta:
                # E.g., adding or updating a route-specific scar
                resolved_phenotype["persistent_marks"].append(variant.mark_delta)
            if variant.hair_delta:
                resolved_presentation["hair"].update(variant.hair_delta)
            if variant.body_delta:
                resolved_phenotype["body"].update(variant.body_delta)
            if variant.wardrobe_delta:
                resolved_presentation["wardrobe"].update(variant.wardrobe_delta)

        # 5. Apply scene overrides (within permitted mutation boundaries)
        if scene_overrides:
            for key, val in scene_overrides.items():
                if key in ["expression", "pose", "environment", "lighting", "camera"]:
                    resolved_presentation[key] = val
                elif key in ["hair_arrangement", "wardrobe"]:
                    resolved_presentation[key] = val
                elif key in ["face_geometry", "skin_identity"]:
                    # Violation of 0.00 mutation budget unless explicit override is passed
                    if not scene_overrides.get("explicit_phenotype_override", False):
                        continue  # Silently reject illegal mutation drift
                    resolved_phenotype[key] = val

        # 6. Freeze Contract
        policy_dict = {
            "face_geometry": root.mutation_policy.face_geometry,
            "skin_identity": root.mutation_policy.skin_identity,
            "persistent_marks": root.mutation_policy.persistent_marks,
            "body_proportions": root.mutation_policy.body_proportions,
            "hair_arrangement": root.mutation_policy.hair_arrangement,
            "expression": root.mutation_policy.expression,
            "wardrobe": root.mutation_policy.wardrobe,
            "pose": root.mutation_policy.pose,
            "environment": root.mutation_policy.environment,
        }

        payload = {
            "character_id": root.character_id,
            "variant_id": variant_id,
            "canon_revision": canon_revision,
            "phenotype": resolved_phenotype,
            "presentation": resolved_presentation,
            "policy": policy_dict,
        }
        serialized = json.dumps(payload, sort_keys=True)
        contract_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        return FrozenCharacterContract(
            transaction_id=str(uuid.uuid4()),
            character_id=root.character_id,
            variant_id=variant_id,
            canon_revision=canon_revision,
            contract_hash=contract_hash,
            resolved_phenotype=resolved_phenotype,
            resolved_presentation=resolved_presentation,
            mutation_policy=policy_dict,
            canonical_references=[],
            negative_constraints=["genetic_drift", "facial_proportions_mutation"],
            fidelity_level=5
        )
