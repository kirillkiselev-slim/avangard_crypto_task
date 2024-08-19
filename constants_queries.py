CREATE_CRYPTO_TABLE = ('CREATE TABLE IF NOT EXISTS'
                       ' crypto(crypto_slug TEXT UNIQUE);')
INSERT_CRYPTO_SLUG_NAMES = 'INSERT INTO crypto(crypto_slug) VALUES (?)'

CREATE_USER_TABLE = ('CREATE TABLE IF NOT EXISTS user('
                     'user TEXT UNIQUE, '
                     'crypto TEXT, '
                     'max_value REAL, '
                     'min_value REAL);')

CHECK_CRYPTO_EXISTENCE = 'SELECT crypto_slug FROM crypto WHERE crypto_slug = ?'