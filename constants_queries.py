CREATE_CRYPTO_TABLE = ('CREATE TABLE IF NOT EXISTS'
                       ' crypto(crypto_slug TEXT UNIQUE);')
INSERT_CRYPTO_SLUG_NAMES = 'INSERT INTO crypto(crypto_slug) VALUES (?)'

CREATE_USER_TABLE = ('CREATE TABLE IF NOT EXISTS user('
                     'user TEXT, '
                     'crypto TEXT, '
                     'max_value REAL, '
                     'min_value REAL, '
                     'date_added TEXT);')

CHECK_CRYPTO_EXISTENCE = 'SELECT crypto_slug FROM crypto WHERE crypto_slug = ?'

INSERT_USER_CRYPTO = ('INSERT INTO user(user, crypto, max_value,'
                      ' min_value, date_added) VALUES(?, ?, ?, ?, ?);')
