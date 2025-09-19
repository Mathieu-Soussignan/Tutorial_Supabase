# models/dataset.py
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
    nb_lignes: Optional[int] = None
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
        if self.nb_lignes is not None:
            data["nb_lignes"] = self.nb_lignes
            
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
            nb_lignes=data.get('nb_lignes'),  # ← AJOUTÉ !
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
        formats_supportes = ['csv', 'json', 'parquet', 'xlsx', 'txt', 'zip']
        return self.format_fichier and self.format_fichier.lower() in formats_supportes
    
    def get_info_complete(self) -> str:
        """Information complète du dataset pour l'affichage"""
        info = f"{self.nom}"
        
        details = []
        
        if self.format_fichier:
            details.append(f"{self.format_fichier}")
        
        if self.taille_mb:
            details.append(f"{self.get_taille_formatee()}")
        
        if self.nb_lignes:
            details.append(f"{self.nb_lignes:,} lignes")
        
        if details:
            info += f" ({', '.join(details)})"
        
        return info
    
    def est_dataset_images(self) -> bool:
        """Détermine si c'est un dataset d'images"""
        formats_images = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'zip']  # ZIP peut contenir des images
        return self.format_fichier and self.format_fichier.lower() in formats_images
    
    def est_dataset_textuel(self) -> bool:
        """Détermine si c'est un dataset textuel"""
        formats_texte = ['csv', 'json', 'txt', 'tsv']
        return self.format_fichier and self.format_fichier.lower() in formats_texte
    
    def calculer_taille_par_ligne(self) -> Optional[float]:
        """Calcule la taille moyenne par ligne en KB"""
        if self.taille_mb and self.nb_lignes and self.nb_lignes > 0:
            taille_kb = float(self.taille_mb) * 1024
            return round(taille_kb / self.nb_lignes, 2)
        return None