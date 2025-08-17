from gui.app import app 

if __name__ == "__main__":
    app.launch(server_port=10000, server_name="0.0.0.0", share=True)