CREATE TABLE public.Region (
  Code_region INTEGER NOT NULL, 
  Nom_region VARCHAR(100) NOT NULL, 
  -- Ajout d'une longueur à VARCHAR
  CONSTRAINT region_pk PRIMARY KEY (Code_region)
);
CREATE TABLE public.Departement (
  Code_departement VARCHAR(10) NOT NULL, 
  -- Ajout d'une longueur à VARCHAR
  Nom_departement VARCHAR(100) NOT NULL, 
  Code_region INTEGER NOT NULL, 
  CONSTRAINT departement_pk PRIMARY KEY (Code_departement)
);
CREATE TABLE public.Commune (
  id_codedep_codecommune VARCHAR(20) NOT NULL, 
  Nom_commune VARCHAR(100) NOT NULL, 
  -- Ajout d'une longueur à VARCHAR
  Code_departement VARCHAR(10) NOT NULL, 
  Code_commune INTEGER NOT NULL, 
  Code_postal INTEGER NOT NULL, 
  Population INTEGER, 
  CONSTRAINT commune_pk PRIMARY KEY (id_codedep_codecommune)
);
CREATE TABLE public.Bien (
  Id_bien INTEGER NOT NULL, 
  id_codedep_codecommune VARCHAR(20) NOT NULL, 
  No_voie INTEGER NOT NULL, 
  BTQ VARCHAR(1) NOT NULL, 
  Type_voie VARCHAR(4) NOT NULL, 
  Voie VARCHAR(50) NOT NULL, 
  Total_pieces INTEGER, 
  Surface_carrez REAL, 
  Surface_local INTEGER NOT NULL, 
  Type_local VARCHAR(50) NOT NULL, 
  Surface_terrain INTEGER NOT NULL, 
  CONSTRAINT id_bien_pk PRIMARY KEY (Id_bien)
);
CREATE TABLE public.Vente (
  Id_vente INTEGER NOT NULL, 
  Id_bien INTEGER NOT NULL, 
  Date DATE NOT NULL, 
  Valeur INTEGER, 
  CONSTRAINT id_vente_pk PRIMARY KEY (Id_vente)
);
-- Clés étrangères
ALTER TABLE 
  public.Departement 
ADD 
  CONSTRAINT region_departement_fk FOREIGN KEY (Code_region) REFERENCES public.Region (Code_region) ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE 
  public.Commune 
ADD 
  CONSTRAINT departement_commune_fk FOREIGN KEY (Code_departement) REFERENCES public.Departement (Code_departement) ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE 
  public.Bien 
ADD 
  CONSTRAINT commune_bien_fk FOREIGN KEY (id_codedep_codecommune) REFERENCES public.Commune (id_codedep_codecommune) ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE 
  public.Vente 
ADD 
  CONSTRAINT bien_vente_fk FOREIGN KEY (Id_bien) REFERENCES public.Bien (Id_bien) ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
