from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "data/history.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    er = None
    error_msg = ""

    if request.method == "POST":
        try:
            likes = int(request.form["likes"])
            comments = int(request.form["comments"])
            shares = int(request.form["shares"])
            followers = int(request.form["followers"])

            # Validasi nilai tidak boleh negatif
            if min(likes, comments, shares, followers) < 0:
                error_msg = "Nilai yang takasih masuk nda boleh Negatif, PAHAM!"
            elif followers == 0:
                error_msg = "Jumlah followersta nda boleh 0 bosku, kayak tong akun baru"
            else:
                # Hitung engagement rate
                er = round(((likes + comments + shares) / followers) * 100, 2)

                # Simpan ke dalam CSV
                new_data = pd.DataFrame([{
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "followers": followers,
                    "engagement_rate": er
                }])

                new_data.to_csv(
                    CSV_FILE,
                    mode='a',
                    header=not os.path.exists(CSV_FILE),  # tulis header kalau belum ada file
                    index=False
                )

        except ValueError:
            error_msg = "yang ta Input nda VALID bosku, masukkan angka yang benar, PAHAM!"

    return render_template("index.html", er=er, error_msg=error_msg)


@app.route("/history")
def history():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        return render_template("history.html", tables=[], titles=[])

    df = pd.read_csv(CSV_FILE)
    return render_template(
        "history.html",
        tables=[df.to_html(classes='data table table-striped', index=False)],
        titles=df.columns.values
    )


if __name__ == "__main__":
    app.run(debug=True)
