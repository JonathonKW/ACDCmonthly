from jinja2 import FileSystemLoader, Environment
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
# from PIL import Image

# Seting up pandas, seaborn and site name formatting
pd.set_option("display.max_colwidth", 150)
sns.set_style("whitegrid")
#palette2 = ["0077cc","cc0077","77cc00"]
#sns.set_palette(palette2)
sns.set()

splt_dict = {}
months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
site_names = ["Belle River", "Renfrew", "Earlton", "Verner", "Kearney", "Sturgeon Falls", "Simcoe", "Newburgh", "Tecumseh", "Oldcastle","Waterford","Pontypool", "Thunder Bay", "Cache Bay", "Thomasburg", "Brockville", "Dundalk", "McDonalds Corners","100 King","102 Arnold","110 Arnold","28 Mill","390 Thomas","462 Riverview","601 Canarctic","Carson Horse Arena","Carson Barns 4 & 6","Carson Sales Barn","Cornerview Dairy","Cranberry Creek","Kemptville Storage","200 Centennial","225 Centennial","42 Commerce Park","66 Hincks","131 Sheldon","1177 Franklin","1195 Franklin","1425 Bishop","101 Wayne Gretzky","1500 Victoria","127 Aviva","151 Aviva","256 Aviva","280 Aviva"]
sites = pd.DataFrame(columns=None)
class PlantResults:

    splt_dict = {}
    site_names = ["Belle River", "Renfrew", "Earlton", "Verner", "Kearney", "Sturgeon Falls", "Simcoe", "Newburgh", "Tecumseh", "Oldcastle","Waterford","Pontypool", "Thunder Bay", "Cache Bay", "Thomasburg", "Brockville", "Dundalk", "McDonalds Corners","100 King","102 Arnold","110 Arnold","28 Mill","390 Thomas","462 Riverview","601 Canarctic","Carson Horse Arena","Carson Barns 4 & 6","Carson Sales Barn","Cornerview Dairy","Cranberry Creek","Kemptville Storage","200 Centennial","225 Centennial","42 Commerce Park","66 Hincks","131 Sheldon","1177 Franklin","1195 Franklin","1425 Bishop","101 Wayne Gretzky","1500 Victoria","127 Aviva","151 Aviva","256 Aviva","280 Aviva"]
    
    def __init__(self, site_name, filepath):
        # site name is the full name of the site
        # filepath takes us to the csv
        self.months = months
        self.site_name = site_name
        self.filepath = filepath

        self.dataset = os.path.split(filepath)[-1]
        self.df_results = csv_to_df(filepath)
        
        
    def self_graph(self):

        # Function to pull site data, turn it into a graph and save it
        # Will need to update this to function by month and year input, currently just pulls the available split data

        plt.figure(figsize=(8,6))

        df = pd.DataFrame(self.df_results).reset_index()
        sns.lineplot(x=df['month'],y=df["Generation"],hue=df["Source"],data=df)
        
        
        plt.xticks(ticks=[1,2,3,4,5,6,7,8,9,10,11,12],labels=months)
        fig_name = self.site_name + ".png"
        plt.savefig("./Outputs/" + fig_name)
        plt.close()
        return fig_name
        
       
    def csv_to_html(self):
    # Return a csv in an html format
    # This is helpful for tables already formatted properly into the csv
    # But I would need to do preformatting before I was able to just export like this

        html = self.df_results.to_html()
        return html

    

           
# Split functionality by site for the full dataset
def split_csv(filepath, year):
   
    df = pd.read_csv(filepath)
    df = pd.melt(df, id_vars=["plant_id","month","year"],value_vars=["MW_gen","weather_adj","pv_syst"],var_name="Source", value_name="Generation")
    # Melts so that I can use lineplot hue to create multi-lined graphs for generation, weather and pv syst

    number_sites = df['plant_id'].max()
    #  print(number_sites)
    for i in range(number_sites):
        current_data = df[(df['plant_id'] == (i + 1)) & (df['year'] == year)]
        name = site_names[i]
        splt_dict[name] = current_data
        csv_name = "datasets/" + name + ".csv"
        current_data.to_csv(csv_name, index=True)
    return splt_dict



# Opening the csv and returning it as a dataframe
def csv_to_df(filepath):
    # Open a csv, return it as a dataframe
    df = pd.read_csv(filepath, index_col=0)
    return df



#Configure Jinja, ready template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)


# Adding templates to the program
base_template = env.get_template("report.html")
table_section_template = env.get_template("table_section.html")


def main():
    # Entry point for script
    # Render a template, write to file
    # :return:
    split_csv("datasets/annual_data1.csv", 2020)
    # Adding content to be published
    title = "Model Report"

    sections = list()

    for i in range(len(site_names)):
        
        site = PlantResults(site_names[i], "datasets/" + site_names[i] + ".csv")
        sections.append(table_section_template.render(model=site.site_name, dataset= site.dataset, table = site.csv_to_html(), graph = site.self_graph()))
    

    #sections.append(table_section_template.render(model=renfrew.site_name, dataset=renfrew.dataset, table=renfrew.csv_to_html(), graph=renfrew.self_graph()))

    
    # I'm still not sure how github pages works (it says they want an index.md but I don't know what that is or how to use it locally so I create
    # this html file at the same time for my own preview purposes (hopefully this does not mess anything up on the deploy)
    with open("index.html", "w") as f:

        # Here we link the template to our code
        f.write(base_template.render(title=title, sections=sections))

    with open("index.md", "w") as f:

        # Here we link the template to our code
        f.write(base_template.render(title=title, sections=sections))

if __name__ == "__main__":
    
    main()
    # This will only run when the script is executed
    # When a script is imported, name is not changed (or is changed to match the name of the new imported location idk)
    # When THIS script is run, __name__ will be __main__ because THIS script is the MAIN script in which it exists
    # This is so we can define classes and functions (like csv_to_html above) here, and still use them in other scripts without having to rewrite them, but also without
    # having to run everything again
