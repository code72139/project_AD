from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Iniciando servidor en http://localhost:5000")
    app.run(debug=True, port=5000)