from flask import Flask, render_template
from routes.chat_routes import chat_bp
from routes.invoice_routes import invoice_bp
from routes.project_routes import project_bp
app=Flask(__name__)
app.register_blueprint(chat_bp,url_prefix='/api/chat')
app.register_blueprint(invoice_bp,url_prefix='/api/invoice')
app.register_blueprint(project_bp,url_prefix='/api/project')
@app.route('/')
def home(): return render_template('index.html')
@app.route('/health')
def health(): return {'status':'healthy'}
if __name__=='__main__': app.run()
