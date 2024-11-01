from flask import Flask, request, render_template_string
import csv
import time

app = Flask(__name__)

bin_data = {}


def load_bin_data(filename='./utils/binlist-data.csv'):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bin_data[row['bin']] = {
                'brand': row['brand'],
                'type': row['type'],
                'country': row['country']
            }


load_bin_data()

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Identifier</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h2>Введите номер карты:</h2>
    <form id="cardForm">
        <label for="card_number">Номер карты:</label><br><br>
        <input type="text" id="card_number" name="card_number" maxlength="16" pattern="\\d{6,16}" placeholder="Цифры 0-9, от 6 до 16 символов" required style="width: 300px;" required>
        <button type="submit">Отправить</button>
    </form>

    <h3>Результаты:</h3>
    <table id="resultsTable">
        <thead>
            <tr>
                <th>Банк</th>
                <th>Тип</th>
                <th>Страна</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>

    <script>
        document.getElementById("cardForm").onsubmit = async function(event) {
            event.preventDefault();

            const cardNumber = document.getElementById("card_number").value;
            const response = await fetch('/get-card-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ card_number: cardNumber })
            });
            
            const result = await response.json();
            updateResultsTable(result);
        };

        function updateResultsTable(result) {
            const tableBody = document.getElementById("resultsTable").getElementsByTagName('tbody')[0];
            const newRow = tableBody.insertRow();
            const brandCell = newRow.insertCell(0);
            const typeCell = newRow.insertCell(1);
            const countryCell = newRow.insertCell(2);
            
            if (result.error) {
                brandCell.colSpan = 3;
                brandCell.innerHTML = result.error;
            } else {
                brandCell.innerHTML = result.brand;
                typeCell.innerHTML = result.type;
                countryCell.innerHTML = result.country;
            }
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(html_template)


@app.route('/get-card-info', methods=['POST'])
def get_card_info():
    data = request.get_json()
    card_number = data.get('card_number')
    if not card_number.isdigit() or len(card_number) < 6:
        return {"error": "Ошибка: Введите корректный номер карты (минимум 6 цифр)."}, 400

    # Имитация задержки
    time.sleep(3)

    bin_number = card_number[:6]

    card_info = bin_data.get(bin_number)
    if card_info:
        return {
            "brand": card_info['brand'],
            "type": card_info['type'],
            "country": card_info['country']
        }, 200
    else:
        return {"brand": "Информация не найдена.", 'type': '-', 'country': '-'}, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
