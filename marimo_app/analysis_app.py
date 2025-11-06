import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    return mo, pd, plt


@app.cell
def _(mo):
    mo.md(
        """
    #🐟Fish Stocking Data Analysis🎣.
    ## Looking at stocking reports provided by the Michigan Department of Natural Resources to see how efforts have changed overtime from 2000 - 2025.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # **The questions we are going to answer with this analysis are:** 
    1. ### what is the top 10 and bottom 10 fish species stocked from 2000 to 2025?
    1. ### How has fish stocking changed over the years?
    1. ### What is the average amount of fish stocked yearly, Semi decadelly, and decadelly?
    1. ### What fish species has seen an increase in stocking efforts and which have seen a decline?
      - ### Has salmon, trout, and steelhead stocking efforts decreased or increased since 2000?
    1. ### What time of year (month) does stocking usually take place? How many times a year? 
    1. ### Which counties see the most effort in stocking? Which ones see significantly less efforts? 
    1. ### What water bodies have the lowest number of stocking efforts? What water bodies have the highest stocking efforts?
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # **📊 Start of our EDA 🔎 :**
    ## Loading the dataset and checking **first 5 rows of the data**.
    """
    )
    return


@app.cell
def _(pd):
    # load the raw csv
    df_raw = pd.read_csv('../data/fish_stocking_data.csv')
    df_raw.head()
    return (df_raw,)


@app.cell
def _(mo):
    mo.md(r"""# Checking for missing values""")
    return


@app.cell
def _(df_raw, pd):
    # missing vs non missing values count
    missing_summary = pd.DataFrame({
        "missing count": df_raw.isnull().sum(),
        "non_missing_count": df_raw.notnull().sum(),
        "total_rows": len(df_raw),
        "missing_%": round(df_raw.isnull().mean() *100, 2)
    })
    missing_summary.sort_values(by="missing_%", ascending=False)
    return


@app.cell
def _(df_raw):
    # Checking row values to better understand the dataset
    print('Range sample values:')
    print(df_raw['Range'].dropna().unique()[:10])

    print("\nStrain sample values:")
    print(df_raw['Strain'].dropna().unique()[:10])

    print("\nTown sample values:")
    print(df_raw['Town'].dropna().unique()[:10])

    print("\nsection sample values:")
    print(df_raw['Section'].dropna().unique()[:10])

    print("\nsite name sample values:")
    print(df_raw['Site Name'].dropna().unique()[:10])

    print("\nSpecies sample values:")
    print(df_raw['Species'].dropna().unique()[:10])

    print("\nCounty sample values:")
    print(df_raw['County'].dropna().unique()[:10])

    print("\nWater Body sample values:")
    print(df_raw['Water Body'].dropna().unique()[:10])

    print("\nDate sample values:")
    print(df_raw['Date'].dropna().unique()[:10])
    return


