import sqlite3

con = sqlite3.connect("database\\data.db")
cursor = con.cursor()
COLS = ("type", "telegram_link", "activity_type",
        "activity", "experience", "education", "place")
TRANSLATE = {
        "activity_type": {
            'r': "Вид діяльності (обрати зі списку)",
            'e': "Вид діяльності (обрати зі списку)"},
        "activity": {
            'r': "Опис вакансії",
            'e': "Побажання щодо професії"},
        "experience": {
            'r': "Досвід роботи",
            'e': "Досвід роботи"},
        "education": {
            'r': "Рівень освіти",
            'e': "Рівень освіти"},
        "place": {
            'r': "Місце роботи",
            'e': "Місце роботи"},
}
def push(utype, tlink, tact=None, act=None, xp=None, edu=None, place=None):
    fields = {
        "type": utype,
        "telegram_link": tlink,
        "activity_type": tact,
        "activity": act,
        "experience": xp,
        "education": edu,
        "place": place,
    }
    headers = [i for i,j in fields.items() if j]
    values = [j for j in fields.values() if j]
    if not headers or not values:
        return
    if exist(tlink):
        key_value = []
        args = []
        for i, j in zip(headers, values):
            key_value.append(f"{i}=?")
            args.append(j)
        string = f"UPDATE Users SET {', '.join(key_value)} "\
                 f"WHERE telegram_link='{tlink}'"
        cursor.execute(string, args)
    else:
        string = f"INSERT INTO Users({', '.join(headers)}) "\
                 f"VALUES ({', '.join('?'*len(headers))})"
        cursor.execute(string, values)
    con.commit()

def get_same(kind, tact, xp, edu):
    stype = 'e' if kind == 'r' else 'r' 
    query = "SELECT telegram_link, activity FROM Users WHERE type=? AND activity_type=? AND education=? AND experience=?"
    res = list(cursor.execute(query, (stype, tact, edu, xp)))
    return res
def get_info(name):
    return list(cursor.execute(f"SELECT * FROM Users WHERE telegram_link='{name}'"))[0] 
def get(name, fieldname):
    for i in cursor.execute(f"SELECT {fieldname} FROM Users WHERE telegram_link = '{name}'"):
        return i[0]
def get_emptycols(name):
    res = []
    for i, data in enumerate(list(cursor.execute(f"SELECT * FROM Users WHERE telegram_link = '{name}'"))[0]): 
        print(i, data)
        if data is None:
            res.append(COLS[i])
    return res

def exist(tlink):
    cursor.execute(f"SELECT COUNT(*) FROM Users WHERE telegram_link = '{tlink}'")
    if cursor.fetchone()[0] == 0:
        return False
    return True

def remove(tlink):
    cursor.execute(f"DELETE FROM Users WHERE telegram_link = '{tlink}'")


"""
Users - table_name:
type CHAR(1), telegram_link TEXT, activity_type TEXT, 
activity TEXT, experience CHAR(1), education TEXT, place TEXT
"""
