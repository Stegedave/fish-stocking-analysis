import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt

    mo.md("#🐟Fish Stocking Data Cleaning🎣.")
    return mo, pd, plt


@app.cell
def _(mo):
    mo.md("""##Looking at stocking reports provided by the Michigan Department of Natural Resources to see how efforts have changed overtime.""")
    return


@app.cell
def _(mo):
    mo.md(r"""## Loading the dataset and checking first 5 rows of the data.""")
    return


@app.cell
def _(pd):
    # load the raw csv
    df_raw = pd.read_csv('../data/fish_stocking_data.csv')
    df_raw.head()
    return (df_raw,)


@app.cell
def _(mo):
    mo.md(r"""## Summarizing the dataset and checking first 5 rows of the data for missing values compared to totals.""")
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

    # print(df_clean['Date'].dropna().unique()[:10])
    return (df_clean,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Top 10 Most Consistently Stocked Fish Species (2000-2025) 🐟

    ## The following species were **stocked every year** from 2000 to 2025 (26 years), showing consistent management focus on walleye and cold water species like trout & salmon.

    - Walleye leads by a huge margin with over **354** million fish stocked. 🐟🐟🐟
    - Trout & Salmon dominate the list showing a priority and focus on **coldwater species**.🐟🐟
    - Atlantic Salmon are stocked consistently but are by far **less stocked**.🐟

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
    return bottom_10_consistent, top_10_consistent


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

    # adding data labels with 2 decimal places
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height() / 2,
                f"{width:.2f} M", va='center', fontsize=9)

    # adding footnote
    fig.text(0.95, 0.01, "Figures shown in millions", ha="right", fontsize=8, style='italic')

    # return figure so it shows in web dashboard
    fig
    return ax, fig


@app.cell
def _(mo):
    mo.md(
        r"""
    # Bottom 10 Consistently Stocked Fish Species (2000-2025) 🐟

    ##The following species were **stocked every year** from 2000 to 2025 (26 years).
    - Species like flathead catfish & white sucker were stocked **only once**, with just a handful of fish. 🐟🐟🐟
    - Some species were stocked for 3 years and in **very limited numbers**.🐟🐟
    - Stocking efforts are heavily focused on sport and game fish.🐟
    - Some native or less popular species have minimal stocking efforts or experimental at best.

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
def _(ax, bottom_10_consistent, fig, plt):
    # bottom 10 plot
    bottom_10_plot = bottom_10_consistent.copy()
    if bottom_10_plot['Total Fish Stocked'].dtype== 'object':
        bottom_10_plot['Total Fish Stocked'] = bottom_10_plot['Total Fish Stocked'].replace({',': ''}, regex=True).astype(int)

    # creating plots
    fig2, ax2 = plt.subplots(figsize=(10,6))
    bars2 = ax2.barh(bottom_10_plot.index, bottom_10_plot['Stocked'], color='teal')

    # adding labels and title
    ax.set_xlabel('Total Fish Stocked')
    ax.set_title('Bottom 10 Fish Stocked Fish Species (2000-2025')
    ax.ivert_yaxis # highest at the top

    #show plot
    fig
    return


if __name__ == "__main__":
    app.run()
