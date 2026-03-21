
CREATE TABLE Region (
    Code_dep_code_commune TEXT NOT NULL,
    reg_code INTEGER NOT NULL,
    reg_nom TEXT NOT NULL,
    aca_nom TEXT NOT NULL,
    dep_nom TEXT NOT NULL,
    com_nom_maj_court TEXT NOT NULL,
    dep_code TEXT NOT NULL,
    dep_nom_num TEXT NOT NULL,
    PRIMARY KEY (Code_dep_code_commune)
);

CREATE TABLE Contrat (
    Contrat_ID INTEGER NOT NULL,
    No_voie INTEGER,
    B_T_Q TEXT,
    Type_de_voie TEXT,
    Voie TEXT,
    Code_dep_code_commune TEXT NOT NULL,
    Code_postal INTEGER NOT NULL,
    Surface INTEGER,
    Type_local TEXT NOT NULL,
    Occupation TEXT NOT NULL,
    Type_contrat TEXT NOT NULL,
    Formule TEXT NOT NULL,
    Valeur_declaree_biens TEXT NOT NULL,
    Prix_cotisation_mensuel INTEGER NOT NULL,
    PRIMARY KEY (Contrat_ID),
    FOREIGN KEY (Code_dep_code_commune)
        REFERENCES Region (Code_dep_code_commune)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);
