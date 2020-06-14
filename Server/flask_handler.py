from flask import Flask, render_template, request, redirect
import os
import Compare_Recordings

app = Flask(__name__)
Upload_path = os.path.abspath(os.path.dirname(__file__))
print(Upload_path)
app.config.update(UPLOADED_PATH=os.path.join(Upload_path, 'Recordings'))


def compare():
    result = Compare_Recordings.main()
    return result


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        if f.filename == '4.wav':
            res = compare()
            if res:
                return redirect("http://www.youtube.com")
            else:
                return render_template('error.html')
        return render_template('upload.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
