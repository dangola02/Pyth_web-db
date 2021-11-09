# Pyth_web-db
```shell
Web application to search news about cryptocurrency.
```
## Installation
- Install dependencies:
- 
```shell
pip install -r requirements.txt
```
In Main add coins that you want to search articles about and store in database.
```
if __name__ == '__main__':
    setup_db()
    # list here coins you want to add to db, separated by comma
    add_news_of_currencies_to_db('bitcoin', 'ethereum')
    app.run(debug=True)
```

- Run application:

```shell
python3 src/web-pyth.py
```

## Usage

In order to use the application, simply enter the name of the cryptocurrency in the text field and click on the search button.

## Example

<p align="center">
  <img src="https://user-images.githubusercontent.com/78271298/140936713-c8f406b9-4edc-458d-8ae8-7bfc9ad536d1.jpg" />
</p>
