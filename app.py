""" Simple Flask Blog WebApp
    Developped by: Luiz Marin """
from website import create_app

if __name__ == '__main__':
    app = create_app
    app.run(debug=True)