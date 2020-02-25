from jinja2 import FileSystemLoader, Environment

# Content to be published
content = "Hello, world"


#Configure Jinja, ready template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

# Adding templates to the program
base_template = env.get_template("report.html")
table_section_template = env.get_template("table_section.html")

# Adding content to be published
title = "Model Report"
sections = list()
sections.append(table_section_template.render(model="ModelTitle?",
dataset="Results.csv", table="table"))

sections.append(table_section_template.render(model="Model22", dataset="dataset2.csv", table="Table2!!!!"))




def main():
    # Entry point for script
    # Render a template, write to file
    # :return:

    with open("outputs/report.html", "w") as f:

        # Here we link the template to our code
        f.write(base_template.render(title=title, sections=sections))

if __name__ == "__main__":
    main()
    
