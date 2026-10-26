from flask import render_template,Flask
#
def app_create():

    from .main.Controller import blueprint_main
    #
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    #
    app.register_blueprint(blueprint_main)
    #
    return app