@app.cell
def _(df_raw, pd):
    # data cleaning & dropping rows not needed
    df_clean = df_raw.drop(columns=["Range", "Section", "Town"])

    # convert date to datetime and keep only the date part (drop the time part)
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce').dt.date

    print(df_clean['Date'].dropna().unique()[:10])
    return (df_clean,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Top 10 Most Consistently Stocked Fish Species (2000-2025) 🐟

    ## The following species were **stocked every year** from 2000 to 2025 (26 years), showing consistent management focus on walleye and cold water species like trout & salmon.

    - Walleye leads by a huge margin with over **354** million fish stocked. 🐟🐟🐟🐟
    - Trout & Salmon dominate the list showing a priority and focus on **coldwater species**.🐟🐟🐟
    - Atlantic Salmon are stocked consistently but are by far **less stocked**.🐟🐟
    - Flathead minnows are a focus providing solid bait fish for predator fish. 🐟

    ###**This reflects long term investment in popular sport fish and strategic strategies across Michigan Waters.**
    """
    )
    return


@app.cell
def _(df_clean, pd):
    # top 10 most consistenly stocked fish from 2000 to 2025
    # group by year and species
    yearly_species = df_clean.groupby(['Date', 'Species'])['Number'].sum().reset_index()

    # extract year from the date
    yearly_species['Year'] = pd.to_datetime(yearly_species['Date']).dt.year

    # count how many years each species appears
    species_years = yearly_species.groupby('Species')['Year'].nunique()

    # total number of fish stocked per species
    species_total = yearly_species.groupby('Species')['Number'].sum()

    # combining and filtering
    species_stats = pd.DataFrame({
        'Years Stocked': species_years,
        'Total Fish Stocked': species_total
    })

    # sort by number of years for consistency and by fish total
    top_10_consistent = species_stats.sort_values(
        by=['Total Fish Stocked', 'Years Stocked'],
        ascending=False
    ).head(10)

    bottom_10_consistent = species_stats.sort_values(
        by=['Total Fish Stocked', 'Years Stocked'],
        ascending=True
    ).head(10)

    # format total fish with commas for readability
    top_10_consistent['Total Fish Stocked'] = top_10_consistent['Total Fish Stocked'].apply(lambda x: f"{x:,}")

    # top 10 stocked fish
    top_10_consistent
    return bottom_10_consistent, top_10_consistent, yearly_species


@app.cell
def _(plt, top_10_consistent):
    # plot from dataframe showing numbers
    # creating a copy to safely convert strings into integers
    top_10_plot = top_10_consistent.copy()
    if top_10_plot['Total Fish Stocked'].dtype== 'object':
        top_10_plot['Total Fish Stocked'] = top_10_plot['Total Fish Stocked'].replace({',': ''}, regex=True).astype(int)


    # convert to millions for readability
    top_10_plot['Stocked (M)'] = top_10_plot['Total Fish Stocked'] / 1_000_000

    # plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = plt.barh(top_10_plot.index[::-1], top_10_plot['Stocked (M)'][::-1], color='mediumseagreen')

    # addding labels and title
    plt.xlabel("Total Fish Stocked (Millions)")
    plt.title("Top 10 Consistently Stocked Fish Species in Michigan (2000 - 2025)")
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # adding data labels with 2 decimal places at end of each bar
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height() / 2,
                f"{width:.2f} M", va='center', fontsize=9)

    # adding footnote
    fig.text(0.95, 0.01, "Figures shown in millions", ha="right", fontsize=8, style='italic')

    # return figure so it shows in web dashboard
    fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # Bottom 10 Stocked Fish Species (2000-2025) 🐟

    ### This looks at the bottom 10 species of fish stocked by number of fish per species by year.

    ##The following species were stocked between 2000 to 2025 (26 years). **Some have only been stocked once throughout the 26 years this dataset covers.**
    - Species like flathead catfish & white sucker were stocked **only once**, with just a handful of fish. This reflects a healthy self sustaining population. 🐟🐟🐟🐟
    - Some species were stocked for 3 years and in **very limited numbers**. Tiger Musky is a world renouned prized sport fish.🐟🐟🐟
    - Stocking efforts are heavily focused on sport and game fish.🐟🐟
    - Some native or less popular species have minimal stocking efforts or experimental at best. Most likely due to a healthy self sustaining population.🐟

    ###**This again reflects a long term investment in popular sport fish & game fish and strategic strategies across Michigan Waters. Focusing on ecological and predator prey balance.**
    """
    )
    return


@app.cell
def _(bottom_10_consistent):
    # bottom 10 stocked fish
    bottom_10_consistent
    return


