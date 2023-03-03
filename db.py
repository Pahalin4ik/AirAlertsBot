import sqlite3


class BotDB:
    def __init__(self, file: str):
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id: int):
        with self.conn:
            result = self.cursor.execute('SELECT `id` FROM `users` WHERE `user_id` = ?', (user_id,))
            return bool(len(result.fetchall()))

    def get_users_by_tag(self, tag: str):
        with self.conn:
            result = self.cursor.execute('SELECT user_id, lang FROM users WHERE area_tag = ?', (tag,))
            return result.fetchall()

    def add_user(self, user_id, lang, tag):
        with self.conn:
            self.cursor.execute('INSERT INTO `users` (`user_id`, `lang`, `area_tag`) VALUES(?, ?, ?)',
                                (user_id, lang, tag))
            self.conn.commit()

    def get_user_lang(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `lang` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()[0]
            return result[0]

    def upd_lang(self, user_id, lang):
        with self.conn:
            self.cursor.execute("update users set lang = ? where user_id = ?", (lang, user_id))

    def upd_region(self, user_id, region):
        with self.conn:
            self.cursor.execute("update users set area_tag = ? where user_id = ?", (region, user_id))

    def close(self):
        self.conn.close()

