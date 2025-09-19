# models/projet.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

@dataclass
class ProjetIA:
    nom: str
    description: str
    type_modele: str  # 'NLP', 'Computer Vision', 'ML', 'Deep Learning'
    hyperparametres: Optional[Dict[str, Any]] = field(default_factory=dict)
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
            "statut": self.statut,
            "hyperparametres": self.hyperparametres
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
            hyperparametres=data.get('hyperparametres', {}),
            created_by=data.get('created_by'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def ajouter_hyperparametre(self, nom: str, valeur: Any):
        """Ajouter un hyperparamètre au projet"""
        if self.hyperparametres is None:
            self.hyperparametres = {}
        self.hyperparametres[nom] = valeur
    
    def get_hyperparametre(self, nom: str, default=None):
        """Récupérer un hyperparamètre spécifique"""
        if self.hyperparametres:
            return self.hyperparametres.get(nom, default)
        return default
    
    def supprimer_hyperparametre(self, nom: str):
        """Supprimer un hyperparamètre"""
        if self.hyperparametres and nom in self.hyperparametres:
            del self.hyperparametres[nom]
    
    def get_info_courte(self) -> str:
        """Résumé du projet pour l'affichage"""
        return f"{self.nom} ({self.type_modele}) - {self.statut}"
    
    def est_termine(self) -> bool:
        """Vérifier si le projet est terminé"""
        return self.statut.lower() in ['termine', 'completed', 'fini']