@app.cell
def _(bottom_10_consistent, plt):
    # bottom 10 plot
    bottom_10_plot = bottom_10_consistent.copy()
    if bottom_10_plot['Total Fish Stocked'].dtype == 'object':
        bottom_10_plot['Total Fish Stocked'] = (
            bottom_10_plot['Total Fish Stocked']
            .replace({',': ''}, regex=True)
            .astype(int)
        )
    # sorting before plotting
    bottom_10_plot = bottom_10_plot.sort_values(by='Total Fish Stocked', ascending=True).head(10)

    # creating plots
    fig1, ax1 = plt.subplots(figsize=(10,6))
    bars1 = ax1.barh(bottom_10_plot.index, bottom_10_plot['Total Fish Stocked'], color='mediumseagreen')


    # adding labels and title
    ax1.set_xlabel('Total Fish Stocked')
    ax1.set_title('Bottom 10 Fish Stocked Fish Species (2000-2025')
    ax1.invert_yaxis() # highest at the top

    # adding data labels at end of each bar
    for bar1 in bars1:
        width1 = bar1.get_width()
        ax1.text(
            width1 + max(bottom_10_plot['Total Fish Stocked']) * 0.01,  # small offset
            bar1.get_y() + bar1.get_height() / 2,
            f"{int(width1):,}",  # convert to int and format with commas
            va='center',
            fontsize=9
        )

    # footnote
    fig1.text(0.95, 0.01, "Figures shown in raw totals", fontsize=8, style='italic')

    #show plot
    fig1
    return


@app.cell
def _(mo):
    mo.md(r"""# **Looking at total fish stocked per year (2000 - 2025)**""")
    return


@app.cell
def _(plt, yearly_species):
    # grouping by year 
    yearly_totals = (
        yearly_species.groupby('Year')['Number'].sum().reset_index().sort_values('Year')
    )

    # plot the yearly trend
    fig2, ax2 = plt.subplots(figsize=(10,6))
    ax2.plot(yearly_totals['Year'], yearly_totals['Number'], marker='o', linestyle='-', color='mediumseagreen')

    # format the chart
    ax2.set_title('Total Fish Stocked Per Year in Michigan 2000 - 2025')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Total Fish Stocked')
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Show the figure
    fig2
    return (yearly_totals,)


@app.cell
def _(mo):
    mo.md(
        r"""
    - #### **There is a significant drop in stocking activity around 2007–2008, followed by another dip in 2020, likely due to COVID-19 and the recession in 2008.**
    - #### **Peak stocking years appear to be around 2006 / 07 and 2016 / 17, of which 2016 / 17 surpassed 40 million fish stocked total.**
    - #### **After 2015, there is a continued trend upwards in efforts but after 2016 / 17, there is consistent decline through 2020, reaching a low point of under 15 million fish stocked.**
    - ### **Post-2020 shows a brief recovery, but drops again in 2023–2024.**
    - ### **2025 shows a small rebound, with totals nearing 20 million fish stocked.**
    # **📊 In conclusion, despite periodic spikes, the overall trend from 2000 - 2025 indicates a general decline in fish stocking activity within Michigan. Factors such as; ecological, enviromental, & predator prey balance likely played a significant role aswell as political pressures.📊**
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## **Let's look at yearly averages, semi decade averages and decade averages.**""")
    return


