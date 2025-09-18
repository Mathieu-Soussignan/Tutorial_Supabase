from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Dataset:
    nom: str
    projet_id: str
    fichier_url: Optional[str] = None
    taille_mb: Optional[Decimal] = None
    format_fichier: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Conversion en dictionnaire pour Supabase"""
        data = {
            "nom": self.nom,
            "projet_id": self.projet_id
        }
        
        # Ajouter les champs optionnels seulement s'ils existent
        if self.fichier_url:
            data["fichier_url"] = self.fichier_url
        if self.taille_mb:
            data["taille_mb"] = float(self.taille_mb)
        if self.format_fichier:
            data["format_fichier"] = self.format_fichier
            
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Dataset':
        """Création depuis un dictionnaire Supabase"""
        return cls(
            id=data.get('id'),
            nom=data['nom'],
            projet_id=data['projet_id'],
            fichier_url=data.get('fichier_url'),
            taille_mb=Decimal(str(data['taille_mb'])) if data.get('taille_mb') else None,
            format_fichier=data.get('format_fichier'),
            created_at=data.get('created_at')
        )
    
    def get_taille_formatee(self) -> str:
        """Retourne la taille formatée (ex: '125.5 MB')"""
        if self.taille_mb:
            if self.taille_mb >= 1024:
                return f"{self.taille_mb/1024:.1f} GB"
            else:
                return f"{self.taille_mb:.1f} MB"
        return "Taille inconnue"
    
    def est_gros_fichier(self, seuil_mb: float = 100.0) -> bool:
        """Vérifie si le dataset est considéré comme gros"""
        return self.taille_mb and self.taille_mb > seuil_mb
    
    def get_extension_fichier(self) -> Optional[str]:
        """Extrait l'extension du fichier depuis l'URL"""
        if self.fichier_url:
            return self.fichier_url.split('.')[-1].lower()
        return None
    
    def valider_format(self) -> bool:
        """Valide si le format du fichier est supporté"""
        formats_supportes = ['csv', 'json', 'parquet', 'xlsx', 'txt']
        return self.format_fichier and self.format_fichier.lower() in formats_supportes