from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import uuid

@dataclass
class ProjetIA:
    nom: str
    description: str
    type_modele: str
    id: Optional[str] = None
    statut: str = "en_cours"
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire pour Supabase"""
        return {
            "nom": self.nom,
            "description": self.description,
            "type_modele": self.type_modele,
            "statut": self.statut
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProjetIA':
        """Création depuis un dictionnaire Supabase"""
        return cls(
            id=data.get('id'),
            nom=data['nom'],
            description=data['description'],
            type_modele=data['type_modele'],
            statut=data.get('statut', 'en_cours'),
            created_by=data.get('created_by'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )