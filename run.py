from app import app
from multiprocessing import Process


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)