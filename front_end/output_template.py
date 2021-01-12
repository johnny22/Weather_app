"""Generates a jinja template."""
import jinja2



loader = jinja2.FileSystemLoader('Templates')
Env = jinja2.Environment(loader=loader)
template = Env.get_template('template.html')
#template.globals['return_print_var'] = return_print_var
#template.globals['len'] = len 

def render_template(dict_list):
    """This renders the jinja template."""
    return template.render(dict_list=dict_list)
