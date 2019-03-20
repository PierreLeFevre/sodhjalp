from flaskr import create_app

app = create_app()

if __name__ == "__main__":
	try:
		app.run(host="0.0.0.0", port=80, ssl_context=('cert.pem', 'key.pem'))
    except:
    	app.run(host="0.0.0.0", port=80)