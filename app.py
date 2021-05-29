import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

IMGCHELSEA = 'chelsea-fc-logo.png'
IMGCITY = 'manchester-city-logo.png'
IMGUEFA = 'uefa.png'
LABELS = ['Chelsea', 'Man. city']
COLOR = ['b','g']
STATS2021 = 'Data/ChampionsLeague2021Stats.csv'

widths = 0.15
images = {'Chelsea': IMGCHELSEA, 'Man. City': IMGCITY}
stats_df = pd.read_csv(STATS2021, index_col=0)
stats_df = stats_df.set_index(['Team'])
goals_df = stats_df[['Total goals','Total goals against','Goal difference']]
goaltype_df = stats_df[['Left foot', 'Right foot', 'Header', 'Inside area', 'Outside area', 'Penalties']]
attempts_df = stats_df[['Total attempts',	'Average per game'	, 'Attempts on target',	'Attempts off target',	'Attempts blocked',	'Attempts against woodwork'	]]
passes_df = stats_df[['PA',	'PC', 'PC %',	'Average ball possession (%)',	'Average ball possession (time)']]


######## Datasets



# Permite definir que la función este en cache.

@st.cache
def run_fxn(n: int) -> list:
    return range(n)

def barplot(subh, dataframe,colnum):
    st.write(subh)
    heights = dataframe.iloc[:,colnum]

    fig, ax = plt.subplots(figsize=(4.2 , 3))
    ax.bar(LABELS, height=heights, tick_label=LABELS, width=widths, color=COLOR)
    for i, v in enumerate(heights):
        ax.text(i-0.025, 
              v/heights[i], 
              heights[i], 
              fontsize=12, 
              )
    plt.tight_layout()
    st.pyplot(fig)

    

def main():
    """Generación de la webapp con streamlit"""

    ###Config
    st.set_page_config(layout="wide")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Definir título
    
    st.title("Uefa Champions League")   

    info = st.selectbox(
        "Seleccione la información a mostrar", ["Historia", "Final 2021"]
    )

    if info == 'Historia':
        st.write('Historia')
    else:
        st.header('Final Uefa Champions League 2021')

        

        #####Show dataframe
        st.write("Dataframe")
        st.dataframe(stats_df)

        #####Match
        st.subheader('Información sobre partidos')


        team = st.selectbox(
        "Seleccione el equipo", ["Chelsea", "Man. City"]
        )
        
        index = 0
        if team == 'Chelsea':index=0
        else: index = 1

        matches_df = stats_df.iloc[:,:4]
        colnames = matches_df.columns
        rows = matches_df.loc[team,:]
        col1, col2, col3, col4, col5 = st.beta_columns(5)

        with col1:
            st.write(colnames[0])
            st.write(rows[colnames[0]])

        with col2:
            st.write(colnames[1])
            st.write(rows[colnames[1]])

        with col3:
            st.write(colnames[2])
            st.write(rows[colnames[2]])

        with col4:
            st.write(colnames[3])
            st.write(rows[colnames[3]])
        with col5:
            st.image(images[team], width=125)

        
        #####Goals
        st.subheader('Goles')

        colnames = goals_df.columns
        rows = goals_df.loc[team,:]
        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.write(colnames[0])
            st.write(rows[colnames[0]])

        with col2:
            st.write(colnames[1])
            st.write(rows[colnames[1]])

        with col3:
            st.write(colnames[2])
            st.write(rows[colnames[2]])

        st.write("")
        #################################################################
        show_goals_comparative = st.checkbox('Mostrar comparativa de goles')
        if show_goals_comparative:

            col1, col2 = st.beta_columns(2)

            with col1:
                st.write('Goles')
                goal_axes = goals_df.plot.barh(rot=0, subplots=True, figsize=(8,8))
                #plt.tight_layout()  
                st.pyplot()


            with col2:
                st.write('Tipo de goles')
                axes = goaltype_df.plot.barh(rot=0, subplots=True, figsize=(10,12))
                st.pyplot()

        st.subheader('Intentos de gol')
        st.write(attempts_df.iloc[index,0])



        if st.button("Mostrar comparativa"):
            axes = attempts_df.iloc[:,1:].plot.barh(rot=0, subplots=True, figsize=(10,12))
            st.pyplot()

        else:
            st.text("")

        st.subheader('Pases')

        col1, col2, col3 = st.beta_columns(3)


        cols =  passes_df.columns
        passes_team = passes_df.loc[team,:]
        passes_complete = passes_team[cols[2]]
        passes_labels = ['Pases completos', 'Pases incompletos']
        sizes = [int(passes_complete[0:2]), 100 - int(passes_complete[0:2])]
        explode = (0,0.1)


        with col1:
            st.write('Intentos de pase', passes_team[cols[0]])
            st.write('Pases completos', passes_team[cols[1]])
            st.write('Pases incompletos', passes_team[cols[0]] - passes_team[cols[1]])

        with col2:

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=passes_labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot()




if __name__ == "__main__":
    main()