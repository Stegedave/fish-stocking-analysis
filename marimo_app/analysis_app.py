import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    return mo, pd, plt


@app.cell
def _(mo):
    mo.md(
        """
    #🐟Fish Stocking Data Analysis🎣.
    ## Looking at stocking reports provided by the Michigan Department of Natural Resources to see how efforts have changed overtime.
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
    1. ### What are the yearly averages of each top 10 species stocked?
    1. ### What time of year (month) does stocking usually take place? How many times a year? 
    1. ### Which counties see the most effort in stocking? Which ones see significantly less efforts? 
    1. ### What Counties see the highest stocking efforts and which ones see the lowest stocking efforts?
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
    mo.md(r"""### **Summarizing the dataset and checking columns of the data for missing values compared to totals.**""")
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
def _(mo):
    mo.md(r""" """)
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

    # print(df_clean['Date'].dropna().unique()[:10])
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
    - Flathead minnows are a focus providing solid bait fish for predetor fish. 🐟

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
    - Species like flathead catfish & white sucker were stocked **only once**, with just a handful of fish. 🐟🐟🐟🐟
    - Some species were stocked for 3 years and in **very limited numbers**.🐟🐟🐟
    - Stocking efforts are heavily focused on sport and game fish.🐟🐟
    - Some native or less popular species have minimal stocking efforts or experimental at best.🐟

    ###**This again reflects a long term investment in popular sport fish & game fish and strategic strategies across Michigan Waters.**
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
    - #### **There is a significant drop in stocking activity around 2007–2008, followed by another dip in 2020, likely due to COVID-19 and the recessio in 2008.**
    - #### **Peak stocking years appear to be around 2006 / 07 and 2016 / 17, of which 2016 / 17 surpassed 40 million fish stocked total.**
    - #### **After 2015, there is a continued trend upwards in efforts but after 2016 / 17, there is consistent decline through 2020, reaching a low point of under 15 million fish stocked.**
    - ### **Post-2020 shows a brief recovery, but drops again in 2023–2024.**
    - ### **2025 shows a small rebound, with totals nearing 20 million fish stocked.**
    - # **📊 In conclusion, despite periodic spikes, the overall trend from 2000 -  2025 indicates a general decline in fish stocking activity in Michigan. These patterns, such as the decline during covid 19 and the 08 recession, indicate economic, enviromental and external pressures likely significantly influence the stocking efforts. 🪓**
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# **Let's look at yearly averages, semi decade averages and decade averages.**""")
    return


@app.cell
def _(mo, yearly_totals):
    # yearly average 2000 to 2025 
    yearly_avg = yearly_totals['Number'].mean()

    # creating bins for semi decadal a nd decadal
    yearly_totals['5yr_bin'] = (yearly_totals['Year'] // 5) * 5
    yearly_totals['10yr_bin'] = (yearly_totals['Year'] // 10) * 10

    # calculating semi decadal average
    semi_decadal_avg = yearly_totals.groupby('5yr_bin')['Number'].mean().mean()

    # calculating decadal average
    decadal_avg = yearly_totals.groupby('10yr_bin')['Number'].mean().mean()

    # print results
    # print(f"Yearly Average from 2000 to 2025: {yearly_avg:,.0f} fish")
    # print(f"Semi Decadal Average: {semi_decadal_avg:,.0f} fish")
    # print(f"Semi Decadal Average: {decadal_avg:,.0f} fish")

    # trying to render as markdown using mo
    mo.md(f"""
    ### **Average Fish Stocked 2000 - 2025**
    - **Yearly Average:** {yearly_avg:,.0f} fish
    - **Semi Decadal Average:** {semi_decadal_avg:,.0f} fish
    - **Decadal Average:** {decadal_avg:,.0f} fish
    """)
    return


if __name__ == "__main__":
    app.run()
