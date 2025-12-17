::: mermaid
graph LR
    subgraph "Système de Gestion RH Django"
        subgraph cluster_auth [
            Authentification
            ]
            A1[Se connecter]
            A2[Se déconnecter]
            A3[Changer mot de passe]
            A4[Réinitialiser mot de passe]
        end
        

        subgraph cluster_users [
            Gestion Utilisateurs
            ]
            U1[Créer un utilisateur]
            U2[Modifier profil utilisateur]
            U3[Consulter liste utilisateurs]
            U4[Supprimer utilisateur]
        end
        
        subgraph cluster_employees [
            Gestion Employés
            ]
            E1[Créer un employé]
            E2[Consulter profil employé]
            E3[Modifier information employé]
            E4[Consulter liste employés]
        end
        

        subgraph cluster_attendance [
            Pointage des Présences
            ]
            P1[Pointer son arrivée]
            P2[Pointer son départ]
        end
        
        %% ============ CONGÉS ============
        subgraph cluster_conges [
            Gestion des Congés
            ]
            C1[Demander un congé]
            C5[Approuver/Refuser congé]
        end
        
        %% ============ ABSENCES ============
        subgraph cluster_absences [
            Gestion des Absences
            ]
            AB1[Enregistrement automatique des Abcences ]
        end
        
        %% ============ PAIE ============
        subgraph cluster_paie [
            Gestion de la Paie
            ]
            PA2[Gérer les salaires employés]
            PA3[Générer fiche de paie]
            PA4[Consulter fiches de paie]
            PA5[Ajouter un bonus]
        end
        
        %% ============ ÉVALUATIONS ============
        subgraph cluster_evaluations [
            Évaluation de performances
            ]
            EV1[Évaluer un employé]
            EV2[Consulter notes employés]
            EV3[Évaluer un département]
            EV4[Consulter notes départements]
            EV5[Exporter évaluations]
        end
        
        %% ============ DÉPARTEMENTS ============
        subgraph cluster_departments [
            Gestion Départements
            ]
            D1[Créer un département]
            D2[Modifier département]
            D3[Consulter liste départements]
            D4[Voir employés par département]
        end
        
        %% ============ RECRUTEMENT ============
        subgraph cluster_recruitment [
            Gestion Recrutement
            ]
            R1[Publier une offre]
            R2[Modifier une offre]
            R3[Consulter offres actives]
            R4[Postuler à une offre]
            R5[Consulter candidatures]
            R6[Gerer candidature]
            R7[Télécharger CV candidat]
        end
    end
    
    %% ============ ACTEURS PRINCIPAUX ============
    EMPLOYÉ[Utilisateur] --> A1
    EMPLOYÉ --> A2
    EMPLOYÉ --> A3
    EMPLOYÉ --> P1
    EMPLOYÉ --> P2
    EMPLOYÉ --> C1
    %% EMPLOYÉ --> PA4
    EMPLOYÉ -->  cluster_departments
    EMPLOYÉ --> cluster_evaluations
    EMPLOYÉ --> cluster_employees
    EMPLOYÉ --> cluster_recruitment
    EMPLOYÉ --> cluster_paie
    CANDIDAT[Candidat Externe] --> R4
    ADMIN --> U4
    ADMIN --> A4
    ADMIN --> EMPLOYÉ
    cluster_attendance --> cluster_absences
    %% ============ RELATIONS INCLUDE ============
    %% PA3 -->|<<include>>| PA2
    %% R5 -->|<<include>>| R1
    %% R6 -->|<<include>>| R5
    
    %% ============ RELATIONS EXTEND ============
    R4 -.->|<<extend>> si accepté| U1 --> |Ajouter profil employee| E1
    
    %% ============ PERMISSIONS SPÉCIFIQUES ============
    subgraph "Permissions Django"
        PERM1[Donner une permission]
        PERM2[Retirer une permission]
    end
    
    %% ============ ASSOCIATION PERMISSIONS ============
    ADMIN --> PERM1
    ADMIN --> PERM2

    
    
    %% ============ FLUX IMPORTANTS ============
    subgraph "Flux : Demande de Congé"
        FC1[Fait une demande de Conges]
        FC2[Conges Accordés]
        FC3[System termine les conges]
    end
    
    
    %% C1 --> FC1
    EMPLOYÉ --> FC1 --> |accepter| FC2
    FC2 --> FC3
    
    subgraph "Flux : Génération Paie"
        FP1[Calcul automatique]
    end
    
    %% PA3 --> FP1
    PA2 --> FP1
    %% PA3 --> PA2
    
    %% ============ STYLES ============
    style EMPLOYÉ fill:#bbdefb
    %% style MANAGER fill:#c8e6c9
    %% style RH fill:#fff3e0
    style ADMIN fill:#ffcdd2
    style CANDIDAT fill:#e1bee7
    style cluster_auth fill:#f5f5f5
    style cluster_users fill:#e3f2fd
    style cluster_employees fill:#f3e5f5
    style cluster_attendance fill:#e8f5e8
    style cluster_conges fill:#fff3e0
    style cluster_absences fill:#ffebee
    style cluster_paie fill:#f3e5f5
    style cluster_evaluations fill:#e0f2f1
    style cluster_departments fill:#fff8e1
    style cluster_recruitment fill:#fce4ec
    
    style PERM1 fill:#ffecb3
    style PERM2 fill:#ffecb3
:::