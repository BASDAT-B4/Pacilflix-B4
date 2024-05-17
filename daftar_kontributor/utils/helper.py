import datetime

class EncodeHelper:
    def toSQL(cursor):
        columns = []
        for col in cursor.description:
            columns.append(col[0])
        
        rows = cursor.fetchall()
        result = []

        if not rows:
            row_dict = {}
            for column in columns:
                row_dict[column] = "-"
            result.append(row_dict)
        else:
            for row in rows:
                row_dict = {}
                for j, value in enumerate(row):
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row_dict[columns[j]] = value.strftime("%d %B %Y")  # Format tanggal
                    else:
                        row_dict[columns[j]] = value
                result.append(row_dict) 
        print(result)
        return result
