# Supplementary materials: Norm repair as an extension to the deliberative dialogue model


This GitHub contains all the supplementary materials for the article: 

*Norm repair as an extension to the deliberative dialogue model*

## Details

The github contains materials for replicating the findings in the article and any additional supplementary materials. 
It is organized around one Python notebook (Supplementary_materials_A)

There are three folders:

(1) "data": Contains all data required for replication.

(2) "model": Contains the trained topic model weights and pre-processing details.

(3) "GitHub supplementary materials" with all additional supplementary materials. 

We have also compressed both data files (model_data.zip) for easy download and access in the Python notebook.

## Analysis 2 and Analysis 3 supplementary data

The "GitHub supplementary materials" folder contains the data and replication scripts for the inter-rater reliability (Analysis 2) and good/bad faith prevalence (Analysis 3) results documented in the notebook. None of these files contain raw participant text.

- `SupplementaryMaterials_A_IRR_Analysis2_long.csv`: long-format coder data for the 26 topics x 6 deliberative norms.
- `SupplementaryMaterials_A_IRR_Analysis2_compute_irr.py`: replication script for the Krippendorff's alpha and agreement statistics.
- `SupplementaryMaterials_A_Analysis3_speaker_flags.csv`: per-moderator good/bad faith mention flags.
- `SupplementaryMaterials_A_Analysis3_term_counts.csv`: per-term turn counts for the good/bad faith dictionary.
- `SupplementaryMaterials_A_Analysis3_faith_terms.py`: replication script for the prevalence figures.

## Running the notebook

We recommend using Google Colab for running the notebook. This is because it does not require any local storage of data nor the local installation of software and packages. Instead, the notebook will be run on a virtual environment hosted by Google (deleted after the runtime is closed or ended). Running the notebook locally requires the installation of necessary packages into your local Python environment.