@app.cell
def _(mo, yearly_totals):
    # yearly average 2000 to 2025 
    yearly_avg = yearly_totals['Number'].mean()

    # creating bins for semi decadal a nd decadal
    yearly_totals['5yr_bin'] = (yearly_totals['Year'] // 5) * 5
    yearly_totals['10yr_bin'] = (yearly_totals['Year'] // 10) * 10

    # calculating semi decadal average
    semi_decadal_avg = yearly_totals.groupby('5yr_bin')['Number'].sum().mean()

    # calculating decadal average
    decadal_avg = yearly_totals.groupby('10yr_bin')['Number'].sum().mean()

    # print results
    # print(f"Yearly Average from 2000 to 2025: {yearly_avg:,.0f} fish")
    # print(f"Semi Decadal Average: {semi_decadal_avg:,.0f} fish")
    # print(f"Semi Decadal Average: {decadal_avg:,.0f} fish")

    # trying to render as markdown using mo
    mo.md(f"""
    ## **Average Fish Stocked 2000 - 2025**
    - # **Yearly Average:** {yearly_avg:,.0f} fish
    - # **Semi Decadal Average (every 5 years):** {semi_decadal_avg:,.0f} fish
    - # **Decadal Average (every 10 years):** {decadal_avg:,.0f} fish
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""## **📊 From 2000 to 2025 Michigan stocked fish at a consistent and large scale. On average about 26.5 million fish stocked each year. When viewed in longer timeframes this averages to around 114.8 million fish stocked every 5 years and 229.6 million every 10 years. This reflects a sustained commitment to fishery management across decades.**""")
    return


@app.cell
def _(mo):
    mo.md(r"""# **Let's look at which species has seen an increase in stocking efforts and which have seen a decline.**""")
    return


@app.cell
def _(pd, plt, yearly_species):
    import numpy as np
    from scipy.stats import linregress

    # ensure yearly totals per species
    species_trends = (
        yearly_species.groupby(['Year', 'Species'])['Number']
            .sum()
            .reset_index()
    )

    # filter for 200-2025
    species_trends = species_trends[
        (species_trends['Year'] >= 2000) & (species_trends['Year'] <=2025)
    ]

    # claculate trend for each species
    trend_results = []
    for species, group in species_trends.groupby('Species'):
        if len(group['Year'].unique()) > 3:
            slope, intercept, r_value, p_value, std_err = linregress(group['Year'], group['Number'])
            trend_results.append({
                'Species' : species,
                'Slope' : slope,
                'Mean Stocked' : group['Number'].mean(),
                'Years Observed' : group['Year'].nunique()
            })
    trend_df = pd.DataFrame(trend_results)

    # identify increase & decrease
    trend_df['Trend'] = np.where(trend_df['Slope'] > 0, 'Increasing', 'Decreasing')

    # top 10 increasing and descreasing
    top_increasing = trend_df.sort_values('Slope', ascending=False).head(10)
    top_decreasing = trend_df.sort_values('Slope', ascending=True).head(10)

    print(top_increasing)
    # creating visual for the trends
    fig3, ax3 = plt.subplots(figsize=(10,6))
    ax3.barh(top_increasing['Species'], top_increasing['Slope'], color='mediumseagreen')
    ax3.set_title('Top 10 Increasing Fish Stocked (2000-2025')
    ax3.set_xlabel('Trend Slope (Fish per Year)')
    fig3
    return top_decreasing, trend_df


@app.cell
def _(mo):
    mo.md(
        r"""
    - # *The data shows fast growth for species like lake herring and flathead minnow.*
    - # *While some species show a fast growth in stocking numbers, salmonoids have maintained moderate efforts but have a high total stocking number.*
    - # *Small species like yellow perch and black crappie are slow growing in terms of slope and are naturally abundant in Michigan waters. There is still some stocking effort occuring but not as targeted as other species.*
    """
    )
    return


@app.cell
def _(plt, top_decreasing):
    # visuals for decreasing trend
    print(top_decreasing)
    fig4,ax4 = plt.subplots(figsize=(10,6))
    ax4.barh(top_decreasing['Species'], top_decreasing['Slope'], color='red')
    ax4.set_title('Top 10 Decreasing Fish Stocked (2000 - 2025)')
    ax4.set_xlabel('Trend Slope (Fish Per Year')
    fig4
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    - # *Significant decline in Chinook Salmon efforts, although they are the abdundant salmon species in Michigan waters, it shows a fine balance between population and ecosystem management.* ***(Salmon were introduced in Michigan to combat the invasive Alewife population within the Great Lakes in 1966).***
    - # **Alewife populations have been on the decline in recent times as evidenced by fluctuations in population by year and lake. Generally Lake Michigan has a healthier population according to recent studies & observations. Lake Huron's population declined in 2003 and has not fully recovered.**
    - # *Key game species like Lake Trout, Chinook Salmon, Walleye, Brown Trout, and Brooke Trout are top predetor fish and most likely reflect ecosystem management strategies or population balancing or both.*
    - # *Nothern Pike and Channel Catfish show a decline but also have a lower stocking average, meaning these species more than likely have a healthy self sustaining population in a majority of Michigan waters.*
    - # **The steady decline in alot of popular game fish most likely suggests that stocking efforts are taking a more ecological approach and are focusing on predetor prey balance.**
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# *Let's focus on Salmon, Steelhead, & Trout.*""")
    return


@app.cell
def _(trend_df):
    # focusing on STS (Salmon, Trout, Steelhead)
    focus_species = trend_df[
        trend_df['Species'].str.contains('Salmon|Trout|Steelhead', case=False)
    ].sort_values('Slope', ascending=False)
    print(focus_species)
    return (focus_species,)


@app.cell
def _(mo):
    mo.md(r"""# There is a slight increase in Coho & Atlantic salmon efforts but other than that, species are on a decline. Especially Chinook Salmon. Although they are the most widely caught, stocking efforts have decreased showing atlest some kind of corrolation between population, stocking efforts & Alewife populations""")
    return


@app.cell
def _(focus_species, plt):
    # focusing on STS
    fig5, ax5 = plt.subplots(figsize=(10,6))

    # color by slope
    colors = ['green' if slope > 0 else 'red' for slope in focus_species['Slope']]

    ax5.barh(focus_species['Species'], focus_species['Slope'], color=colors)
    ax5.set_title('Salmon, Steelhead, Trout Trend 2000 - 2025')
    ax5.set_xlabel('Trend Slope (Fish per Year)')
    fig5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # - Looking at the data, **it is surprising lake trout has been on the decline in terms of stocking efforts.**
    # -  Coho & Atltantic salmon are **prized catches** and are on the rise which is a good sign for the fisheries for these particular fish.
    # - **Did not know brooke trout was stocked**. Brooke trout are naturally occuring in Michigan. Shows that there is interest and efforts to support the natural brook trout fisheries within the state.
    #- Overall, Salmon, Steelhead & Trout are on the decline by majority. Coho & Atlantic salmon are the ones seeing an increase with every other individual species seeing a decline. This indicates one of four things in my opinion; **1) The fisheries for the fishes on the decline indicate a healthy and self sustaning population. In other words, a healthy population ratio between the taregted species and their prey. 2) The funding for said programs has drastically decreased. 3) There is an unhealthy balance of the target species and their prey. Or, 4) Unsuitable habitat coupled with 2 and 3.** (Furthere analysis is needed to fully understand the root cause of the decline)
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## **Lets look at Monthly totals from 2000 to 2025**""")
    return


@app.cell
def _(df_clean):
    # total fish stocked per county
    county_stocked = df_clean.groupby('County')['Number'].sum().reset_index(name='total_stocked')

    # sort from most to least
    county_stocked = county_stocked.sort_values(by='total_stocked', ascending=False)

    # declaring top and bottom 10
    top_10_counties = county_stocked.head(10)
    bottom_10_counties = county_stocked.tail(10)

    # show the top and bottom counties
    print("Counties with the most stocking efforts:")
    print(top_10_counties, '\n') # top 10 counties

    print("Counties with the lest stocking efforts:")
    print(bottom_10_counties) # bottom 10 counties
    return bottom_10_counties, top_10_counties


@app.cell
def _(df_clean, pd, plt):
    #Ensure Date is datetime format
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])

    # extract year and month
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['month'] = df_clean['Date'].dt.month

    # total nimber of fished stocked per month
    monthly_stocked = df_clean.groupby('month')['Number'].sum().reset_index(name='total_stocked')
    monthly_stocked = monthly_stocked.sort_values('month')
    monthly_stocked

    # visualization
    fig6, ax6 = plt.subplots(figsize=(10,6))

    # color for bars
    bar_colors = ['green'] * len(monthly_stocked)

    # horizontal bar chart
    ax6.barh(monthly_stocked['month'].astype(str), monthly_stocked['total_stocked'], color=bar_colors)

    # adding value labels
    for i, v in enumerate(monthly_stocked['total_stocked']):
        ax6.text(v + 0.5, i, f"{v:,}", color='black', va='center')

    # titles and labels
    ax6.set_title('Total Fish Stocked per Month (2000-2025')
    ax6.set_xlabel('Total Fish Stocked')
    ax6.set_ylabel('Month')

    # show plot
    fig6
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # **Over the years, majority of the stocking efforts have by far been in May. 290 Million fish have been stocked in May from 2000 to 2025. April is a far 2nd with 207 million fished stocked from 2000 to 2025.**

    # We can safetly say that majority of the stocking takes plane in **April, May & June respectively.**
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# **Let's plot top and bottom county numbers and then dive deeper and uncover insights**""")
    return


