import pandas as pd

water_df = pd.read_csv('drinking_water.csv')
hygiene_df = pd.read_csv('hygiene.csv')
# print(hygiene_df)
# print(water_df)

import plotly.express as px

# print(water_df['Region'].unique())


# Load data into a Pandas DataFrame
# df = pd.read_csv('your_data.csv')

# # Create a Plotly figure
# fig = px.line(water_df, x='Year', y='Coverage')
#
# # Add a dropdown menu to select different features
# features = water_df.columns[2:] # get all column names starting from the third column
# fig.update_layout(
#     updatemenus=[dict(
#         buttons=[dict(label=feat, method='update', args=[{'y':[water_df[feat]], 'x':[water_df['Year']]}]) for feat in features],
#         direction='down',
#         showactive=True,
#         xanchor='left',
#         yanchor='top',
#         x=0.5,
#         y=1.2
#     )]
# )
#
# # Display the figure
# fig.show()

water_df = water_df.loc[water_df["Service level"] == "Basic service"]
water_df = water_df.loc[water_df["Residence Type"] == "total"]

# Create the dropdown menu
fig = px.line(water_df, x="Year", y="Coverage", color="Region", range_x=[water_df["Year"].min(), water_df["Year"].max()],
              range_slider=dict(visible=True),
              title="Interactive Plotly Line Plot",
              labels={"Year": "Year", "Coverage": "Coverage of Basic Drinking Water Service", "Region": "Region"},
              hover_data={"Service level": "Basic Service", "Residence Type": "Total(rural and urban)"},
              template="simple_white",
              color_discrete_sequence=px.colors.qualitative.Safe)

# Add the dropdown menu to select region
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True]},
                           {"title": "All Regions"}]),
                dict(label="Africa",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False]},
                           {"title": "Africa"}]),
                dict(label="Americas",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False]},
                           {"title": "Americas"}]),
                dict(label="Eastern Mediterranean",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False]},
                           {"title": "Eastern Mediterranean"}]),
                dict(label="Europe",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False]},
                           {"title": "Europe"}]),
                # dict(label="South-East Asia",
                #      method="update",
                #      args=[{"visible": [False, False, False, False, True, False]},
                #            {"title": "South-East Asia"}]),
                # dict(label="Western Pacific",
                #      method="update",
                #      args=[{"visible": [False, False, False, False, False, True]},
                #            {"title": "Western Pacific"}])
            ]),
            x=0.1,
            y=1.15
        )
    ])

# Show the plot
fig.show()