from jinja2 import FileSystemLoader, Environment

# Content to be published
content = "Hello, world"


#Configure Jinja, ready template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

template = env.get_template("report.html")

def main():
    # Entry point for script
    # Render a template, write to file
    # :return:

    with open("outputs/report.html", "w") as f:

        # Here we link the template to our code
        f.write(template.render(content=content))

if __name__ == "__main__":
    main()
    