@app.cell
def _(plt, top_10_counties):
    # plotting top 10 counties
    fig7, ax7 = plt.subplots(figsize=(10,6))
    ax7.barh(top_10_counties["County"][::-1], top_10_counties['total_stocked'][:: -1], color="green") #reversed for better order

    # setting titles
    ax7.set_title("Top 10 Counties by Total Fish Stocked (2000 - 2025)")
    ax7.set_xlabel("Fish Stocked")

    # show plot
    fig7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # **Delta county by far sees the biggest effors. Most of the top 10 are what are considered prestine fishing waters within Michigan. Benzonia & Manistee counties are known hot spots for Salmon, Steelhead and Trout.**
    - **Many of the counties stocked are presite fishing waters within Michigan and produce quality fish consistenly**
    - **Muskegon River,  Big Manistee & Little Manistee, and Betsite River within Benzonia county are known State wide as solid fisheries with plenty of access for Salmon, Trout, and Steelhead.**
    - **Targeting tributaries of the river systems within the top 10 counties is VERY LIKELY to produce solid, quality fishing opportunities. (Provided you are targeting the dominant species within that fishery, at the right time of year, and using the right tackle)**
    - **The upper paninsula remains to be a stable of a fishery for Michiganders and tourists both domestic and foreign**
    """
    )
    return


@app.cell
def _(bottom_10_counties, plt):
    # bottom 10 plot
    fig8, ax8 = plt.subplots(figsize=(10,6))
    ax8.barh(bottom_10_counties['County'][:: -1], bottom_10_counties['total_stocked'][:: -1], color='red') # reversed for better order

    # setting titles
    ax8.set_title("Bottom 10 Counties By Total Fish Stocked (2000 - 2025)")
    ax8.set_xlabel("Total Fish Stocked")

    # show plot
    fig8
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # **To my suprise Midland & Saginaw are up there in terms of the least stocked counties. Mainly due to being a resident and hearing stories from other fishermen plus personal experience, the fishery in those counties seem to be healthy in the sense that you can catch a variety of fish from Catfish, Pike, Musky, Walleye, Sturgeon, and if you are very lucky an odd ball Salmon or Steelhead. Mainly steelhead and salmon are caught trolling within Midland's Titabawasee River around Posseyville bridge. Sturgeon can be caught from Posseyville bridge going downstream into the Saginaw River and the Saginaw Bay. The Chippewa River within Midland County is known to be a solid bass fishing location, excellent for fly fishing. Main thing to be aware of is pollution and do not eat advisories when fishing in Saginaw / Midland waters.**

    - **Most if not all of the bottom 10 counties are not known to be solid fishing locations and to some extent locals consider the river systems within as ' trash' & 'polluted". Saginaw bay is a solid fishery and has good numbers of multiple species but going upstream into Midland via the Saginaw River the more the river deteriorates according to locals.**
    - **The closer you are to Dow Chemical generally from there downwards is considered iffy in terms of polution. From the Tridge going upwards towards Sanford you have somewhat healthy fisheries for some species but accesss is limited and water quality varies.**
    -
    """
    )
    return


if __name__ == "__main__":
    app.run()
