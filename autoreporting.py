from jinja2 import FileSystemLoader, Environment

# Content to be published
content = "Hello, world"


#Configure Jinja, ready template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

template = env.get_template("report.html")