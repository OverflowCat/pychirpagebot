from dotenv import load_dotenv
load_dotenv()
import os
import pymysql.cursors
def exe(operation):
# Connect to the database
  connection = pymysql.connect(host=  os.environ['PYCMYSQLHOST'],
                             user=    os.environ['PYCMYSQLUSER'],
                             password=os.environ['PYCMYSQLPWD'],
                             database='twimg',
                             cursorclass=pymysql.cursors.DictCursor)
  with connection:
      with connection.cursor() as cursor:
          cursor.execute(operation)
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      connection.commit()

exe("""INSERT INTO `jpg`
(`twitter`, `telegraph`)
VALUES("test", "testpy1")
""")