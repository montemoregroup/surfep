# -*- coding: utf-8 -*-


import streamlit as st
from PIL import Image

from ase.io import read, write
import numpy as np
from ase.visualize import view
import copy
import matplotlib.pyplot as plt
#from ase.io import write


#import surfEP
import sys
# sys.path.append("../algorithms")
from ..algorithms.surfEP import surfEP

from ..functions.table import mask_equal
from ..functions.col import pdb_code_col
from ..functions.path import pages_str, data_str, get_file_path,get_dir_name,util_str
from ..functions.gui import load_st_table, write_st_end, create_st_button, show_st_structure, get_neighbor_path, show_st_fig


def general_surfEP():

    left_col, right_col = st.columns(2)

    df = load_st_table(__file__)


    img_1 = Image.open(
        get_file_path(
            "web_image.png",
            dir_path=get_neighbor_path(__file__, pages_str, data_str),
        )
    )

    left_col.image(img_1, output_format="PNG")
    # show_st_structure(mask_equal(df, pdb_code_col, "6oim"),
    #         zoom=1.2,
    #         width=400,
    #         height=300,
    #         cartoon_trans=0,
    #         surface_trans=1,
    #         spin_on=True,
    #         st_col=left_col)

    right_col.markdown("# SurfEp")
    right_col.markdown("### A tool for predicting alloy energetics")
    right_col.markdown("**Created by the Montemore group**")
    #right_col.markdown("**The Montemore group**")

    group_link_dict = {
        "Group's website": "https://www.montemoregroup.org/",
        "Repository": "https://bitbucket.org/mmmontemore/surfep/src/master/",
        
    }

    st.sidebar.markdown("## The Montemore Group")
    for link_text, link_url in group_link_dict.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    paper_link_dict = {
        "SurfEP paper": "https://pubs.rsc.org/en/content/articlelanding/2020/cy/d0cy00682c",
        "Latent-variable SurfEP paper": "",
        "ECFP paper": "https://iopscience.iop.org/article/10.1088/2515-7655/aca122",
    }

    st.sidebar.markdown("## Research papers")
    for link_text, link_url in paper_link_dict.items():
        create_st_button(link_text, link_url, st_col=st.sidebar)

    # software_link_dict = {
    #     "BioPython": "https://biopython.org",
    #     "RDKit": "https://www.rdkit.org",
    #     "PDBrenum": "http://dunbrack.fccc.edu/PDBrenum/",
    #     "Fpocket": "https://bioserv.rpbs.univ-paris-diderot.fr/services/fpocket/",
    #     "PyMOL": "https://pymol.org/2/",
    #     "3Dmol": "https://3dmol.csb.pitt.edu",
    #     "Pandas": "https://pandas.pydata.org",
    #     "NumPy": "https://numpy.org",
    #     "SciPy": "https://scipy.org",
    #     "Sklearn": "https://scikit-learn.org/stable/",
    #     "Matplotlib": "https://matplotlib.org",
    #     "Seaborn": "https://seaborn.pydata.org",
    #     "Streamlit": "https://streamlit.io",
    # }

    # st.sidebar.markdown("## Software-Related Links")
    # link_1_col, link_2_col, link_3_col = st.sidebar.columns(3)

    # i = 0
    # link_col_dict = {0: link_1_col, 1: link_2_col, 2: link_3_col}
    # for link_text, link_url in software_link_dict.items():

    #     st_col = link_col_dict[i]
    #     i += 1
    #     if i == len(link_col_dict.keys()):
    #         i = 0

    #     create_st_button(link_text, link_url, st_col=st_col)

    st.markdown("---")

    st.markdown(
        """
        ### SurfEP
        SurfEP is organized as a class, which is initialized by calling surfEP(). There are optional arguments for the locations of the files that give the model parameters. Once a class object has been created, the primary function is atomsToAds(), which takes a list of atoms objects for the surfaces, a list of adsorbates, the site type, a list of the site indices (a list of lists, where each sublist contains the indices of a site), and a list of surface indices (the indices of all of the atoms in the surface). 

        - Possible host metals: ['Cu','Ag','Au','Ni','Pt','Pd','Co','Rh','Ir','Ru','Os','Re','Ti','Zr','Hf','Sc']
        - Possible dopant metals: ['Cu','Ag','Au','Ni','Pt','Pd','Co','Rh','Ir','Fe','Ru','Os','Mn','Re','Cr','Mo','W','V','Ta','Ti','Zr','Hf','Sc']
        - Possible adsorbates: ['C', 'N', 'O', 'OH', 'H', 'S', 'K', 'F']
        - Possible siteTypes: ['Top','Bridge','Hollow']
        - Not all siteTypes may be available for all species.
        - Other limitations: Currently, only bimetallic fcc(111) and hcp(0001) surfaces are supported, and each surface must be a pure metal in the bulk but can be doped with other atoms in the top two layers. Other geometries and architectures may run, but the predictions are unlikely to be reliable. Further, if the surface dramatically reconstructs or the adsorbate relaxes out of site, the predictions are unlikely to be reliable. The surfaceIndicesList must be sequential and start at 0 (hence, the first few atoms in the atoms object must be in the top layer of the slab).
        
        """
    )

    left_col, right_col = st.columns(2)

    

    left_col.markdown(
        """
        ### How does it work ?

        Complete all the parameters and the machine learning model will predict the adsorption energy of your chosen alloy

        """
    )
    img_1 = Image.open(
        get_file_path(
            "gen_screen.png",
            dir_path=get_neighbor_path(__file__, pages_str, data_str),
        )
    )

    left_col.image(img_1, output_format="PNG")

    with right_col:
        hostMetal=st.selectbox("Choose host metal",
                            ('Cu','Ag','Au','Ni','Pt','Pd','Co','Rh','Ir','Ru','Os','Re','Ti','Zr','Hf','Sc'))
        dopingMetal=st.selectbox("Select doping metal(s)",
                                    ('Cu','Ag','Au','Ni','Pt','Pd','Co','Rh','Ir','Fe','Ru','Os','Mn','Re','Cr','Mo','W','V','Ta','Ti','Zr','Hf','Sc'))
        adsorbate=st.selectbox("Choose host adsorbate",
                                ('C', 'N', 'O', 'OH', 'H', 'S', 'K', 'F'))
        dopingLocations=st.multiselect("Select doping locations",
                                       (i for i in range(18)))
        siteType=st.selectbox("Choose adsorbing site", 
                              ('Top','Bridge','Hollow'))
        adsorptionSite_dict=st.multiselect("Select adsorbing sites indices",
                                       (i for i in range(9)))
        surfaceIndicesList = [[0,1,2,3,4,5,6,7,8]]

        ### Set up and view structure
        # Import host metal structure
        from pathlib import Path
        par_dir=Path(__file__).parent.parent
        json_path=get_file_path("datas/JSONFiles/",
                dir_path=str(par_dir)#f"{get_dir_name(__file__)}/{util_str}",
                )
        element_path=get_file_path("datas/",
                dir_path=str(par_dir)#f"{get_dir_name(__file__)}/{util_str}",
                )
        if st.button('Predict'):

            slab = read(par_dir.joinpath('./datas/HostStructures/POSCAR_'+hostMetal))
            # Dope in metal
            symbols = np.array(slab.get_chemical_symbols())
            symbols[dopingLocations] = dopingMetal
            slab.set_chemical_symbols(symbols)

            adsorptionSite=list(adsorptionSite_dict)

            adsPredictor = surfEP(verbose=False,jsonDirectory =json_path,elementDataDirectory=element_path)
            try:
                predAdsList = adsPredictor.atomsToAds([slab] ,[adsorbate],siteType,[adsorptionSite], surfaceIndicesList)
            except KeyError:
                st.write(':red[This current version of SurfEp cannot predict ' + adsorbate + ' at the ' + siteType + ' site. Try another adsorbate and/or site]') 
                raise SystemExit
            try:
                st.write('Predicted adsorption energy (eV):', predAdsList[0][0][0])
                
            except IndexError:
                st.write(':red[Enter doping locations and/or adsorption site locations]') 
                raise SystemExit

            write(str(Path(__file__).parent) + '/del.png', slab)
            img_3 = Image.open(
            get_file_path(
            "del.png",
            dir_path=str(Path(__file__).parent),
            ))

            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            left_col.image(img_3, output_format="PNG")
        
    
    st.markdown("---")

    # left_info_col, right_info_col = st.columns(2)

    # left_info_col.markdown(
    #     f"""
    #     The current version of this package is an early release. While it has been tested, it may have unexpected behavior in some situations.

    #     If comparing to your own DFT data, we suggest you do a linear fit between SurfEP predictions and your data, for the particular subset of alloys and adsorbate you're interested in.

    #     ### Authors
    #     Please feel free to contact us with any issues, comments, or questions.

    #     ##### Mattew montemore 

    #     - Email:  <mmontemore@tulane.edu> 
       

    #     ##### Gbolade Kayode
    #     """,
    #     unsafe_allow_html=True,
    # )


    write_st_end()
